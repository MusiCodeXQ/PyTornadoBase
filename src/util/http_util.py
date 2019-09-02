from json import JSONDecodeError

from jsonschema import validate, validators, Draft7Validator, _utils
import json
import re
from jsonschema.exceptions import _Error

from src.util.json_encoder import JsonEncoder

table = dict(Draft7Validator.VALIDATORS)


def pattern(validator, patrn, instance, schema):
    if (
            validator.is_type(instance, "string") and
            not re.search(patrn, instance)
    ):
        yield ValidationError(schema)


def min_length(validator, mL, instance, schema):
    if validator.is_type(instance, "string") and len(instance) < mL:
        yield ValidationError(schema)


def required(validator, required, instance, schema):
    if not validator.is_type(instance, "object"):
        return
    for property in required:
        if property not in instance:
            yield ValidationError(property, type="required")


def type(validator, types, instance, schema):
    types = _utils.ensure_list(types)
    if not any(validator.is_type(instance, type) for type in types):
        nschema = schema.copy()
        nschema['msg'] = types_msg(instance, types)
        yield ValidationError(nschema, type='type')


# add some rules
table['pattern'] = pattern
table['minLength'] = min_length
table['required'] = required
table['type'] = type
meta_schema = {"type": "object",
               "properties": {
                   "group_name": {"type": "string"}
               }}
v = validators.create(meta_schema={}, validators=table)


async def check(self, schema, fun, success=None, fail=None):
    self.set_header('Access-Control-Allow-Origin', '*') 
    self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
    try:
        instance = json.loads(
            self.request.body.decode('utf-8'))
        validate(instance=instance, schema=schema, cls=v)
        msg=''
        try:
            msg=await fun(instance)
        except FunErro as erro:
            if fail is not None:
                await fail(instance)
            else:
                self.set_status(erro.code)
                self.write("""{"code":%d,"data":"%s"}""" % (erro.code, erro.msg))
        # except Exception as erro:
        #     self.set_status(500)
        #     self.write("""{"code":%d,"data":"%s"}""" % (500, str(erro)))
        else:
            if success is not None:
                success(instance)
            else:
                self.set_status(200)
                if msg is not None:
                    self.write("""{"code":"200","data":"%s"}"""%msg)
                else:
                    self.write("""{"code":"200","data":"success"}""")

                return
    except JSONDecodeError as erro:
        self.set_status(320)
        self.write("""{
            "code":320,
            "data":"json格式校验错误"
        }""")
        return
    except ValidationError as err:
        if fail is not None:
            fail(instance)
        else:
            self.set_status(406)
            self.write("""{"code":"406","data":%s}""" % err.message)
            return
        pass

def wegood(self,data={'code':200,'msg':'success'}):
    self.set_header("Content-Type", "application/json")
    self.set_status(200)
    if data is not None:
        data={'code':200,'msg':'success','data':data}
    self.write(json.dumps(data,cls=JsonEncoder))

    
def webad(self,code,data):
    self.set_header("Content-Type", "application/json")
    self.set_status(code)
    self.write(json.dumps(data, cls=JsonEncoder))


class FunErro(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class ValidationError(_Error):
    _word_for_schema_in_error_message = "schema"
    _word_for_instance_in_error_message = "instance"

    def __init__(self, map, type="default"):
        if isinstance(map, dict) and type == "default":
            name = map.get('name', "")
            erro = map.get("erro", "参数错误")
            msg = '{"name":"%s","msg":"%s"}' % (name, erro)
            _Error.__init__(self, msg)
        elif isinstance(map, dict) and type == "type":
            msg = '{"name":"%s","msg":"%s"}' % (map.get('name', ""), map['msg'])
            _Error.__init__(self, msg)

        elif isinstance(map, str) and type == "required":
            msg = '{"name":"%s","msg":"缺少参数"}' % (map)
            _Error.__init__(self, msg)

        elif isinstance(map, str):
            _Error.__init__(self, map)


def types_msg(instance, types):
    """
    Create an error message for a failure to match the given types.

    If the ``instance`` is an object and contains a ``name`` property, it will
    be considered to be a description of that object and used as its type.

    Otherwise the message is simply the reprs of the given ``types``.

    """

    reprs = []
    for type in types:
        try:
            reprs.append(repr(type["name"]))
        except Exception:
            reprs.append(repr(type))
    return """ %r 类型错误,应是 %s """ % (instance, ", ".join(reprs))

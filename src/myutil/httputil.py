from jsonschema import validate, validators, Draft7Validator, _utils
import json
import re
from jsonschema.exceptions import _Error, ValidationError
 
table = dict(Draft7Validator.VALIDATORS)


def pattern(validator, patrn, instance, schema):
    if (
            validator.is_type(instance, "string") and
            not re.search(patrn, instance)
    ):
        yield ValidationError(schema)


def minLength(validator, mL, instance, schema):
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
        nschema=schema.copy()
        nschema['msg']=types_msg(instance, types)
        yield ValidationError(nschema, type='type')


# add some rules
table['pattern'] = pattern
table['minLength'] = minLength
table['required'] = required
table['type'] = type
meta_schema={"type": "object",
            "properties": {
                "group_name": {"type": "string"}
            }}
v = validators.create(meta_schema={}, validators=table)


async def check(self, schema, fun, success=None, fail=None):

    instance = json.loads(
        self.request.body.decode('utf-8'))
    try:
        validate(instance=instance, schema=schema, cls=v)
        await fun(instance)
        if success is not None:
            success(instance)
        else:
            self.set_header("Content-Type", "application/json")
            self.set_status(200)
            self.write("""{"code":"200","body":"success"}""")
    except ValidationError as err:
        if fail is not None:
            fail(instance)
        else:
            self.write("""{"code":"406","body":%s}""" % err.message)
        pass


class ValidationError(_Error):
    _word_for_schema_in_error_message = "schema"
    _word_for_instance_in_error_message = "instance"

    def __init__(self, map, type="default"):
        if isinstance(map, dict) and type == "default":
            name = map.get('name', "")
            erro = map.get("erro","参数错误")
            msg = '{"name":"%s","msg":"%s"}' % (name, erro)
            _Error.__init__(self, msg)
        elif isinstance(map, dict) and type == "type":
            msg = '{"name":"%s","msg":"%s"}' % (map.get('name', ""),map['msg'])
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

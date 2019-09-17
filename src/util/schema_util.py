schema = {
    "type": "object",
    "properties": {
        "name": {"name": "name", "type": "string", "minLength": 1},
        "phone": {"name": "phone", "type": "string", "minLength": 11,
                  "pattern": "^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$",
                  "erro": "手机号输入错误"},
        "remarks": {"name": "remarks", "type": "string", "minLength": 1, "erro": "备注输入非法"},
    },
    "required": ["name", "phone", "remarks"]
}


def get_default_sc() -> {}:
    schema = {
        "type": "object",
        "properties": {
        }, "required": []
    }
    return schema


def add_sc_pro(schema, name: str, pro_type, min_length: int = None, max_length: int = None,need=True,pattern=None ):
    map = {'type': pro_type}
    if min_length is not None:
        map['minLength'] = min_length
    if max_length is not None:
        map['maxLength'] = max_length
    if name is not None:
        map['name'] = name
    if pattern is not None:
        map['pattern']=pattern
    schema['properties'][name] = map
    if need:
        schema['required'].append(name)

def add_sc_data(schema, names: list,need=True):
    for name in names:
        add_sc_pro(schema,name,ProTypes.STRING,need=need)

def add_sc_data_n(schema, datas: list,need=True):
    for data in datas:
        tp=data.value_type
        if tp==ProTypes.DATATIME:
            tp=ProTypes.STRING
        add_sc_pro(schema,data.name,tp,need=data.need)

def add_inner_pro(schema, name: str,key:str ,pro_type, min_length: int = None, max_length: int = None,pattern=None):
    map = {'type': pro_type}
    if min_length is not None:
        map['minLength'] = min_length
    if max_length is not None:
        map['maxLength'] = max_length
    if name is not None:
        map['name'] = name
    if pattern is not None:
        map['pattern']=pattern
    schema['properties'][key] = map



class ProTypes:
    STRING = 'string'
    NUMBER = 'number'
    BOOLEAN='boolean'
    INTEGER='integer'
    ARRAY = 'array'
    TIMESTAMP='timestamp'#string
    FLOAT='number'
    DATATIME='datatime'#string

def get_phone_schema() -> {}:
    return {"name": "phone", "type": "string", "minLength": 11,
            "pattern": "^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$",
            "erro": "手机号输入错误"}

def get_phone_pattern():
    return "^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$"

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

def getDefaltSchema():
    schema = {
            "type": "object",
            "properties": {
                },
            }
    return schema

def addSchemaProperties(schema,name,map):
    schema['properties'][name]=map
    pass

def getPhoneSchema():
    return {"name": "phone", "type": "string", "minLength": 11,
                  "pattern": "^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$",
                  "erro": "手机号输入错误"}
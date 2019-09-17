import datetime

from src.util.schema_map import ProTypes


class BaseData:
    def __init__(self):
        self.data = []
        self.data_type = {}

    def get_register(self):
        return self.data

    def get_selector(self):
        return self.data

    def get_columns(self, data: list):
        str = ''
        for i in range(0, len(data)):
            if i == len(data) - 1:
                str += data[i]
            else:
                str += data[i] + ','
        return str

    def get_placeholders(self, data):
        sql = ''
        for i in range(1, len(data) + 1):
            if i == len(data):
                sql += '$' + str(i)
            else:
                sql += '$' + str(i) + ','
        return sql

    def get_update(self,data:list):
        sql=''
        for i in range(2,len(data)+2):
            if i == len(data)+1:
                sql+="{}=${}".format(data[i-2],str(i))
            else:
                sql+="{}=${},".format(data[i-2],str(i))
        return sql

    def get_data_type(self, name):
        return self.data_type.get(name) if self.data_type.get(name) else ProTypes.STRING

    def get_sql_args(self, inst: dict, data: list):
        values = []
        for name in data:
            tp = self.get_data_type(name)
            v = None
            if tp == ProTypes.STRING:
                v = inst[name]
            elif tp == ProTypes.NUMBER:
                v = int(inst[name])
            elif tp == ProTypes.BOOLEAN:
                v = inst[name]
            elif tp == ProTypes.FLOAT:
                v = float(inst[name])
            elif tp == ProTypes.DATATIME:
                v = datetime.datetime.strptime(inst[name], '%Y-%m-%d %H:%M:%S');
            else:
                v = inst[name]
            values.append(v)
        return tuple(values)


class User(BaseData):

    def __init__(self):
        super().__init__()
        self.data = ['id', 'name', 'age']
        self.data_type = {'id': ProTypes.NUMBER, 'age': ProTypes.NUMBER}

    def get_selector(self):
        ignore = ['id']
        # 填写忽略代码
        data = self.data.copy()
        data.remove('id')
        return data

    pass


def aa(*args):
    for i in args:
        print(i)
    # print(type(args))


def read(a, b):
    values = []
    for i in a:
        values.append(b[i])
    return values


if __name__ == '__main__':
    pass
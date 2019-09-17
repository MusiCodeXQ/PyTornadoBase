from src.util.schema_util import ProTypes
import datetime

temp="""from src.util.schema_map import ProTypes
class {}(BaseData):
    def __init__(self):
        super().__init__()
{}
"""

def get_temp():
    return temp

class Data():
    def __init__(self, name,value_type):
        self.name=name
        self.value_type=value_type
        self.need=False
    
    def __eq__(self, value):
        return self.name==value

    
class BaseData():
    def __init__(self):
        self.data=[]

    def sql_columns(self,data:list,inst:dict=None):
        sql = ''
        if inst is not None:
            data=[d for d in data if d in inst.keys()]

        for i in range(0, len(data)):
            if i == len(data) - 1:
                sql += data[i].name
            else:
                sql += data[i].name + ','
        return sql

    # def sql_columns_require(self,data:list,inst:dict=None):
    #     pass
    def sql_mix_data_json(data:list,inst:dict):
        return [d for d in data if d in inst.keys()]
        
    def sql_placeholder(self,data:list,start=1,inst:dict=None):
        sql=''
        if inst is not None:
            data=[d for d in data if d in inst.keys()]
        for i in range(start, len(data)+start):
            if i == len(data)+start-1  :
                sql += "${}".format(i)
            else:
                sql += "${},".format(i)
        return sql
    
    def sql_update(self,data:list,start:int):
        sql=''
        for i in range(start, len(data)+start):
            if i == len(data)+start-1  :
                sql += "{}=${}".format(data[i-start].name,i)
            else:
                sql += "{}=${},".format(data[i-start].name,i)
        return sql

    def sql_args(self,inst:dict,data_list:list):
        values = []
        for data in data_list:
            tp = data.value_type
            v = None
            value=inst[data.name]
            if tp == ProTypes.STRING:
                v = value
            elif tp == ProTypes.NUMBER:
                v = value
            elif tp == ProTypes.BOOLEAN:
                v = value
            elif tp == ProTypes.INTEGER:
                v = value
            elif tp == ProTypes.DATATIME:
                v = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S');
            else:
                v = value
            values.append(v)
        return tuple(values)


    def add(self,name,value_type,need=False):
        self.data.append(Data(name,value_type))
        return self.data

    def set_need(self,name,need=False):
        self.data[self.data.index(name)].need=need

    def get_register(self):
        data=self.data.copy()
        return data
    
    def get_selector(self):
        data=self.data.copy()
        
        return data

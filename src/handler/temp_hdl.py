from src.util import schema_map, db_util,http_util,data_util
from src.com.request_com import app
from tornado.web import RequestHandler
from html.parser import HTMLParser


@app.route('/api/temp')
class TempHandler(RequestHandler):

    async def get(self):
        class_name = "Course"
        table_name = 'course'
        #self.add('money',ProTypes.FLOAT)
        adds=''

        for row in await db_util.db_fetch("""select column_name,data_type from information_schema.columns
                                               where table_schema='public' and table_name=$1;""", table_name):
            name=row['column_name']
            # print(row)
            item = "        self.add('{}',{})\n"
            tp = "ProTypes.STRING"
            if row['data_type'] == 'integer':
                tp = "ProTypes.INTEGER"
            elif row['data_type'] == 'timestamp without time zone':
                tp = "ProTypes.DATATIME"
            elif row['data_type'] == 'double precision':
                tp = "ProTypes.FLOAT"
            elif row['data_type']=='boolean':
                tp="ProTypes.BOOLEAN"
            else :
                tp = "ProTypes.STRING"
            adds+=item.format(name,tp)
        temp = data_util.get_temp().format(class_name, adds).replace('\n','<br>').replace(' ','&nbsp')
        self.write(temp)

    async def post(self):
        schema=schema_map.get_default_sc()
        async def fun(inst:dict):
            print(inst)
            print(inst.keys())
            for key in inst:
                print(key)
                print(type(inst[key]))
            pass
        await http_util.check(self,schema,fun)
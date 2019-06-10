from tornado.web import RequestHandler
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import random

# 短信应用 SDK AppID
appid = 1400009099  # SDK AppID 以1400开头

# 短信应用 SDK AppKey
appkey = "9ff91d87c2cd7cd0ea762f141975d1df37481d48700d70ac37470aefc60f9bad"

class SmsCtl(RequestHandler):
    def __init__(self):
        self.ssender = SmsSingleSender(appid, appkey)

        pass
    async def get(self,phone):
        #getsmscode/13011111111
        sms_type = 0
        r=random.randint(1000,9999)
        result = self.ssender.send(sms_type, 86,phone,
            "%s您的验证码是: %d"%("布金阁",r), extend="", ext="")
        print(result)
        pass
    
    async def post(self,path):
        schema=httputil.getDefaultSchema()
        schema['properties']['user_phone']=httputil.get
        pass

    
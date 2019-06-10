from tornado.web import RequestHandler

from src.myutil import redisutil

class UserCtl(RequestHandler):

    async def get(self):
        if not self.get_secure_cookie("login_session"):
            self.set_secure_cookie("login_session", "myvalue")
            self.write("Your cookie was not set yet!")
        else:
            self.write("Your cookie was set! {} {}".format(self.get_secure_cookie("login_session"),self.get_cookie("login_session")))
        pass
        await redisutil.setStrToRedis('haha','nonono')
        self.write(await redisutil.getStrFromRedis('haha'))

    async def post(self):
        
        pass

class LoginCtl(RequestHandler):
    async def post(self):
        '''登录方法'''
        pass


class SmsCtl(RequestHandler):
    async def get(self,phone_number,a):
        '''发送短信验证码 /sms/13011033542'''
        self.write(phone_number)
        redisutil.setStrToRedis(phone_number+"sms_code",'1234',ex=1)
        pass

    async def post(self):
        '''验证短信验证码'''
        phone=self.get_body_argument('phone')
        code=redisutil.getStrFromRedis(phone+"sms_code")
        self.write(code)
        pass
        
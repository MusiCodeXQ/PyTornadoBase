import tornado.web
import tornado.ioloop

class BaseApplication(tornado.web.Application):

    def route(self, url):
        def register(handler):
            self.add_handlers(".*$", [(url, handler)])  # URL和Handler对应关系添加到路由表中
            return handler

        return register

app = BaseApplication(cookie_secret='yuxiaoqiyuanyuanruilixue',debug=True)  # 创建Tornado路由对象，默认路由表为空

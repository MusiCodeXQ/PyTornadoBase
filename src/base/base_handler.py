from tornado.web import RequestHandler
from src.util.redis_util import get_str_from_redis


class BaseHandler(RequestHandler):
    url_pattern = None

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin",
                        self.request.headers.get("origin", "rui.b612.site"))
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET,DELETE,PUT, OPTIONS')
        self.set_header("Content-Type", "application/json")

    def get_current_user(self):
        if self.get_secure_cookie("login_session"):
            return get_str_from_redis(self.get_secure_cookie("login_session"))
        else:
            return None

    def get_login_url(self):
        return "http://baidu.com"

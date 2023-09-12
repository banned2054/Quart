from sanic import Sanic


class MySanic(Sanic):
    @classmethod
    def _set_startup_method(cls):
        pass

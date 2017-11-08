import bobo
from setting import *
class MyApplication(bobo.Application):
    def __call__(self, environ, start_response):
        for middleware in MIDDLEWARE[0]:
            try:
                middleware(environ)
            except Exception as e:
                print(e)
        return super(MyApplication, self).__call__(environ, start_response)

    def build_response(self, request, method, data):
        response = super(MyApplication, self).build_response(request,method,data)
        for middleware in MIDDLEWARE[1]:
            try:
                middleware(request, response)
            except Exception as e:
                print(e)
        return response

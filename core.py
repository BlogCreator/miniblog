import bobo
from bobo import webob
from setting import *
class MyApplication(bobo.Application):
    def __call__(self, environ, start_response):
        request = webob.Request(environ)
        if request.charset is None:
            # Maybe middleware can be more tricky?
            request.charset = 'utf8'
        for middleware in MIDDLEWARE:
            try:
                next(middleware) #激活协程
                middleware.send(request)
            except Exception as e:
                print(e)

        return self.bobo_response(request, request.path_info, request.method
                                  )(environ, start_response)

    def build_response(self, request, method, data):
        response = super(MyApplication, self).build_response(request,method,data)
        for middleware in MIDDLEWARE:
            try:
                middleware.send(response)
            except Exception as e:
                print(e)
        return response

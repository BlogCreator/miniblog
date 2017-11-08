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
                self.middle_gen = middleware()
                next(self.middle_gen) #激活协程
                self.middle_gen.send(request)
            except StopIteration as e:
                pass

        return self.bobo_response(request, request.path_info, request.method
                                  )(environ, start_response)

    def build_response(self, request, method, data):
        response = super(MyApplication, self).build_response(request,method,data)
        for middleware in MIDDLEWARE:
            try:
                self.middle_gen.send(response)
            except StopIteration as e:
                pass
        return response

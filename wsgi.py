from core import MyApplication
source = ["boboserver:static('/static','static')"]
application = MyApplication(bobo_resources="\n".join(source))

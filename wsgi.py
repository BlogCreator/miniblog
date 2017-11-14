import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core import MyApplication
source = ["boboserver:static('/static','static')"]
application = MyApplication(bobo_resources="\n".join(source))

import sys
import types
import six
import os
cdr = os.path.dirname(os.path.abspath(__file__))+os.path.sep
sys.path.append(cdr)
from core import MyApplication

module = types.ModuleType("miniblog")
module.__file__ = cdr+"blog.py"
six.exec_(compile(open(module.__file__).read(),
                  module.__file__, 'exec'),
          module.__dict__)
sys.modules[module.__name__] = module
source = ["miniblog","boboserver:static('/static','%s')"%(cdr+'static')]
application = MyApplication(bobo_resources="\n".join(source))

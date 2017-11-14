#!/usr/bin/python3

# -*- coding: utf-8 -*-
import bobo
import os
import optparse
import re
import sys
import types
import six
from six.moves import map
from core import MyApplication
import wsgiref.simple_server
_mod_re = re.compile(
    "(^|>) *(\w[a-zA-Z_.]*)(:|$)"
    ).search
def run_server(app, port):
    wsgiref.simple_server.make_server('', port, app).serve_forever()

class Reload:
    """Module-reload middleware

    This middleware can *only* be used with bobo applications.  It
    monitors a list of modules given by a ``modules`` keyword
    parameter and configuration option.  When a module changes, it
    reloads the module and reinitializes the bobo application.

    The Reload class implements the `Paste Deployment
    filter_app_factory protocol
    <http://pythonpaste.org/deploy/#paste-filter-app-factory>`_ and is
    exported as a ``paste.filter_app_factory`` entry point named ``reload``.
    """

    def __init__(self, app, default, modules):
        if not isinstance(app, bobo.Application):
            raise TypeError("Reload can only be used with bobo applications")
        self.app = app

        self.mtimes = mtimes = {}
        for name in modules.split():
            module = sys.modules[name]
            filename = module.__file__
            if filename[-4:] in (".pyc", ".pyo"):
                filename = filename[:-1]
            mtimes[name] = (filename, os.stat(filename).st_mtime)

    def __call__(self, environ, start_response):
        for name, (path, mtime) in sorted(six.iteritems(self.mtimes)):
            if os.stat(path).st_mtime != mtime:
                print('Reloading %s' % name)
                six.exec_(compile(open(path).read(), path, 'exec'),
                          sys.modules[name].__dict__)
                self.app.__init__(self.app.config)
                self.mtimes[name] = path, os.stat(path).st_mtime

        return self.app(environ, start_response)

def server(args=None, Application=bobo.Application):
    """Bobo development server

    The server function implements the bobo development server.

    It is exported as a ``console_script`` entry point named ``bobo``.

    An alternate application can be passed in to run the server with a
    different application implementation as long as application passed
    in subclasses bobo.Application.
    """

    if args is None:
        import logging; logging.basicConfig()
        args = sys.argv[1:]

    usage = "%prog [options] name=value ..."
    if sys.version_info >= (2, 5):
        usage = 'Usage: ' + usage
    parser = optparse.OptionParser(usage)
    parser.add_option(
        '--port', '-p', type='int', dest='port', default=8080,
        help="Specify the port to listen on.")
    parser.add_option(
        '--file', '-f', dest='file', action='append',
        help="Specify a source file to publish.")
    parser.add_option(
        '--resource', '-r', dest='resource', action='append',
        help=("Specify a resource, such as a module or module global,"
              " to publish."))
    parser.add_option(
        '--debug', '-D', action='store_true', dest='debug',
        help="Run the post mortem debugger for uncaught exceptions.")
    parser.add_option(
        '-c', '--configure', dest='configure',
        help="Specify the bobo_configure option.")
    parser.add_option(
        '-s', '--static', dest='static', action='append',
        help=("Specify a route and directory (route=directory)"
              " to serve statically"))

    def error(message):
        sys.stderr.write("Error:\n%s\n\n" % message)
        parser.parse_args(['-h'])

    options, pos = parser.parse_args(args)

    resources = options.resource or []
    mname = 'bobo__main__'
    for path in options.file or ():
        module = types.ModuleType(mname)
        module.__file__ = path
        six.exec_(compile(open(module.__file__).read(),
                          module.__file__, 'exec'),
                  module.__dict__)
        sys.modules[module.__name__] = module
        resources.append(module.__name__)
        mname += '_'

    for s in options.static or ():
        route, path = s.split('=', 1)
        resources.append("boboserver:static(%r,%r)" % (route, path))

    if not resources:
        error("No resources were specified.")

    if [a for a in pos if '=' not in a]:
        error("Positional arguments must be of the form name=value.")
    app_options = dict(a.split('=', 1) for a in pos)

    module_names = [m.group(2)
                    for m in map(_mod_re, resources)
                    if m is not None]

    if options.configure:
        if (':' not in options.configure) and module_names:
            options.configure = module_names[0]+':'+options.configure
        app_options['bobo_configure'] = options.configure
    print('\n'.join(resources))
    app = Application(app_options, bobo_resources='\n'.join(resources))
    app = Reload(app, None, ' '.join(module_names))

    print("Serving %s on port %s..." % (resources, options.port))
    run_server(app, options.port)

if __name__ == '__main__':
    default_args = [sys.argv[0], '-f', 'blog.py', '-s', '/static=static']
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    if len(sys.argv) == 1:
        sys.argv = default_args
    sys.exit(server(Application = MyApplication))

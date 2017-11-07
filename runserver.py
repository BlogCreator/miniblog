#!/usr/bin/python3

# -*- coding: utf-8 -*-
import re
import sys

from boboserver import server

if __name__ == '__main__':
    default_args = [sys.argv[0], '-f', 'blog.py', '-s', '/static=static']
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    if len(sys.argv) == 1:
        sys.argv = default_args
    sys.exit(server())

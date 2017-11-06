import bobo
import tinydb
import datetime
import os
import sys

DB_PATH = '/media/syk/work/work/python/miniblog/database.json'
STATIC = '/media/syk/work/work/python/miniblog/static/'
UPLOAD = '/media/syk/work/work/python/miniblog/static/upload/'
db = tinydb.TinyDB(DB_PATH)
ADMIN_SESSIONID = set()

def authentication(instance,request, decorated):
    if request.cookies['optimizelyEndUserId'] not in ADMIN_SESSIONID:
        resp = bobo.webob.Response()
        resp.body = b'{"success":"false","msg":"authentication fail!"}'
        return resp

@bobo.query('/interface/login')
def login(bobo_request,username,password):
    if username=='admin' and password=='123456':
        if 'optimizelyEndUserId' in bobo_request.cookies:
            print(ADMIN_SESSIONID)
            ADMIN_SESSIONID.add(bobo_request.cookies['optimizelyEndUserId'])
            return '{"success":"true"}'
        else:
            return '{"success":"false","msg":"optimizelyEndUserId is null"}'
    else:
        return '{"success":"false","msg":"username or password error"}'

@bobo.query('/static/:static')
def static(static):
    return open(STATIC+static, 'r').read()

@bobo.query('/interface/get_article')
def get_article(title=None,cls=None):
    query = tinydb.Query()
    result = db.search((query.title==title) & (query.cls==cls))
    for i in result:
        with open(UPLOAD+i['file']) as file:
            i['content'] = file.read()
    resp = {"success":"true","result":result}
    return str(resp)

@bobo.query('/interface/publish_article',check=authentication)
def pulish_article(file=None,title=None,desc=None,cls=None):

    if hasattr(file,'file') and hasattr(file,'filename'):
        with open(UPLOAD + file.filename,'wb') as new_file:
            new_file.write(file.file.read())

    date = {
        "year":datetime.datetime.now().year,
        "month":datetime.datetime.now().month,
        "day":datetime.datetime.now().day,
        "hour":datetime.datetime.now().hour,
        "minute":datetime.datetime.now().minute,
        "second":datetime.datetime.now().second
    }
    query = tinydb.Query()
    if hasattr(file, 'filename'):
        result = db.search((query.title==title) | (query.file==file.filename))
        if len(result)==0:
            db.insert({
                "file":file.filename if hasattr(file,'filename') else None,
                "title":title if title else 'untitled',
                "desc":desc if desc else '...',
                "date":date,
                "cls":cls if cls else 'other'
            })
            return '{"sucess":"true"}'
        else:
            return '{"success":"false","msg":"title or filename already exist!"}'
    return '{"success":"false","msg":"file can not be null"}'

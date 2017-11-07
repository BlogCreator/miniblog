#! /usr/bin/python3
import bobo
import tinydb
import datetime
import os
import sys
import json
from setting import *

def authentication(instance,request, decorated):
    if request.cookies['optimizelyEndUserId'] not in ADMIN_SESSIONID:
        resp = bobo.webob.Response()
        resp.body = b'{"success":"false","msg":"authentication fail!"}'
        return resp

def wrap_article_result(db_result):
    if hasattr(db_result, '__getitem__'):
        for i in db_result:
            with open(UPLOAD+i['file'],'r') as file:
                i['content'] = file.read()


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

@bobo.query('/interface/get_article')
def get_article(title=None,cls=None):
    query = tinydb.Query()
    result = []
    if cls and title:
        result = db.search((query.title==title) & (query.cls==cls))
    else:
        result = db.search((query.title==title) | (query.cls==cls))

    wrap_article_result(result)
    resp = {"success":"true","result":result}
    return json.dumps(resp)

@bobo.query('/interface/get_recent_article')
def get_recent_article(limit=100):
    if limit == '':
        limit = 100
    result = db.all()[:int(limit)]
    result.sort(key=lambda k:k['date'],reverse=True)
    wrap_article_result(result)
    return json.dumps({"success":"true","result":result})

@bobo.query('/interface/get_cls')
def get_cls():
    meta = db.table(name='meta').all()
    try:
        classes = meta[0]['cls']
        return json.dumps({"success":"true","result":classes})
    except Exception as e:
        return '{"success":"false","msg":"you have not create any class"}'

@bobo.query('/interface/create_cls', check=authentication)
def create_cls(cls):
    '''
    meta table only has one json object like {"key":"meta","cls":["note"]}
    '''
    meta = db.table(name='meta')
    if len(meta.all()) == 0:
        meta.insert({"key":"meta","cls":[]})
    origin = meta.all()[0]
    if cls not in origin['cls']:
        origin['cls'].append(cls)
        meta.update(origin,tinydb.Query().key=="meta")
        return '{"success":"true"}'
    else:
        return '{"success":"false","msg":"this class has already exist"}'

@bobo.query('/interface/del_cls', check=authentication)
def del_cls(cls):
    '''
    delete a given class
    '''
    meta = db.table(name='meta')
    origin = meta.all()
    if len(origin) == 0 or cls not in origin[0]['cls']:
        return '{"success":"false","msg":"class not exist"}'
    else:
        origin[0]['cls'].remove(cls)
        meta.update(origin[0],tinydb.Query().key=='meta')
        return '{"success":"true"}'

@bobo.query('/interface/publish_article',check=authentication)
def pulish_article(file=None,title=None,desc=None,cls=None):

    if hasattr(file,'file') and hasattr(file,'filename'):
        with open(UPLOAD + file.filename,'wb') as new_file:
            new_file.write(file.file.read())

    date =  datetime.datetime.now().isoformat()
    query = tinydb.Query()
    if hasattr(file, 'filename'):
        result = db.search((query.title==title) | (query.file==file.filename))
        classes = db.table(name='meta').all()
        if len(classes) == 0 or cls not in classes[0]['cls']:
            return '{"succcess":"false","msg":"the class not exist,please create a classes first"}'
        if len(result)==0:
            db.insert({
                "file":file.filename if hasattr(file,'filename') else None,
                "title":title if title else 'untitled',
                "desc":desc if desc else '...h',
                "date":date,
                "cls":cls if cls else 'other'
            })
            return '{"sucess":"true"}'
        else:
            return '{"success":"false","msg":"title or filename already exist!"}'
    return '{"success":"false","msg":"file can not be null"}'

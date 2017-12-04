#! /usr/bin/python3
# coding=ascii
import setting
from setting import *
import re
import bobo
import tinydb
import datetime
import json
import sqlite3
from md import md
ADMIN_SESSIONID = set()

print(cdr)
print(UPLOAD)

def authentication(instance,request, decorated):
    if request.cookies['session_id'] not in ADMIN_SESSIONID:
        resp = bobo.webob.Response()
        resp.body = b'{"success":"false","msg":"authentication fail!"}'
        return resp

def wrap_article_result(db_result,convert=md.convert):
    if hasattr(db_result, '__getitem__'):
        for i in db_result:
            d = {}
            d.update(i)
            d['pic']='static/upload/pic/'+d['pic']
            if len(db.table('meta').all())!=0 and 'info' in db.table('meta').all()[0] and \
                            'name' in db.table('meta').all()[0]['info']:
                d['author'] = db.table('meta').all()[0]['info']['name']
            try:
                with open(UPLOAD+i['file'],'r', encoding='utf-8') as file:
                    d['content'] = "<link rel=stylesheet href='/static/css3/mdstyle.css'></link>"+convert(file.read())
            except:
                d['content'] = "an error was occurred while reading the file"
            yield d

@bobo.query('/')
def index(bobo_request):
    t = db.table("access")
    t.insert({"date":datetime.datetime.now().timetuple()[:3],"ip":bobo_request.remote_addr})
    return bobo.redirect(url='/static/main/main1.html')


@bobo.query('/interface/login')
def login(bobo_request,username,password):
    meta = db.table("meta").all()
    if len(meta) != 0 and \
        'login' in meta[0] and \
        username==meta[0]['login']['username'] and \
        password==meta[0]['login']['password'] :
        if 'session_id' in bobo_request.cookies:
            global ADMIN_SESSIONID
            ADMIN_SESSIONID.add(bobo_request.cookies['session_id'])
            return '{"success":"true"}'
        else:
            return '{"success":"false","msg":"session_id is null"}'
    else:
        if username=='admin' and password=='123456':
            if 'session_id' in bobo_request.cookies:
                global ADMIN_SESSIONID
                ADMIN_SESSIONID.add(bobo_request.cookies['session_id'])
                return '{"success":"true","msg":"please change your authentication!!!!!!"}'
            else:
                return '{"success":"false","msg":"session_id is null"}'
        return '{"success":"false","msg":"username or password error"}'

@bobo.query('/interface/get_article')
def get_article(title=None,cls=None):
    blog = []
    if title:
        blog = sql_db.search("blog",('title',title))
    elif cls:
        blog = sql_db.search("blog",('cls',cls))
    r = []
    for i in wrap_article_result(blog):
        d = {}
        d.update(i)
        r.append(d)
    resp = {"success":"true","result":r}
    return json.dumps(resp)

@bobo.query('/interface/get_recent_article')
def get_recent_article(limit=100):
    if limit == '':
        limit = 100
    blog = sql_db.all("blog")[:int(limit)]
    blog.sort(key=lambda k:k['date'],reverse=True)
    r = []
    for i in wrap_article_result(blog):
        r.append(i)
    return json.dumps({"success":"true","result":r})

@bobo.query('/interface/get_click_article')
def get_click_article(limit=5):
    if limit=='':limit=5
    click = sql_db.all("click")[:limit]
    click.sort(key=lambda it:it['number'],reverse=True)
    r = []
    for i in click:
        d = {}
        d.update(i)
        r.append(d)
    return json.dumps({"success":"true","result":r})
@bobo.query('/interface/get_cls')
def get_cls():
    r = []
    try:
        for i in sql_db.all("cls "):
            r.append(i['name'])
    except:
        return json.dumps({"success":"false"})
    return json.dumps({"success":"true","result":r})


@bobo.query('/interface/create_cls', check=authentication)
def create_cls(cls):
    """
    meta table only has one json object like {"key":"meta","cls":["note"]}
    """
    try:
        sql_db.insert("cls",(cls,))
    except:
        return json.dumps({"success":"false"})
    return json.dumps({"success":"true"})

@bobo.query('/interface/del_cls', check=authentication)
def del_cls(cls):
    """
    delete a given class
    """
    if len(sql_db.search("blog",("cls",cls)))!=0:
        return json.dumps({"success":"false","msg":"this class is not null"})
    else: sql_db.delete("cls",("name",cls))
    return json.jumps({"success":"true"})

@bobo.query('/interface/publish_article',check=authentication)
def pulish_article(file=None,title=None,desc=None,cls=None,pic=None):

    if hasattr(file,'file') and hasattr(file,'filename'):
        print(file.filename)
        with open(UPLOAD + file.filename,'wb') as new_file:
            new_file.write(file.file.read())
    if hasattr(pic,'file') and hasattr(pic,'filename'):
        with open(UPLOAD+'pic/'+pic.filename,'wb') as new_pic:
            new_pic.write(pic.file.read())

    if hasattr(file, 'filename'):
        try:
            sql_db.insert(
                "blog",
                (title,file.filename,pic.filename,desc,datetime.datetime.now(),cls)
            )
        except sqlite3.OperationalError:
            return json.dumps({"success":"false","msg":"database write fail!"})
        return json.dumps({"success":"true"})
    else:
        return json.dumps({"success":"false","msg":"filename is necessary"})

@bobo.query('/interface/comment')
def comment(bobo_request, title=None,content=None, name="anonymous"):
    if not content or not title:
        return json.dumps({"success":"false","msg":"content and title can not be null"})
    sql_db.insert(
        'comment',
        (title,name,datetime.datetime.now(),content,bobo_request.remote_addr))
    return json.dumps({"success":"true"})

@bobo.query('/interface/get_comment')
def get_comment(title=None, limit=None):
    if not title:
        return json.dumps({"success":"false","msg":"we must have a title to get the comments"})
    r = sql_db.search('comment',('article_title',title))
    r = r[:int(limit)] if limit else r
    result = []
    for i in r:
        d = {}
        d.update(i)
        result.append(d)
    return json.dumps({"success":"true","result":result})

@bobo.query('/interface/get_access')
def get_access(start=None, end=None):
    if not start and not end:
        num = len(db.table(name='access').all())
        return json.dumps({"success":"true","result":num})
    elif not end and start:
        num = len(db.table(name='access')
            .search(tinydb.Query().date==[int(i) for i in start.split('-')]))
        return json.dumps({"success":"true","result":num})
    elif end and start:
        num = len(db.table(name='access').search(
            (tinydb.Query().date>=[int(i) for i in start.split('-')]) &
            (tinydb.Query().date<=[int(i) for i in end.split('-')])
        ))
        return json.dumps({"success":"true","result":num})
    else:
        return json.dumps({"success":"false","msg":"date is not illege"})

@bobo.query('/interface/click')
def click(title=None):
    db_r = sql_db.search('click',('blog_title',title))
    if title:
        if len(db_r) == 0:
            sql_db.insert('click',(title,1))
        else:
            sql_db.update('click',('number',),(db_r[0]['number']+1,),('blog_title',title))
        return json.dumps({"success":"true"})
    else:
        return json.dumps({"success":"false","msg":"title can not be null"})

@bobo.query('/interface/set_info',check=authentication)
def set_info(name='null', email='null', motto='null',birthday='null',school="null"):
    t = db.table('meta')
    meta = t.all()
    if len(meta)!=0:
        meta[0]["info"] = {"name":name,"email":email,
                           "motoo":motto,"birthday":birthday,
                           "school":school}
        t.update(meta[0],tinydb.Query().key == 'meta')
    else:
        t.insert({"key":"meta","info":{"name":name,"email":email,"motoo":motto}})

    return json.dumps({"success":"true"})

@bobo.query('/interface/info')
def info():
    t = db.table('meta')
    meta = t.all()
    if len(meta)==0 or 'info' not in meta[0].keys():
        return json.dumps({"success":"false","msg":"the information is null"})
    else:
        return json.dumps({"success":"true","result":meta[0]["info"]})

@bobo.query('/interface/register',check=authentication)
def register(username,password):
    t = db.table('meta')
    if len(t.all()) == 0:
        t.insert({"key":"meta","login":{"username":username,"password":password}})
    else:
        buf = t.all()[0]
        buf['login'] = {"username":username,"password":password}
        t.update(buf,tinydb.Query().key == 'meta')
    return json.dumps({"success":"true"})
@bobo.query('/interface/article/:title')
def show_article(title):
    article = sql_db.search('blog',('title',title))
    if len(article) == 0:
        return bobo.redirect('/')
    else:
        html = ''
        with open(cdr+'/template/show.html','r',encoding='utf-8') as show:
            html = show.read()
            m = re.search('{article_my}',html)
            html = html[:m.span()[0]] + next(wrap_article_result(article))['content']+\
                html[m.span()[1]:]
        return html

#! /usr/bin/python3
# coding=ascii
import setting
from setting import *
import re
import bobo
import tinydb
import datetime
import json
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
            i['pic']='static/upload/pic/'+i['pic'].lstrip(UPLOAD)
            try:
                with open(UPLOAD+i['file'],'r', encoding='utf-8') as file:
                    i['content'] = "<link rel=stylesheet href='/static/css3/mdstyle.css'></link>"+convert(file.read())
            except:
                i['content'] = "an error was occurred while reading the file"

@bobo.query('/')
def index(bobo_request):
    t = db.table("access")
    t.insert({"date":datetime.datetime.now().timetuple()[:3],"ip":bobo_request.remote_addr})
    return bobo.redirect(url='/static/main/main1.html')


@bobo.query('/interface/login')
def login(bobo_request,username,password):
    meta = db.table("meta").all()
    if len(meta) != 0 and \
        username==meta[0]['login']['username'] and \
        password==meta[0]['login']['password'] :
        if 'session_id' in bobo_request.cookies:
            global ADMIN_SESSIONID
            ADMIN_SESSIONID.add(bobo_request.cookies['session_id'])
            return '{"success":"true"}'
        else:
            return '{"success":"false","msg":"session_id is null"}'
    else:
        if len(meta)==0 and username=='admin' and password=='123456':
            if 'session_id' in bobo_request.cookies:
                global ADMIN_SESSIONID
                ADMIN_SESSIONID.add(bobo_request.cookies['session_id'])
                return '{"success":"true","msg":"please change your authentication!!!!!!"}'
            else:
                return '{"success":"false","msg":"session_id is null"}'
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

@bobo.query('/interface/get_click_article')
def get_click_article(limit=5):
    if limit == '': limit = 5
    r = db.table("click").all()
    r.sort(key=lambda d:d['click'],reverse=True)
    r = r[:int(limit)]
    return json.dumps({"success":"true","result":r})
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
    elif 'cls' not in meta.all()[0]:
        meta.update({'cls':[]},tinydb.Query().key=='meta')

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
def pulish_article(file=None,title=None,desc=None,cls=None,pic=None):

    if hasattr(file,'file') and hasattr(file,'filename'):
        print(file.filename)
        with open(UPLOAD + file.filename,'wb') as new_file:
            new_file.write(file.file.read())
    if hasattr(pic,'file') and hasattr(pic,'filename'):
        with open(UPLOAD+'pic/'+pic.filename,'wb') as new_pic:
            new_pic.write(pic.file.read())

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
                "desc":desc if desc else '...',
                "date":datetime.datetime.now().timetuple(),
                "cls":cls if cls else 'other',
                "pic":UPLOAD+'pic/'+pic.filename if (pic is not None) and hasattr(pic,'filename') else UPLOAD+"pic/default.jpg",
            })
            return '{"sucess":"true"}'
        else:
            return '{"success":"false","msg":"title or filename already exist!"}'
    return '{"success":"false","msg":"file can not be null"}'

@bobo.query('/interface/comment')
def comment(bobo_request, title=None,content=None, name="anonymous"):
    if not content or not title:
        return json.dumps({"success":"false","msg":"content and title can not be null"})
    commentdb = db.table(name='comment')
    commentdb.insert({
        "article_title":title,
        "ip":bobo_request.remote_addr,
        "name":name,
        "content":content,
        "date":datetime.datetime.now().timetuple()
    })
    return json.dumps({"success":"true"})

@bobo.query('/interface/get_comment')
def get_comment(title=None, limit=None):
    if not title:
        return json.dumps({"success":"false","msg":"we must have a title to get the comments"})
    commentdb = db.table("comment")
    result = commentdb.search(tinydb.Query().article_title == title)
    print(result)
    result = result[:int(limit)] if limit else result
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
    if title and len(db.search(tinydb.Query().title==title))!=0:
        t = db.table(name="click")
        r = t.search(tinydb.Query().title == title)
        if len(r) == 0:
            t.insert({"title":title,"click":1})
        else:
            t.update({"click":r[0]['click']+1}, tinydb.Query().title==title)
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
    article = db.search(tinydb.Query().title==title)
    if len(article) == 0:
        return bobo.redirect('/')
    else:
        html = ''
        with open(cdr+'/template/show.html','r',encoding='utf-8') as show:
            html = show.read()
            m = re.search('{article_my}',html)
            wrap_article_result(article)
            html = html[:m.span()[0]] + article[0]['content']+\
                html[m.span()[1]:]
        return html

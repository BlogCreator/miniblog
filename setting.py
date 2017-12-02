import tinydb
import middleware
import os
from database import query
cdr = os.path.dirname(os.path.abspath(__file__))
DB_PATH = cdr +'/database.json'
STATIC = cdr +'/static/'
UPLOAD = cdr +'/static/upload/'
db = tinydb.TinyDB(DB_PATH)
MIDDLEWARE=[
    middleware.session_id,
]
os.umask(000)
if not os.path.exists(cdr + '/static/upload'):
    os.mkdir(cdr + '/static/upload')
    os.mkdir(cdr + '/static/upload/pic')

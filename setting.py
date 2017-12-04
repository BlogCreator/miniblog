import tinydb
import middleware
import os
from database import query
cdr = os.path.dirname(os.path.abspath(__file__))
SQLDB_PATH = cdr +'/database/database.db'
DB_PATH = cdr + '/database.json'
STATIC = cdr +'/static/'
UPLOAD = cdr +'/static/upload/'

db = tinydb.TinyDB(DB_PATH)
sql_db = query.DB(SQLDB_PATH)
MIDDLEWARE=[
    middleware.session_id,
]
os.umask(000)
if not os.path.exists(cdr + '/static/upload'):
    os.mkdir(cdr + '/static/upload')
    os.mkdir(cdr + '/static/upload/pic')

import tinydb
import middleware
import os
from database import make_db_file
cdr = os.path.dirname(os.path.abspath(__file__))
SQLDB_PATH = cdr +'/database/database.db'
DB_PATH = cdr + '/database.json'
STATIC = cdr +'/static/'
UPLOAD = cdr +'/static/upload/'
MIDDLEWARE=[
    middleware.session_id,
]

db = tinydb.TinyDB(DB_PATH)
os.umask(000)
if not os.path.exists(cdr + '/static/upload'):
    os.mkdir(cdr + '/static/upload')
    os.mkdir(cdr + '/static/upload/pic')
make_db_file.create_database()

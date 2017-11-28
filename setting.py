import tinydb
import middleware
import os
cdr = os.path.dirname(os.path.abspath(__file__))
DB_PATH = cdr +'/database.json'
STATIC = cdr +'/static/'
UPLOAD = cdr +'/static/upload/'
db = tinydb.TinyDB(DB_PATH)
MIDDLEWARE=[
    middleware.session_id,
]

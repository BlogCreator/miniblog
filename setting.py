import tinydb
import middleware
DB_PATH = 'database.json'
STATIC = 'static/'
UPLOAD = 'static/upload/'
db = tinydb.TinyDB(DB_PATH)


MIDDLEWARE=[
    middleware.session_id,
]

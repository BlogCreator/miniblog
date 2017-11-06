import tinydb
DB_PATH = 'database.json'
STATIC = 'static/'
UPLOAD = 'static/upload/'
db = tinydb.TinyDB(DB_PATH)
ADMIN_SESSIONID = set()

import setting
import tinydb
import json
from datetime import datetime
import uuid
def access_record(environ):
    setting.db.table(name="access").insert({
        "remote_addr":environ['REMOTE_ADDR'],
        "time":datetime.now().timetuple(),
        "date":datetime.now().timetuple()[:3]
    })
def session_id(environ):
    if 'session_id' in request.cookies:
        pass
    else:
        response.set_cookie('session_id', str(uuid.uuid1()))

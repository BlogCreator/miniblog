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
def session_id():
    request = yield
    if 'session_id' in request.cookies:
        return
    request.cookies['session_id'] = uuid.uuid1()
    response = yield
    response.set_cookies(request.cookies['session_id'])

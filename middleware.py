from datetime import datetime
import uuid
def access_record(environ):
    from setting import db
    db.table(name="access").insert({
        "remote_addr":environ['REMOTE_ADDR'],
        "time":datetime.now().timetuple(),
        "date":datetime.now().timetuple()[:3]
    })
def session_id():
    request = yield
    if 'session_id' in request.cookies:
        print("already has session id")
        return
    request.cookies['session_id'] = str(uuid.uuid1())
    response = yield
    response.set_cookie("session_id",request.cookies['session_id'])

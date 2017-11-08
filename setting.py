import tinydb
import middleware
DB_PATH = 'database.json'
STATIC = 'static/'
UPLOAD = 'static/upload/'
db = tinydb.TinyDB(DB_PATH)


MIDDLEWARE=[
    # 前处理器，在请求到来时执行，控制权未转交给控制器前被调用
    [

    ],
    # 后处理器, 在控制器执行完之后，完整相应未生成之前被调用
    [
        #middleware.access_record,

    ],
    # 全局处理器，一个协程，在请求到来时执行到yield语句处，响应之前会将request传入，并执行完yield后面的语句
    [
        middleware.session_id
    ]
]

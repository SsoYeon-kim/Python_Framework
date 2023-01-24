import pymongo

MONGO_HOST = 'localhost'
MONGO_CONN = pymongo.MongoClient('mongodb://%s' % (MONGO_HOST))

# collection 가져오기
def conn_mongodb():
    try:
        MONGO_CONN.admin.command('ismaster')
        blog_ab = MONGO_CONN.blog_session_db.blog_ab
    # connection 오류가 난 경우 mongodb 재접속
    except:
        MONGO_CONN = pymongo.MongoClient('mongodb://%s' % (MONGO_HOST))
        blog_ab = MONGO_CONN.blog_session_db.blog_ab
    return blog_ab
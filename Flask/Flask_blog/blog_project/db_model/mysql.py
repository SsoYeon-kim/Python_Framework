import pymysql

# 여기는 connection만 할거야

MYSQL_HOST = 'localhost'
MYSQL_CONN = pymysql.connect(
    host=MYSQL_HOST,
    port=3306,
    user='sso',
    passwd='thdus1477!',
    db='blog_db',
    charset='utf8'
)

# connection
# return한 객체는 control에서 사용
def conn_mysqldb():
    # connection이 끊어졌는지 확인 (다시 연결)
    if not MYSQL_CONN.open:
        MYSQL_CONN.ping(reconnect=True)
    return MYSQL_CONN
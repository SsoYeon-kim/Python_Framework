from db_model.mongodb import conn_mongodb
from datetime import datetime


class BlogSession():
    blog_page = {'A': 'A_page.html', 'B': 'B_page.html'}
    session_count = 0

    # 접속 정보 몽고db 저장
    @staticmethod
    def save_session_info(session_ip, user_email, webpage_name):
        now = datetime.now()
        now_time = now.strftime("%d/%m/%Y %H:%M:%S")  # https://strftime.org/

        mongo_db = conn_mongodb()
        mongo_db.insert_one({
            'session_ip': session_ip,
            'user_email': user_email,
            'page': webpage_name,
            'access_time': now_time
        })

    # 50% 확률로 보여줄 페이지 정의 (접속할 때마다 한 번은 A, 한 번은 B 보여주기)
    @staticmethod
    def get_blog_page(blog_id=None):
        if blog_id == None:
            if BlogSession.session_count == 0:
                BlogSession.session_count = 1
                return BlogSession.blog_page['A']
            else:
                BlogSession.session_count = 0
                return BlogSession.blog_page['B']
        else:
            return BlogSession.blog_page[blog_id]

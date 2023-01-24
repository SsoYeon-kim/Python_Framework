from flask import Flask, Blueprint, request, session, render_template, make_response, jsonify, redirect, url_for
from flask_login import login_user, current_user, logout_user
from blog_control.user_mgmt import User
from blog_control.session_mgmt import BlogSession
import datetime

# 여기서는 라우팅 처리를 함
# 이메일을 넣고 구독을 누르면 해당 데이터를 받아서 flask_login을 사용해 세션 정보를 웹 페이지에 보내주고
# 이메일 주소를 등록이 된 상태로 페이지가 보여지게끔 구현

# redirect : 리턴을 다른 라우팅 경로로 변경 (전체 라우팅 경로를 넣어줘야 됨)
    # return redirect('/blog/test_blog')
# url _for : 라우팅 경로 리턴 (블루 프린트명, 함수 명)
    # return redirect(url_for('blog.test_blog'))

blog_abtest = Blueprint('blog', __name__)


# 구독 버튼 클릭 시
@blog_abtest.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'GET':
        print('set_email', request.headers)
        print(request.args.get('user_email'))
        return redirect(url_for('blog.start_blog'))
    else:
        print('set_email', request.headers)
        print('set_email', request.form['user_email'])
        print('set_email', request.form['blog_id'])
        # mysql 등록 (이를 기반으로 flask server에서는 세션 정보를 만들고 웹 브라우저로 http response를 보낼 때 set cookie로 세션 정보를 넣어서 보내야됨)
        user = User.create(request.form['user_email'], request.form['blog_id'])
        # 세션 정보 만들기
        # remeber는 웹 브라우저가 꺼져서 세션 정보 기억
        login_user(user, remember=True, duration=datetime.timedelta(days=365))

        return redirect(url_for('blog.start_blog'))

        # Content-Type: application/x-www-form-urlencoded (form 데이터)
        # 이 경우에는 request.get_json()으로 body 부분을 가져올 수 없음
        # get_json은 content-type이 application/json인 경우임

@blog_abtest.route('/logout')
def logout():
    # mysql에서 지우기
    User.delete(current_user.id)
    # 세션 지우기
    logout_user()
    return redirect(url_for('blog.start_blog'))

# 이메일 구독 후 다시 사용자가 test_blog로 접속을 했을 때
# 세션 정보가 같이 들어오게 되고 여기서 flask_login이 id를 가져올 수 있어 (세션 정보에서 id 추출)
# 이미 구독이 되어 있다면 user_email을 변수값을 넣어서 넘겨줘야돼
@blog_abtest.route('/start_blog')
def start_blog():
    # 로그인이 된 사용자 (@login_manager.user_loader를 호출함)
    # current_user는 User 객체임 (user_mgmt.py)
    # 이게 템플릿을 넘어가서 html에 user_emaill로 넘어가
    if current_user.is_authenticated:
        webpage_name = BlogSession.get_blog_page(current_user.blog_id)
        # 구독한 사용자가 얼마나 접속하는지 알기위한 로그
        BlogSession.save_session_info(session['client_id'], current_user.user_email, webpage_name)
        return render_template(webpage_name, user_email=current_user.user_email)
    else:
        webpage_name = BlogSession.get_blog_page()
        # 전체 사용자 접속 로그
        BlogSession.save_session_info(session['client_id'], 'anonynous', webpage_name)
        return render_template(webpage_name)
from flask import Flask, jsonify, session, request, render_template, make_response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
from blog_view import blog
from blog_control.user_mgmt import User
import os

# https만을 지원하는 기능을 http에서 테스트할 때 필요한 설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.secret_key = 'sso_server'

app.register_blueprint(blog.blog_abtest, url_prefix='/blog')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'

# user_id는 flask_login이 http request에서 id를 추출해서 가져옴
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)

# 모든 요청에 대한 client ip
@app.before_request
def app_before_request():
    if 'client_id' not in session:
        session['client_id'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
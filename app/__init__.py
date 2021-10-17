from flask import Flask, redirect
# 20211002 KYB add flask_restful 추가
from flask_restful import Api
# 20210911 KYB add 플라스크 로그인 추가
from flask_login import LoginManager

# 20210912 KYB add 사용자 객체 추가
from app.model.common.model_user import User

from app.config import DB


app = Flask(__name__)
# 20211002 KYB add api 객체 추가
api = Api(app)

# 20210911 KYB add 로그인 매니저 추가
app.secret_key = 'keona_we'

login_manager = LoginManager()
login_manager.init_app(app)


# 20210912 KYB add 로그인 객체 생성
# 20210912 KYB exp 플라스크가 로그인 객체 생성하도록 설정
# 20210912 KYB exp 로그인 매니저 연결 시 선언 필수
@login_manager.user_loader
def user_loader(user_id):
    user_info = User.get_user_info(user_id)

    user_id = user_info['data'][0]['USER_ID']
    user_name = user_info['data'][0]['USER_NAME']

    login_info = User(user_id=user_id, user_name=user_name)

    return login_info


# 20210912 KYB add 로그인이 되어 있지 않은 사용자일 경우 해당 경로로 이동
@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0')


# view
from app.view.default.common import main
# 20210911 KYB add 로그인 관련 view 추가
from app.view.default.common import login
# 20210913 KYB add 업무 관련 view 추가
from app.view.default.work import work
# 20211011 KYB add 보고서 관련 view 추가
from app.view.default.work import work_report

# api
from app.view.API.work import api_work
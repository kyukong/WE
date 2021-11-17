from flask import Flask, redirect, g
from flask_restful import Api
from flask_login import LoginManager

from app.model.common.model_db_connect import commit
from app.model.common.model_user import User

from app.config import DB


app = Flask(__name__)
api = Api(app)

app.secret_key = 'keona_we'

login_manager = LoginManager()
login_manager.init_app(app)


# 플라스크가 로그인 객체 생성하도록 설정
# 로그인 매니저 연결 시 선언 필수
@login_manager.user_loader
def user_loader(user_id):
    user_info = User.get_user_info(user_id)

    user_id = user_info['data'][0]['USER_ID']
    user_name = user_info['data'][0]['USER_NAME']

    login_info = User(user_id=user_id, user_name=user_name)

    return login_info


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/")


@app.after_request
def after_request(response):
    if hasattr(g, 'conn'):
        commit()
        conn = getattr(g, 'conn')
        conn.close()
        delattr(g, 'conn')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')


# view
from app.view.default.common import main
from app.view.default.common import login
from app.view.default.work import work
from app.view.default.work import work_report

# api
from app.view.API.work import api_work
from app.view.API.work import api_workReport
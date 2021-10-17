from flask import render_template, redirect, request, g
from app import app
# 20210911 KYB add 플라스크 로그인 추가
from flask_login import login_user, logout_user, current_user

from app.model.common.model_user import User


@app.route('/')
def root():
    # 20210918 KYB mod 기본 경로로 접속했을 경우 로그인 여부 판단하여 표출
    # return redirect('/login')
    if current_user.is_authenticated:
        return redirect('/main')
    else:
        return redirect('/login')


@app.route('/login')
def login():
    return render_template('common/template_login.html')


# 20210911 KYB add 로그인 실행
@app.route('/login/get_info', methods=['GET', 'POST'])
def login_get_info():
    user_id = request.form.get('userID')
    user_pw = request.form.get('userPW')

    if user_id is None or user_pw is None:
        return redirect('/relogin')

    user_info = User.get_user_info(user_id, user_pw)

    if user_info['result'] != 'fail' and user_info['count'] != 0:
        # 20210912 KYB 로그인 정보 플라스크 세션에 저장
        user_id = user_info['data'][0]['USER_ID']
        user_name = user_info['data'][0]['USER_NAME']
        login_info = User(user_id=user_id, user_name=user_name)
        login_user(login_info)

        # 20211004 KYB add 사용자 ID 정보 g 에 저장
        g.user = current_user

        return redirect('/main')
    else:
        return redirect('/relogin')


# 20210911 KYB add 로그인 실패 시 재로그인
@app.route('/relogin')
def relogin():
    login_result_text = "로그인에 실패했습니다. 다시 시도해주세요."
    
    return render_template('common/template_login.html', login_result_text=login_result_text)


# 20210912 KYB add 로그아웃
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
from flask import render_template
from app import app
# 20210912 KYB add 플라스크 로그인 추가
from flask_login import login_required

from app.view.default.common.basic import get_menu_list



@app.route("/main")
@login_required
def main():
    menu_list = get_menu_list()
    
    return render_template("common/layout/layout_basic.html", 
            menu_list=menu_list)

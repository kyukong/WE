from flask import g
# 20210911 KYB add 플라스크 로그인 관련 추가
from flask_login import UserMixin

from app.config import DB

from app.model.common.model_db_connect import select, insert, update, delete

class User(UserMixin):
    
    # 20210911 KYB add 초기값 설정
    def __init__(self, user_id):
        self.user_id = user_id
    
    # 20210911 KYB add 사용자 아이디 조회
    def get_id(self):
        return str(self.user_id)

    # 20210911 KYB add 사용자 정보 조회
    @staticmethod
    def get_user_info(user_id, user_pw=None):
        result = dict()

        try:
            sql = ""
            sql += f"SELECT USER_ID, USER_NAME, `PASSWORD`, COMPANY_CODE, DEPARTMENT_CODE, POSITION_CODE, AUTH_CODE, "
            sql += f"REGISTER_DATETIME, LOGIN_DATETIME, LASTWEEK_REPORT_ID, THISWEEK_REPORT_ID, "
            sql += f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME "
            sql += f"FROM tn_user_info "
            if user_pw:
                sql += f"WHERE USER_ID = '{user_id}' AND `PASSWORD` = '{user_pw}'; "
            else:
                sql += f"WHERE USER_ID = '{user_id}'; "

            result = select(sql)
            
        except ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result
    
    # def ins_menu_info(self, menu_info):
    #     sql = ""
    #     sql += f"INSERT INTO tc_menu_info (HIGHCODE, `CODE`, MENU_NAME, MENU_LEVEL, `PATH`, DISPLAY_FLAG) "
    #     sql += f"VALUES "
    #     sql += f"('{menu_info['HIGHCODE']}', '{menu_info['CODE']}', '{menu_info['MENU_NAME']}', "
    #     sql += f"{menu_info['MENU_LEVEL']}, '{menu_info['PATH']}', '{menu_info['DISPLAY_FLAG']}'), "

    #     result = insert(sql)

    #     return result
    
    # def upd_menu_info(self, menu_info):
    #     sql = ""
    #     sql += f"UPDATE tc_menu_info "
    #     sql += f"SET MENU_NAME = '{menu_info['MENU_NAME']}' "
    #     sql += f"WHERE CODE = '{menu_info['CODE']}'; "

    #     result = update(sql)

    #     return result

    # def del_menu_info(self, menu_info):
    #     sql = ""
    #     sql += f"DELETE FROM  tc_menu_info "
    #     sql += f"WHERE CODE = '{menu_info['CODE']}'; "

    #     result = delete(sql)

    #     return result

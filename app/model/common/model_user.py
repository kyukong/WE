from flask import g
# 20210911 KYB add 플라스크 로그인 관련 추가
from flask_login import UserMixin

from app.config import DB

from app.model.common.model_db_connect import select, insert, update, delete


class User(UserMixin):
    
    # 초기값 설정
    def __init__(self, user_id=None, user_name=None):
        self.user_id = user_id
        self.user_name = user_name
    
    # 사용자 아이디 조회
    def get_id(self):
        return str(self.user_id)

    # 사용자 정보 조회
    @staticmethod
    def get_user_info(user_id: str, user_pw: str = "") -> dict:
        result: dict = dict()

        try:
            sql: str = f"SELECT USER_ID, IFNULL(USER_NAME, '') AS USER_NAME, " \
                       f"IFNULL(`PASSWORD`, '') AS `PASSWORD`, " \
                       f"IFNULL(COMPANY_CODE, '') AS COMPANY_CODE, " \
                       f"IFNULL((SELECT CODE_NAME " \
                       f"FROM tc_code_info WHERE `CODE` = COMPANY_CODE), '') AS COMPANY_CODE_NAME, " \
                       f"IFNULL(DEPARTMENT_CODE, '') AS DEPARTMENT_CODE, " \
                       f"IFNULL((SELECT CODE_NAME " \
                       f"FROM tc_code_info WHERE `CODE` = DEPARTMENT_CODE), '') AS DEPARTMENT_CODE_NAME, " \
                       f"IFNULL(POSITION_CODE, '') AS POSITION_CODE, " \
                       f"IFNULL((SELECT CODE_NAME " \
                       f"FROM tc_code_info WHERE `CODE` = POSITION_CODE), '') AS POSITION_CODE_NAME, " \
                       f"IFNULL(AUTH_CODE, '') AS AUTH_CODE, " \
                       f"IFNULL((SELECT CODE_NAME " \
                       f"FROM tc_code_info WHERE `CODE` = AUTH_CODE), '') AS POSITION_CODE_NAME, " \
                       f"IFNULL(PAYMENT_USER_ID, '') AS PAYMENT_USER_ID, " \
                       f"IFNULL((SELECT USER_NAME " \
                       f"FROM tn_user_info WHERE USER_ID = PAYMENT_USER_ID), '') AS PAYMENT_USER_NAME, " \
                       f"IFNULL(DATE_FORMAT(REGISTER_DATETIME, '%Y-%m-%d %H:%i:%S'), '') AS REGISTER_DATETIME, " \
                       f"IFNULL(DATE_FORMAT(LOGIN_DATETIME, '%Y-%m-%d %H:%i:%S'), '') AS LOGIN_DATETIME, " \
                       f"IFNULL(LASTWEEK_REPORT_ID, '') AS LASTWEEK_REPORT_ID, " \
                       f"IFNULL(THISWEEK_REPORT_ID, '') AS THISWEEK_REPORT_ID, " \
                       f"INSERT_USER_ID, " \
                       f"IFNULL(DATE_FORMAT(INSERT_DATETIME, '%Y-%m-%d %H:%i:%S'), '') AS INSERT_DATETIME, " \
                       f"UPDATE_USER_ID, " \
                       f"IFNULL(DATE_FORMAT(UPDATE_DATETIME, '%Y-%m-%d %H:%i:%S'), '') AS UPDATE_DATETIME " \
                       f"FROM tn_user_info "
            if user_pw:
                sql += f"WHERE USER_ID = '{user_id}' AND `PASSWORD` = '{user_pw}'; "
            else:
                sql += f"WHERE USER_ID = '{user_id}'; "

            result = select(sql)
            
        except Exception as ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result

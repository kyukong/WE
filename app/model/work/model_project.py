from flask import g

from app.config import DB

from app.model.common.model_db_connect import select, insert, update, delete

class Project():

    # 20210913 KYB add 프로젝트 정보 조회
    def get_project_info(self):
        result = dict()

        try:
            sql = ""
            sql += f"SELECT PROJECT_ID, IFNULL(PROJECT_NAME, '') AS PROJECT_NAME, "
            sql += f"IFNULL(PROJECT_START_DATETIME, '') AS PROJECT_START_DATETIME, "
            sql += f"IFNULL(PROJECT_END_DATETIME, '') AS PROJECT_END_DATETIME, IFNULL(MEMO, '') AS MEMO, "
            sql += f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME "
            sql += f"FROM tn_project_info; "

            result = select(sql)
            
        except ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result
    
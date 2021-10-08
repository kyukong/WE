from app.config import DB

from app.model.common.model_db_connect import select, insert, update, delete

class Code:
    
    def __init__(self, CODE=None):
        self.CODE = CODE

    def get_code_list(self, highcode):
        sql = ""
        sql += f"SELECT IFNULL(HIGHCODE, '') AS HIGHCODE, CODE, "
        sql += f"IFNULL(CODE_NAME, '') AS CODE_NAME, IFNULL(CODE_LEVEL, '') AS CODE_LEVEL "
        sql += f"FROM tc_code_info "
        sql += f"WHERE HIGHCODE = '{highcode}'; "

        result = select(sql)
        return result
    

from app.config import DB

from app.model.common.model_db_connect import select, insert, update, delete

class Menu:
    
    def __init__(self, CODE=None):
        self.CODE = CODE

    def get_menu_list(self):
        sql = ""
        sql += f"SELECT HIGHCODE, `CODE`, MENU_NAME, MENU_LEVEL, `PATH`, DISPLAY_FLAG "
        sql += "FROM tc_menu_info "
        sql += "WHERE DISPLAY_FLAG != 'N'; "

        result = select(sql)
        return result
    
    def ins_menu_info(self, menu_info):
        sql = ""
        sql += f"INSERT INTO tc_menu_info (HIGHCODE, `CODE`, MENU_NAME, MENU_LEVEL, `PATH`, DISPLAY_FLAG) "
        sql += f"VALUES "
        sql += f"('{menu_info['HIGHCODE']}', '{menu_info['CODE']}', '{menu_info['MENU_NAME']}', "
        sql += f"{menu_info['MENU_LEVEL']}, '{menu_info['PATH']}', '{menu_info['DISPLAY_FLAG']}'), "

        result = insert(sql)

        return result
    
    def upd_menu_info(self, menu_info):
        sql = ""
        sql += f"UPDATE tc_menu_info "
        sql += f"SET MENU_NAME = '{menu_info['MENU_NAME']}' "
        sql += f"WHERE CODE = '{menu_info['CODE']}'; "

        result = update(sql)

        return result

    def del_menu_info(self, menu_info):
        sql = ""
        sql += f"DELETE FROM  tc_menu_info "
        sql += f"WHERE CODE = '{menu_info['CODE']}'; "

        result = delete(sql)

        return result

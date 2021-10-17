from app.config import DB

from app.model.common.model_db_connect import select, insert, update, delete


class Code:
    
    def __init__(self, CODE=None):
        self.CODE = CODE

    # 'highcode' 값을 가지는 코드들 리스트 조회
    def get_code_list(self, highcode: str) -> dict:
        '''
        입력한 하이코드값을 가지는 코드들의 리스트를 조회한다.
        :param highcode: 하이코드값
        :return: 코드리스트
        '''
        result: dict = dict()
        try:
            sql: str = f"SELECT IFNULL(HIGHCODE, '') AS HIGHCODE, CODE, " \
                   f"IFNULL(CODE_NAME, '') AS CODE_NAME, IFNULL(CODE_LEVEL, '') AS CODE_LEVEL " \
                   f"FROM tc_code_info " \
                   f"WHERE HIGHCODE = '{highcode}'; "

            result = select(sql)
        except Exception as ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result

    # 코드값 이름 조회
    def get_code_name(self, code: str) -> dict:
        '''
        하나의 코드 값의 코드 이름을 조회한다.
        :param code: 코드
        :return: 코드 이름
        '''
        result: dict = dict()
        try:
            sql: str = f"SELECT HIGHCODE, CODE, CODE_NAME, CODE_LEVEL " \
                       f"FROM tc_code_info " \
                       f"WHERE CODE = '{code}'; "
            result = select(sql)
        except Exception as ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result

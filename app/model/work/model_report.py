from flask import g

from app.model.common.model_db_connect import select, insert, update, delete

from app.config import DB, SEARCH


class Report:
    
    # 보고서 리스트 조회
    @staticmethod
    def get_report_list(search_list: dict, page: str) -> dict:
        '''
        보고서 검색 화면에서 보고서 리스트 정보 조회
        :param search_list: 검색어
        :param page: 요청한 페이지
        :return 보고서 리스트 정보
        '''
        result = dict()

        try:
            sql = ""
            total_sql = ""
            from_sql = ""
            where_sql = ""

            sql += f"SELECT REPORT_ID, IFNULL(`report`.REGISTER_DATETIME, '') AS REGISTER_DATETIME, " \
                   f"IFNULL(`report`.USER_ID, '') AS USER_ID, " \
                   f"IFNULL(`report`.USER_ID, '') AS now_USER_ID, " \
                   f"IFNULL((SELECT USER_NAME FROM tn_user_info WHERE USER_ID = now_USER_ID), '') AS USER_NAME, " \
                   f"IFNULL((SELECT CODE_NAME " \
                   f"FROM tc_code_info WHERE `CODE` = PAYMENT_PROGRESS_CODE), '') AS PAYMENT_PROGRESS_CODE_NAME, " \
                   f"IFNULL(DATE_FORMAT(THISWEEK_START_DATETIME, '%Y-%m-%d'), '') AS THISWEEK_START_DATETIME, " \
                   f"IFNULL(DATE_FORMAT(THISWEEK_END_DATETIME, '%Y-%m-%d'), '') AS THISWEEK_END_DATETIME "

            total_sql += f"SELECT count(*) AS total "

            from_sql += f"FROM tn_report_info AS `report` "
            if search_list:
                from_sql += f"JOIN tn_user_info AS `user` "
                from_sql += f"ON `report`.USER_ID = `user`.USER_ID "
                
                where_count = 0
                if search_list['search_start_report_date'] != "":
                    if where_count == 0:
                        where_sql += f"WHERE "
                    else:
                        where_sql += f"AND "
                    where_sql += f"`report`.REGISTER_DATETIME >= '{search_list['search_start_register_date']}' "
                    where_count += 1
                if search_list['search_end_report_date'] != "":
                    if where_count == 0:
                        where_sql += f"WHERE "
                    else:
                        where_sql += f"AND "
                    where_sql += f"`report`.REGISTER_DATETIME <= '{search_list['search_end_register_date']}' "
                    where_count += 1
                if search_list['search_report_state_code'] != "":
                    if where_count == 0:
                        where_sql += f"WHERE "
                    else:
                        where_sql += f"AND "
                    where_sql += f"PAYMENT_PROGRESS_CODE = '{search_list['search_report_state_code']}' "
                    where_count += 1
                if search_list['search_report_user_name'] != "":
                    if where_count == 0:
                        where_sql += f"WHERE "
                    else:
                        where_sql += f"AND "
                    where_sql += f"USER_NAME LIKE '%{search_list['search_report_user_name']}%' "
                    where_count += 1

            sql += from_sql + where_sql
            sql += f"ORDER BY REGISTER_DATETIME DESC " \
                   f"LIMIT {str(SEARCH['SEARCH_RESULT_COUNT'] * (int(page) - 1))}, " \
                   f"{ str(SEARCH['SEARCH_RESULT_COUNT']) }; "
            total_sql += from_sql + where_sql + "; "

            result = select(sql)
            total_result = select(total_sql)

            if total_result['result'] != 'fail':
                result['total'] = total_result['data'][0]['total']
            else:
                result['total'] = 0
            
        except Exception as ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result

    # 보고서 정보 조회
    @staticmethod
    def get_report_info(report_id: str) -> dict:
        '''
        보고서 상세정보 정보 조회
        :param report_id: 보고서 ID
        :return: 보고서 정보
        '''
        result: dict = dict()
        try:
            sql: str = f"SELECT REPORT_ID, IFNULL(REGISTER_DATETIME, '') AS REGISTER_DATETIME, " \
                       f"IFNULL(USER_ID, '') AS USER_ID, " \
                       f"IFNULL(PAYMENT_USER_ID, '') AS PAYMENT_USER_ID, " \
                       f"IFNULL((SELECT USER_NAME FROM tn_user_info WHERE USER_ID = PAYMENT_USER_ID), '') " \
                       f"AS PAYMENT_USER_NAME, " \
                       f"IFNULL(PAYMENT_PROGRESS_CODE, '') AS PAYMENT_PROGRESS_CODE, " \
                       f"IFNULL((SELECT CODE_NAME FROM tc_code_info WHERE `CODE` = PAYMENT_PROGRESS_CODE), '') " \
                       f"AS PAYMENT_PROGRESS_CODE_NAME, " \
                       f"IFNULL(DATE_FORMAT(PAYMENT_DATETIME, '%Y-%m-%d %H:%i:%s'), '') AS PAYMENT_DATETIME, " \
                       f"IFNULL(PAYMENT_RETURN_CONTENT, '') AS PAYMENT_RETURN_CONTENT, " \
                       f"IFNULL(DATE_FORMAT(THISWEEK_START_DATETIME, '%Y-%m-%d %H:%i:%s'), '') " \
                       f"AS THISWEEK_START_DATETIME, " \
                       f"IFNULL(DATE_FORMAT(THISWEEK_END_DATETIME, '%Y-%m-%d %H:%i:%s'), '') AS THISWEEK_END_DATETIME, " \
                       f"IFNULL(DATE_FORMAT(NEXTWEEK_START_DATETIME, '%Y-%m-%d %H:%i:%s'), '') " \
                       f"AS NEXTWEEK_START_DATETIME, " \
                       f"IFNULL(DATE_FORMAT(NEXTWEEK_END_DATETIME, '%Y-%m-%d %H:%i:%s'), '') AS NEXTWEEK_END_DATETIME, " \
                       f"IFNULL(INSERT_USER_ID, '') AS INSERT_USER_ID, " \
                       f"IFNULL(DATE_FORMAT(INSERT_DATETIME, '%Y-%m-%d %H:%i:%s'), '') AS INSERT_DATETIME, " \
                       f"IFNULL(UPDATE_USER_ID, '') AS UPDATE_USER_ID, " \
                       f"IFNULL(DATE_FORMAT(UPDATE_DATETIME, '%Y-%m-%d %H:%i:%s'), '') AS UPDATE_DATETIME " \
                       f"FROM tn_report_info " \
                       f"WHERE REPORT_ID = '{report_id}';"
            result = select(sql)
        except Exception as ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result

    # 이번주 보고서 정보 조회
    @staticmethod
    def get_thisweek_report_info(user_id: str, thisweek_start_datetime: str) -> dict:
        '''
        이번주 주간보고서 정보 조회
        :param user_id: 사용자 ID
        :param thisweek_start_datetime: 이번주 주간보고서 시작일자
        :return: 주간보고서 정보
        '''
        result: dict = dict()
        try:
            sql: str = f"SELECT REPORT_ID, IFNULL(REGISTER_DATETIME, '') AS REGISTER_DATETIME, " \
                       f"IFNULL(USER_ID, '') AS USER_ID, IFNULL(PAYMENT_USER_ID, '') AS PAYMENT_USER_ID, " \
                       f"IFNULL((SELECT USER_NAME FROM tn_user_info WHERE USER_ID = PAYMENT_USER_ID), '') " \
                       f"AS PAYMENT_USER_NAME, " \
                       f"IFNULL(PAYMENT_PROGRESS_CODE, '') AS PAYMENT_PROGRESS_CODE, " \
                       f"IFNULL((SELECT CODE_NAME FROM tc_code_info WHERE `CODE` = PAYMENT_PROGRESS_CODE), '') " \
                       f"AS PAYMENT_PROGRESS_CODE_NAME, " \
                       f"IFNULL(DATE_FORMAT(PAYMENT_DATETIME, '%Y-%m-%d %H:%i:%s'), '') AS PAYMENT_DATETIME, " \
                       f"IFNULL(PAYMENT_RETURN_CONTENT, '') AS PAYMENT_RETURN_CONTENT, " \
                       f"IFNULL(DATE_FORMAT(THISWEEK_START_DATETIME, '%Y-%m-%d %H:%i:%s'), '') " \
                       f"AS THISWEEK_START_DATETIME, " \
                       f"IFNULL(DATE_FORMAT(THISWEEK_END_DATETIME, '%Y-%m-%d %H:%i:%s'), '') " \
                       f"AS THISWEEK_END_DATETIME, " \
                       f"IFNULL(DATE_FORMAT(NEXTWEEK_START_DATETIME, '%Y-%m-%d %H:%i:%s'), '') " \
                       f"AS NEXTWEEK_START_DATETIME, " \
                       f"IFNULL(DATE_FORMAT(NEXTWEEK_END_DATETIME, '%Y-%m-%d %H:%i:%s'), '') " \
                       f"AS NEXTWEEK_END_DATETIME, " \
                       f"IFNULL(INSERT_USER_ID, '') AS INSERT_USER_ID, " \
                       f"IFNULL(DATE_FORMAT(INSERT_DATETIME, '%Y-%m-%d %H:%i:%s'), '') AS INSERT_DATETIME, " \
                       f"IFNULL(UPDATE_USER_ID, '') AS UPDATE_USER_ID, " \
                       f"IFNULL(DATE_FORMAT(UPDATE_DATETIME, '%Y-%m-%d %H:%i:%s'), '') AS UPDATE_DATETIME " \
                       f"FROM tn_report_info " \
                       f"WHERE USER_ID = '{user_id}' AND THISWEEK_START_DATETIME = '{thisweek_start_datetime}' " \
                       f"ORDER BY REGISTER_DATETIME DESC " \
                       f"LIMIT 1; "

            result = select(sql)
        except Exception as ex:
            result['result'] = 'fail'
            result['data'] = ex
        return result

    # 보고서 정보 등록
    @staticmethod
    def ins_report_info(report_dict: dict, user_id: str, his_id: str) -> dict:
        '''
        보고서 정보 등록
        :param report_dict: 보고서 정보
        :param user_id: 사용자 ID
        :param his_id: 이력 ID
        :return: 성공 여부
        '''
        result: dict = dict()
        try:
            sql = f"INSERT INTO tn_report_info " \
                  f"(REPORT_ID, REGISTER_DATETIME, USER_ID, PAYMENT_USER_ID, " \
                  f"PAYMENT_PROGRESS_CODE, PAYMENT_DATETIME, PAYMENT_RETURN_CONTENT, " \
                  f"THISWEEK_START_DATETIME, THISWEEK_END_DATETIME, " \
                  f"NEXTWEEK_START_DATETIME, NEXTWEEK_END_DATETIME, " \
                  f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME) " \
                  f"VALUES " \
                  f"('{report_dict['report_id']}', now(), '{user_id}', '{report_dict['paymentUserId']}', " \
                  f"'{report_dict['payment_progress_code']}', NULL, NULL, " \
                  f"'{report_dict['thisweekStartDatetime']}', '{report_dict['thisweekEndDatetime']}', " \
                  f"'{report_dict['nextweekStartDatetime']}', '{report_dict['nextweekEndDatetime']}', " \
                  f"'{user_id}', now(), '{user_id}', now()); "
            his_sql = Report.get_report_his_sql(report_dict['report_id'], his_id, 'INSERT')

            sql += his_sql

            result = insert(sql)

        except Exception as ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result

    # 보고서 정보 수정
    @staticmethod
    def upd_report_info(report_dict: dict, user_id: str, his_id: str) -> dict:
        '''
        보고서 정보 수정
        :param report_dict: 보고서 정보
        :param user_id: 사용자 ID
        :param his_id: 이력 ID
        :return: 성공 여부
        '''
        result: dict = dict()
        try:
            sql = f"UPDATE tn_report_info " \
                  f"SET REGISTER_DATETIME = now(), " \
                  f"PAYMENT_PROGRESS_CODE = '{report_dict['payment_progress_code']}', " \
                  f"UPDATE_USER_ID = '{user_id}', UPDATE_DATETIME = now() " \
                  f"WHERE REPORT_ID = '{report_dict['report_id']}';"
            his_sql = Report.get_report_his_sql(report_dict['report_id'], his_id, 'UPDATE')

            sql += his_sql

            result = update(sql)

        except Exception as ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result

    # 보고서 이력 테이블 sql 문 생성
    @staticmethod
    def get_report_his_sql(report_id: str, his_id: str, action: str = 'INSERT') -> str:
        '''
        보고서 이력 테이블 sql 문 생성
        :param report_id: 보고서 ID
        :param his_id: 이력 ID
        :param action: 이력 행위
        :return: sql 문
        '''
        his_sql = ""
        if not report_id:
            return his_sql

        his_sql += f"INSERT INTO th_report_his " \
                   f"(HIS_ID, HIS_DATETIME, ACTION, REPORT_ID, REGISTER_DATETIME, " \
                   f"USER_ID, PAYMENT_USER_ID, PAYMENT_PROGRESS_CODE, PAYMENT_DATETIME, PAYMENT_RETURN_CONTENT, " \
                   f"THISWEEK_START_DATETIME, THISWEEK_END_DATETIME, NEXTWEEK_START_DATETIME, NEXTWEEK_END_DATETIME, " \
                   f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME) " \
                   f"SELECT '{his_id}', now(), '{action}', REPORT_ID, REGISTER_DATETIME, " \
                   f"USER_ID, PAYMENT_USER_ID, PAYMENT_PROGRESS_CODE, PAYMENT_DATETIME, PAYMENT_RETURN_CONTENT, " \
                   f"THISWEEK_START_DATETIME, THISWEEK_END_DATETIME, NEXTWEEK_START_DATETIME, NEXTWEEK_END_DATETIME, " \
                   f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME " \
                   f"FROM tn_report_info " \
                   f"WHERE REPORT_ID = '{report_id}'; "

        return his_sql

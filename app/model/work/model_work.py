from app.model.common.model_db_connect import select, insert, update, delete

from app.config import DB, SEARCH


class Work:
    
    # 업무 정보 조회
    @staticmethod
    def get_work_list(search_list: dict, page: str) -> dict:
        '''
        업무 검색 화면에서 업무 리스트 정보 조회
        :param search_list: 검색어
        :param page: 요청한 페이지
        :return 업무 리스트 정보
        '''
        result = dict()

        try:
            sql = ""
            total_sql = ""
            from_sql = ""
            where_sql = ""

            sql += f"SELECT WORK_ID, PROJECT_ID, PROJECT_ID AS now_PROJECT_ID, " \
                   f"IFNULL((SELECT PROJECT_NAME FROM tn_project_info WHERE PROJECT_ID = now_PROJECT_ID), '') " \
                   f"AS PROJECT_NAME, " \
                   f"IFNULL(PLAN, '') AS PLAN, " \
                   f"IFNULL(WORK_STATE_CODE, '') AS WORK_STATE_CODE, " \
                   f"IFNULL((SELECT CODE_NAME FROM tc_code_info WHERE `CODE` = WORK_STATE_CODE), '') " \
                   f"AS WORK_STATE_CODE_NAME, " \
                   f"IFNULL(WORK_PROGRESS_CODE, '') AS WORK_PROGRESS_CODE, " \
                   f"IFNULL(DATE_FORMAT(WORK_DATE, '%Y-%m-%d'), '') AS WORK_DATE, " \
                   f"IFNULL(`work`.USER_ID, '') AS USER_ID, " \
                   f"IFNULL(`work`.USER_ID, '') AS now_USER_ID, " \
                   f"IFNULL((SELECT USER_NAME FROM tn_user_info WHERE USER_ID = now_USER_ID), '') AS USER_NAME, " \
                   f"IFNULL(WORK_CONTENT, '') AS WORK_CONTENT, IFNULL(DELAY_CONTENT, '') AS DELAY_CONTENT, " \
                   f"IFNULL(SOLUTION_CONTENT, '') AS SOLUTION_CONTENT, IFNULL(MEMO, '') AS MEMO, " \
                   f"`work`.INSERT_USER_ID, `work`.INSERT_DATETIME, `work`.UPDATE_USER_ID, `work`.UPDATE_DATETIME "

            total_sql += f"SELECT count(*) AS total "

            from_sql += f"FROM tn_work_info AS `work` "
            if search_list:
                from_sql += f"JOIN tn_user_info AS `user` " \
                            f"ON `work`.USER_ID = `user`.USER_ID "
                
                where_count = 0
                if search_list['search_start_word_date'] != "":
                    if where_count == 0:
                        where_sql += f"WHERE "
                    else:
                        where_sql += f"AND "
                    where_sql += f"WORK_DATE >= '{search_list['search_start_word_date']}' "
                    where_count += 1
                if search_list['search_end_word_date'] != "":
                    if where_count == 0:
                        where_sql += f"WHERE "
                    else:
                        where_sql += f"AND "
                    where_sql += f"WORK_DATE <= '{search_list['search_end_word_date']}' "
                    where_count += 1
                if search_list['search_project_code'] != "":
                    if where_count == 0:
                        where_sql += f"WHERE "
                    else:
                        where_sql += f"AND "
                    where_sql += f"PROJECT_ID = '{search_list['search_project_code']}' "
                    where_count += 1
                if search_list['search_work_user_name'] != "":
                    if where_count == 0:
                        where_sql += f"WHERE "
                    else:
                        where_sql += f"AND "
                    where_sql += f"USER_NAME LIKE '%{search_list['search_work_user_name']}%' "
                    where_count += 1
            
            sql += from_sql + where_sql
            sql += f"ORDER BY WORK_DATE DESC " \
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
    
    # 20211004 KYB add 업무 등록
    @staticmethod
    def ins_work_info(plan_insert_list, plan_update_list, plan_delete_list,
                      work_insert_list, work_update_list, work_delete_list, his_id):
        '''
        업무 상세정보 조회 화면에서 업무 등록
        :param 
        :return: 성공여부
        '''
        result = dict()

        try:
            sql = ""
            
            plan_sql = ""
            # TODO KYB 계획 정보 관련 처리는 model_plan 파일로 이동
            # 계획 정보 등록
            if plan_insert_list:
                plan_id_list = []
                plan_sql += f"INSERT INTO `tn_plan_info` "
                plan_sql += f"(PLAN_ID, PROJECT_ID, PLAN_DATE, `USER_ID`, PLAN, MEMO, "
                plan_sql += f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME) "
                plan_sql += f"VALUES "

                for i, plan_info in enumerate(plan_insert_list):
                    plan_id_list.append(plan_info['planID'])

                    plan_sql += f"('{plan_info['planID']}', '{plan_info['projectID']}', '{plan_info['planDay']}', "
                    plan_sql += f"'{plan_info['userID']}', '{plan_info['plan']}', '{plan_info['memo']}', "
                    plan_sql += f"'{plan_info['userID']}', now(), '{plan_info['userID']}', now()) "

                    if i != len(plan_insert_list) - 1:
                        plan_sql += ", "
                    else:
                        plan_sql += "; "

                # 계획 이력 정보 등록
                plan_his_sql = ""
                plan_his_sql += Work.get_plan_his_sql(plan_id_list, his_id, "INSERT")
                plan_sql += plan_his_sql

            # 계획 정보 수정
            if plan_update_list:
                plan_id_list = []
                
                for i, plan_info in enumerate(plan_update_list):
                    plan_id_list.append(plan_info['planID'])

                    plan_sql += f"UPDATE `tn_plan_info` "
                    plan_sql += f"SET PROJECT_ID = '{plan_info['projectID']}', PLAN_DATE = '{plan_info['planDay']}', "
                    plan_sql += f"USER_ID = '{plan_info['userID']}', PLAN = '{plan_info['plan']}', MEMO = '{plan_info['memo']}', "
                    plan_sql += f"UPDATE_USER_ID = '{plan_info['userID']}', UPDATE_DATETIME = now() "
                    plan_sql += f"WHERE PLAN_ID = '{plan_info['planID']}'; "
                
                # 계획 이력 정보 등록
                plan_his_sql = ""
                plan_his_sql += Work.get_plan_his_sql(plan_id_list, his_id, "UPDATE")
                plan_sql += plan_his_sql

            # 계획 정보 삭제
            if plan_delete_list:
                # 계획 이력 정보 등록
                plan_his_sql = ""
                plan_his_sql += Work.get_plan_his_sql(plan_delete_list, his_id, "DELETE")
                plan_sql += plan_his_sql

                # 계획 정보 삭제
                plan_sql += f"DELETE FROM `tn_plan_info` "
                plan_sql += f"WHERE PLAN_ID = "

                for i, plan_id in enumerate(plan_delete_list):
                    plan_sql += f"'{plan_id}' "

                    if i != len(plan_delete_list) - 1:
                        plan_sql += f"OR PLAN_ID = "
                    else:
                        plan_sql += f"; "

            work_sql = ""
            # 업무 정보 등록
            if work_insert_list:
                work_id_list = []
                work_sql += f"INSERT INTO `tn_work_info` "
                work_sql += f"(WORK_ID, PROJECT_ID, PLAN, WORK_STATE_CODE, WORK_PROGRESS_CODE, WORK_DATE, "
                work_sql += f"`USER_ID`, WORK_CONTENT, DELAY_CONTENT, SOLUTION_CONTENT, MEMO, FTP_PATH, "
                work_sql += f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME) "
                work_sql += f"VALUES "
                
                for i, work_info in enumerate(work_insert_list):
                    work_id_list.append(work_info['workID'])

                    work_sql += f"('{work_info['workID']}', '{work_info['projectID']}', '{work_info['plan']}', "
                    work_sql += f"'WRS0001', '{work_info['workStateCode']}', '{work_info['workDay']}', "
                    work_sql += f"'{work_info['userID']}', '{work_info['workContent']}', '{work_info['delayContent']}', "
                    work_sql += f"'{work_info['solutionContent']}', '{work_info['memo']}', '{work_info['ftpPath']}', "
                    work_sql += f"'{work_info['userID']}', now(), '{work_info['userID']}', now()) "

                    if i != len(work_insert_list) - 1:
                        work_sql += ", "
                    else:
                        work_sql += "; "
                
                # 업무 이력 정보 등록
                work_his_sql = ""
                work_his_sql += Work.get_work_his_sql(work_id_list, his_id, "INSERT")
                work_sql += work_his_sql

            # 업무 정보 수정
            if work_update_list:
                work_id_list = []
                
                for i, work_info in enumerate(work_update_list):
                    work_id_list.append(work_info['workID'])

                    work_sql += f"UPDATE `tn_work_info` "
                    work_sql += f"SET PROJECT_ID = '{work_info['projectID']}', PLAN = '{work_info['plan']}', "
                    work_sql += f"WORK_STATE_CODE = 'WRS0001', WORK_PROGRESS_CODE = '{work_info['workStateCode']}', "
                    work_sql += f"WORK_DATE = '{work_info['workDay']}', USER_ID = '{work_info['userID']}', "
                    work_sql += f"WORK_CONTENT = '{work_info['workContent']}', DELAY_CONTENT = '{work_info['delayContent']}', "
                    work_sql += f"SOLUTION_CONTENT = '{work_info['solutionContent']}', MEMO = '{work_info['memo']}', "
                    work_sql += f"FTP_PATH = '{work_info['ftpPath']}', "
                    work_sql += f"UPDATE_USER_ID = '{work_info['userID']}', UPDATE_DATETIME = now() "
                    work_sql += f"WHERE WORK_ID = '{work_info['workID']}'; "
                
                # 업무 이력 정보 등록
                work_his_sql = ""
                work_his_sql += Work.get_work_his_sql(work_id_list, his_id, "UPDATE")
                work_sql += work_his_sql

            # 업무 정보 삭제
            if work_delete_list:
                # 업무 이력 정보 등록
                work_his_sql = ""
                work_his_sql += Work.get_work_his_sql(work_delete_list, his_id, "DELETE")
                work_sql += work_his_sql

                # 업무 정보 삭제
                work_sql += f"DELETE FROM `tn_work_info` "
                work_sql += f"WHERE WORK_ID = "

                for i, work_id in enumerate(work_delete_list):
                    work_sql += f"'{work_id}' "

                    if i != len(work_delete_list) - 1:
                        work_sql += f"OR WORK_ID = "
                    else:
                        work_sql += f"; "
            
            sql += plan_sql + work_sql
            result = insert(sql)

        except Exception as ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result
    
    # 20211004 KYB add 계획 정보 조회
    @staticmethod
    def get_plan_info(user_id, plan_start_date, plan_end_date=False):
        '''
        업무 상세정보 조회 화면에서 계획 정보 조회
        보고서 화면에서 계획 정보 조회
        :param user_id: 작성자
        :param plan_start_date: 계획 등록 일자
        :param plan_end_date: 계획 종료 일자
        :return: 계획 정보 리스트
        '''
        result = dict()

        try:
            sql: str = f"SELECT PLAN_ID, IFNULL(PROJECT_ID, '') AS PROJECT_ID, " \
                       f"IFNULL(DATE_FORMAT(PLAN_DATE, '%Y-%m-%d'), '') AS PLAN_DATE, " \
                       f"IFNULL(`USER_ID`, '') AS USER_ID, IFNULL(PLAN, '') AS PLAN, IFNULL(MEMO, '') AS MEMO, " \
                       f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME " \
                       f"FROM `tn_plan_info` " \
                       f"WHERE PLAN_DATE >= '{plan_start_date}' AND `USER_ID` = '{user_id}' "
            if plan_end_date:
                sql += f"AND PLAN_DATE <= '{plan_end_date}' "
            sql += f"ORDER BY INSERT_DATETIME; "

            result = select(sql)

        except Exception as ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result

    # 20211004 KYB add 업무 정보 조회
    @staticmethod
    def get_work_info(user_id, work_start_date, work_end_date=False):
        '''
        업무 상세정보 조회 화면에서 업무 정보 조회
        보고서 화면에서 업무 정보 조회
        :param user_id: 작성자
        :param work_start_date: 업무 시작 일자
        :param work_end_date: 업무 종료 일자
        :return: 업무 정보 리스트
        '''
        result = dict()

        try:
            sql: str = f"SELECT WORK_ID, IFNULL(PROJECT_ID, '') AS PROJECT_ID, IFNULL(PLAN, '') AS PLAN, " \
                       f"IFNULL(WORK_STATE_CODE, '') AS WORK_STATE_CODE, " \
                       f"IFNULL(WORK_PROGRESS_CODE, '') AS WORK_PROGRESS_CODE, " \
                       f"IFNULL(DATE_FORMAT(WORK_DATE, '%Y-%m-%d'), '') AS WORK_DATE, " \
                       f"IFNULL(`USER_ID`, '') AS USER_ID, IFNULL(WORK_CONTENT, '') AS WORK_CONTENT, " \
                       f"IFNULL(DELAY_CONTENT, '') AS DELAY_CONTENT, IFNULL(SOLUTION_CONTENT, '') AS SOLUTION_CONTENT, " \
                       f"IFNULL(MEMO, '') AS MEMO, IFNULL(FTP_PATH, '') AS FTP_PATH, " \
                       f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME " \
                       f"FROM `tn_work_info` " \
                       f"WHERE WORK_DATE >= '{work_start_date}' AND `USER_ID` = '{user_id}' "
            if work_end_date:
                sql += f"AND WORK_DATE <= '{work_end_date}' "
            sql += f"ORDER BY INSERT_DATETIME; "

            result = select(sql)

        except Exception as ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result

    # 업무 상태값 수정
    @staticmethod
    def upd_work_state_info(work_id_list: list, work_state_code: str, user_id: str, his_id: str) -> dict:
        '''
        업무 상태값 및 시스템 정보 수정
        :param work_id_list: 업무 ID 리스트
        :param work_state_code: 저장할 업무 상태값
        :param user_id: 사용자 ID
        :param his_id: 이력 ID
        :return: 성공 여부
        '''
        result: dict = dict()
        try:
            if not work_id_list:
                return {'result': 'fail', 'data': 'work id list is empty.'}

            sql: str = f"UPDATE tn_work_info " \
                       f"SET WORK_STATE_CODE = '{work_state_code}', " \
                       f"UPDATE_USER_ID = '{user_id}', UPDATE_DATETIME = now() " \
                       f"WHERE WORK_ID = "

            for i, work_id in enumerate(work_id_list):
                sql += f"'{work_id}' "

                if i != len(work_id_list) - 1:
                    sql += f"OR WORK_ID = "
                else:
                    sql += f"; "

            his_sql: str = Work().get_work_his_sql(work_id_list, his_id, 'UPDATE')
            sql += his_sql

            result = update(sql)
        except Exception as ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result

    # 20211004 KYB add 계획 테이블 이력 sql 문 생성
    @staticmethod
    def get_plan_his_sql(plan_id_list, his_id, action="INSERT"):
        his_sql = ""
        if not plan_id_list:
            return his_sql
        
        his_sql += f"INSERT INTO `th_plan_his` "
        his_sql += f"(HIS_ID, HIS_DATETIME, ACTION, PLAN_ID, PROJECT_ID, PLAN_DATE, `USER_ID`, PLAN, MEMO, "
        his_sql += f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME) "
        his_sql += f"SELECT '{his_id}', now(), '{action}', PLAN_ID, PROJECT_ID, PLAN_DATE, `USER_ID`, PLAN, MEMO, "
        his_sql += f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME "
        his_sql += f"FROM `tn_plan_info` "
        his_sql += f"WHERE PLAN_ID = "

        for i, plan_id in enumerate(plan_id_list):
            his_sql += f"'{plan_id}' "

            if i != len(plan_id_list) - 1:
                his_sql += f"OR PLAN_ID = "
            else:
                his_sql += f"; "
        
        return his_sql

    # 20211004 KYB add 업무 테이블 이력 sql 문 생성
    @staticmethod
    def get_work_his_sql(work_id_list, his_id, action="INSERT"):
        his_sql = ""
        if not work_id_list:
            return his_sql
        
        his_sql += f"INSERT INTO `th_work_his` "
        his_sql += f"(HIS_ID, HIS_DATETIME, ACTION, WORK_ID, PROJECT_ID, PLAN, WORK_STATE_CODE, "
        his_sql += f"WORK_PROGRESS_CODE, WORK_DATE, `USER_ID`, WORK_CONTENT, DELAY_CONTENT, SOLUTION_CONTENT, MEMO, "
        his_sql += f"FTP_PATH, INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME) "
        his_sql += f"SELECT '{his_id}', now(), '{action}', WORK_ID, PROJECT_ID, PLAN, WORK_STATE_CODE, "
        his_sql += f"WORK_PROGRESS_CODE, WORK_DATE, `USER_ID`, WORK_CONTENT, DELAY_CONTENT, SOLUTION_CONTENT, MEMO, "
        his_sql += f"FTP_PATH, INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME "
        his_sql += f"FROM `tn_work_info` "
        his_sql += f"WHERE WORK_ID = "

        for i, work_id in enumerate(work_id_list):
            his_sql += f"'{work_id}' "

            if i != len(work_id_list) - 1:
                his_sql += f"OR WORK_ID = "
            else:
                his_sql += f"; "
        
        return his_sql



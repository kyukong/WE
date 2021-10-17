from app.model.common.model_db_connect import select, insert, update, delete

from app.config import DB, SEARCH


class Plan:

    # 계획 정보 등록
    @staticmethod
    def ins_plan_info(plan_insert_list: list, plan_update_list: list, plan_delete_list: list, his_id: str) -> dict:
        '''
        계획 정보 등록
        :param plan_insert_list:
        :param plan_update_list:
        :param plan_delete_list:
        :param his_id: 이력 ID
        :return: 성공 여부
        '''
        result: dict = dict()

        try:
            sql = ""

            plan_sql = ""
            # 계획 정보 등록
            if plan_insert_list:
                plan_id_list = []
                plan_sql += f"INSERT INTO `tn_plan_info` " \
                            f"(PLAN_ID, PROJECT_ID, PLAN_DATE, `USER_ID`, PLAN, MEMO, " \
                            f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME) " \
                            f"VALUES "

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
                plan_his_sql += Plan.get_plan_his_sql(plan_id_list, his_id, "INSERT")
                plan_sql += plan_his_sql

            # 계획 정보 수정
            if plan_update_list:
                plan_id_list = []

                for i, plan_info in enumerate(plan_update_list):
                    plan_id_list.append(plan_info['planID'])

                    plan_sql += f"UPDATE `tn_plan_info` " \
                                f"SET PROJECT_ID = '{plan_info['projectID']}', PLAN_DATE = '{plan_info['planDay']}', " \
                                f"USER_ID = '{plan_info['userID']}', PLAN = '{plan_info['plan']}', MEMO = '{plan_info['memo']}', " \
                                f"UPDATE_USER_ID = '{plan_info['userID']}', UPDATE_DATETIME = now() " \
                                f"WHERE PLAN_ID = '{plan_info['planID']}'; "

                # 계획 이력 정보 등록
                plan_his_sql = ""
                plan_his_sql += Plan.get_plan_his_sql(plan_id_list, his_id, "UPDATE")
                plan_sql += plan_his_sql

            # 계획 정보 삭제
            if plan_delete_list:
                # 계획 이력 정보 등록
                plan_his_sql = ""
                plan_his_sql += Plan.get_plan_his_sql(plan_delete_list, his_id, "DELETE")
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

            sql += plan_sql
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
            sql = ""
            sql += f"SELECT PLAN_ID, IFNULL(PROJECT_ID, '') AS PROJECT_ID, IFNULL(PLAN_DATE, '') AS PLAN_DATE, "
            sql += f"IFNULL(`USER_ID`, '') AS USER_ID, IFNULL(PLAN, '') AS PLAN, IFNULL(MEMO, '') AS MEMO, "
            sql += f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME "
            sql += f"FROM `tn_plan_info` "
            sql += f"WHERE PLAN_DATE >= '{plan_start_date}' AND `USER_ID` = '{user_id}' "
            if plan_end_date:
                sql += f"AND PLAN_DATE <= '{plan_end_date}' "
            sql += f"ORDER BY INSERT_DATETIME; "

            result = select(sql)

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

        his_sql += f"INSERT INTO `th_plan_his` " \
                   f"(HIS_ID, HIS_DATETIME, ACTION, PLAN_ID, PROJECT_ID, PLAN_DATE, `USER_ID`, PLAN, MEMO, " \
                   f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME) " \
                   f"SELECT '{his_id}', now(), '{action}', PLAN_ID, PROJECT_ID, PLAN_DATE, `USER_ID`, PLAN, MEMO, " \
                   f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME " \
                   f"FROM `tn_plan_info` " \
                   f"WHERE PLAN_ID = "

        for i, plan_id in enumerate(plan_id_list):
            his_sql += f"'{plan_id}' "

            if i != len(plan_id_list) - 1:
                his_sql += f"OR PLAN_ID = "
            else:
                his_sql += f"; "

        return his_sql

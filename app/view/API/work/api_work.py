from flask import request
from flask_login import current_user
from flask_restful import Resource

from app import api

from app.view.API.common.basic import get_ID

from app.model.work.model_work import Work


# 20211002 KYB add 업무 등록
class APIWorkInsert(Resource):
    def get(self):
        return {'result': "get"}

    def post(self):
        user_info = current_user
        if not user_info.is_authenticated:
            return {"result": "fail", "context": "login first"}
        
        body = request.get_json()

        plan_insert_list = body['planInsertInfoList']
        plan_update_list = body['planUpdateInfoList']
        plan_delete_list = body['planDeleteInfoList']
        work_insert_list = body['workInsertInfoList']
        work_update_list = body['workUpdateInfoList']
        work_delete_list = body['workDeleteInfoList']

        # 계획 정보 추가
        for plan_info in plan_insert_list:
            plan_info['planID'] = get_ID("PN")
            plan_info['userID'] = user_info.user_id

        for plan_info in plan_update_list:
            plan_info['userID'] = user_info.user_id

        # 업무 정보 추가
        for work_info in work_insert_list:
            work_info['workID'] = get_ID("WK")
            work_info['userID'] = user_info.user_id
        
        for work_info in work_update_list:
            work_info['userID'] = user_info.user_id

        # 이력 아이디
        his_id = get_ID("HIS")

        result = Work().ins_work_info(plan_insert_list, plan_update_list, plan_delete_list,
                                      work_insert_list, work_update_list, work_delete_list, his_id)

        if result['result'] == 'fail':
            return {'result': 'fail'}
        else:
            return result


api.add_resource(APIWorkInsert, "/api/v1/work/insert")
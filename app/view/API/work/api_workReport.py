from flask import request
from flask_login import current_user
from flask_restful import Resource

from app import api

from app.view.API.common.basic import get_ID

from app.model.work.model_report import Report
from app.model.work.model_work import Work
from app.model.work.model_plan import Plan


# 보고서 등록
class APIWorkReportInsert(Resource):
    def get(self):
        return {'result': "get"}

    def post(self):
        user_info = current_user
        if not user_info.is_authenticated:
            return {"result": "fail", "context": "login first"}

        body: dict = request.get_json()
        report_dict: dict = body['reportDict']
        work_id_list: list = body['workIDList']
        plan_insert_list: list = body['planInsertInfoList']
        plan_update_list: list = body['planUpdateInfoList']
        plan_delete_list: list = body['planDeleteInfoList']

        user_id = user_info.user_id

        his_id = get_ID('HISWRP')

        # 보고서 정보 저장
        report_id: str = get_ID('WRP')
        report_dict['report_id'] = report_id
        report_insert_result = Report().ins_report_info(report_dict, user_id, his_id)
        if report_insert_result['result'] == 'fail':
            return {'result': 'fail'}

        # 업무 상태 정보 변경
        work_state_code: str = 'WRS0002'
        work_state_update_result = Work().upd_work_state_info(work_id_list, work_state_code, user_id, his_id)
        if work_state_update_result['result'] == 'fail':
            return {'result': 'fail'}

        # 차주 계획 정보 저장
        # 계획 정보 추가
        for plan_info in plan_insert_list:
            plan_info['planID'] = get_ID("PN")
            plan_info['userID'] = user_id

        for plan_info in plan_update_list:
            plan_info['userID'] = user_id

        result = Plan().ins_plan_info(plan_insert_list, plan_update_list, plan_delete_list, his_id)
        if result['result'] == 'fail':
            return {'result': 'fail'}
        else:
            return result


api.add_resource(APIWorkReportInsert, "/api/v1/workReport/insert")
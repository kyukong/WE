from flask import request
from flask_login import current_user
from flask_restful import Resource

from app import api

from app.view.API.common.basic import get_ID

from app.model.work.model_report import Report
from app.model.work.model_work import Work
from app.model.work.model_plan import Plan
from app.model.common.model_user import User


# 보고서 등록
class APIWorkReportInsert(Resource):
    @staticmethod
    def get():
        return {'result': "get"}

    @staticmethod
    def post():
        user_info = current_user
        if not user_info.is_authenticated:
            return {"result": "fail", "context": "login first"}

        body: dict = request.get_json()
        request_type: str = body['requestType']
        report_dict: dict = body['reportDict']
        work_id_list: list = body['workIDList']
        plan_insert_list: list = body['planInsertInfoList']
        plan_update_list: list = body['planUpdateInfoList']
        plan_delete_list: list = body['planDeleteInfoList']

        user_id = user_info.user_id
        his_id = get_ID('HISWRP')

        if request_type == 'save':
            payment_progress_code: str = 'RPS0001'  # 작성중
            work_state_code: str = 'WRS0002'  # 보고서 작성
        else:  # request_type == 'report'
            payment_progress_code: str = 'RPS0002'  # 보고
            work_state_code: str = 'WRS0003'  # 보고

        # 이전에 작성한 금주 주간보고서가 없을 경우
        if report_dict['report_id'] == '':
            # 보고서 정보 저장
            report_id: str = get_ID('WRP')
            report_dict['report_id'] = report_id
            report_dict['payment_progress_code'] = payment_progress_code
            report_insert_result = Report().ins_report_info(report_dict, user_id, his_id)
            if report_insert_result['result'] == 'fail':
                return {'result': 'fail'}
        else:
            # 보고서 정보 수정
            report_dict['payment_progress_code'] = payment_progress_code
            report_update_result = Report().upd_report_info(report_dict, user_id, his_id)
            if report_update_result['result'] == 'fail':
                return {'result': 'fail'}

        # 업무 상태 정보 변경
        work_state_update_result = Work().upd_work_state_info(work_id_list, work_state_code, user_id, his_id)
        if work_state_update_result['result'] == 'fail':
            return {'result': 'fail'}

        # 차주 계획 정보 저장
        for plan_info in plan_insert_list:
            plan_info['planID'] = get_ID("PN")
            plan_info['userID'] = user_id
        for plan_info in plan_update_list:
            plan_info['userID'] = user_id

        plan_insert_result = Plan().ins_plan_info(plan_insert_list, plan_update_list, plan_delete_list, his_id)
        if plan_insert_result['result'] == 'fail':
            return {'result': 'fail'}

        # 사용자 정보 수정
        user_update_result = User().upd_user_report_info(user_id, his_id, thisweek_report_id=report_dict['report_id'])
        if user_update_result['result'] == 'fail':
            return {'result': 'fail'}
        else:
            return user_update_result


# 보고서 결재
class APIWorkApprovalReport(Resource):
    @staticmethod
    def get():
        return {'result': "get"}

    @staticmethod
    def post():
        user_info = current_user
        if not user_info.is_authenticated:
            return {"result": "fail", "context": "login first"}

        body: dict = request.get_json()
        report_id: str = body['reportID']
        work_id_list: list = body['workIDList']

        user_id = user_info.user_id
        his_id = get_ID('HISWRP')

        # 업무 상태코드 수정
        work_state_update_result = Work().upd_work_state_info(work_id_list, 'WRS0004', user_id, his_id)
        if work_state_update_result['result'] == 'fail':
            return {'result': 'fail'}

        # 보고서 상태코드 및 결재 시간 수정
        report_dict: dict = dict()
        report_dict['report_id'] = report_id
        report_dict['payment_progress_code'] = 'RPS0003'
        approval_report_result = Report().upd_report_info(report_dict, user_id, his_id)
        if approval_report_result['result'] == 'fail':
            return {'result': 'fail'}
        else:
            return approval_report_result


# 보고서 반려
class APIWorkReportReturn(Resource):
    @staticmethod
    def get():
        return {'result': "get"}

    @staticmethod
    def post():
        user_info = current_user
        if not user_info.is_authenticated:
            return {"result": "fail", "context": "login first"}

        # 업무 상태코드 수정

        # 보고서 상태코드 및 결재시간, 반려 내용 수정

        # 사용자 이번주 보고서 정보 수정


api.add_resource(APIWorkReportInsert, "/api/v1/workReport/insert")
api.add_resource(APIWorkApprovalReport, "/api/v1/workReport/approval")

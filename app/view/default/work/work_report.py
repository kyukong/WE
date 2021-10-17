from flask import render_template, request
from app import app
from flask_login import login_required, current_user
from datetime import datetime, timedelta

from app.model.common.model_code import Code
from app.model.work.model_report import Report
from app.model.work.model_work import Work
from app.model.work.model_project import Project
from app.model.common.model_user import User

from app.view.default.common.basic import set_code_ALL, get_menu_list, get_page_info


# 20211011 KYB add 업무 보고서 검색 추가
@app.route('/work/report/search')
@login_required
def work_report_search():
    # 메뉴 조회
    menu_list = get_menu_list()
    now_top_menu_code = 'MENWRK'
    now_left_menu_code = 'MENWRK001'

    # 보고서 상태 코드 조회
    report_state_list = Code().get_code_list('RTS0001')
    if report_state_list['result'] != 'fail' and report_state_list['count'] != 0:
        report_state_list = report_state_list['data']
    else:
        report_state_list = []
    report_state_list = set_code_ALL(report_state_list)

    # 검색어 조회
    search_word = request.args
    search_list = dict()
    if search_word.get('page'):
        search_list['page'] = search_word.get('page')
    else:
        search_list['page'] = '1'

    if search_word:
        search_list['search_start_report_date'] = search_word.get('searchStartReportDate')
        search_list['search_end_report_date'] = search_word.get('searchEndReportDate')
        if search_word.get('searchReportStateCode') == 'ALL':
            search_list['search_report_state_code'] = ''
        else:
            search_list['search_report_state_code'] = search_word.get('searchReportStateCode')
        search_list['search_report_user_name'] = search_word.get('searchReportUserName')
    else:
        search_list['search_start_report_date'] = ""
        search_list['search_end_report_date'] = ""
        search_list['search_report_state_code'] = ""
        search_list['search_report_user_name'] = ""
    
    # 보고서 정보 조회
    report_list = Report().get_report_list(search_list)
    if report_list['result'] != 'fail':
        report_total_count = report_list['total']
        report_list = report_list['data']
    else:
        report_total_count = 0
        report_list = []
    
    # 페이징 처리
    page_info = get_page_info(int(search_list['page']), report_total_count)

    return render_template('/work/template_workReportSearch.html', menu_list=menu_list,
                           now_top_menu_code=now_top_menu_code, now_left_menu_code=now_left_menu_code,
                           report_state_list=report_state_list, report_list=report_list,
                           page_info=page_info, report_total_count=report_total_count)


# 업무 보고서 등록
@app.route('/work/report/insert')
@login_required
def work_report_insert():
    now_user = current_user
    user_id = now_user.user_id
    user_name = now_user.user_name

    # 메뉴 조회
    menu_list = get_menu_list()
    now_top_menu_code = 'MENWRK'
    now_left_menu_code = 'MENWRK003'

    # 보고서 등록 일자 조회
    today_datetime = datetime.today()
    today = today_datetime.strftime("%Y-%m-%d")
    weekday = today_datetime.weekday()

    # 금주 날짜 계산
    thisweek_start_datetime = today_datetime - timedelta(days=weekday)
    thisweek_start_day = thisweek_start_datetime.strftime("%Y-%m-%d")
    thisweek_end_datetime = today_datetime + timedelta(days=(4 - weekday))
    thisweek_end_day = thisweek_end_datetime.strftime("%Y-%m-%d")

    # 차주 날짜 계산
    nextweek_start_datetime = thisweek_start_datetime + timedelta(days=7)
    nextweek_start_day = nextweek_start_datetime.strftime("%Y-%m-%d")
    nextweek_end_datetime = thisweek_end_datetime + timedelta(days=7)
    nextweek_end_day = nextweek_end_datetime.strftime("%Y-%m-%d")

    day_info = dict()
    day_info['today'] = today
    day_info['thisweek_start_day'] = thisweek_start_day
    day_info['thisweek_end_day'] = thisweek_end_day
    day_info['nextweek_start_day'] = nextweek_start_day
    day_info['nextweek_end_day'] = nextweek_end_day

    # 프로젝트명 코드 조회
    project_list = Project().get_project_info()
    if project_list['result'] != 'fail' and project_list['count'] != 0:
        project_list = project_list['data']
    else:
        project_list = []

    # 업무 진행 상태 코드 조회
    work_state_code_list = Code().get_code_list('WKS0001')
    if work_state_code_list['result'] != 'fail' and work_state_code_list['count'] != 0:
        work_state_code_list = work_state_code_list['data']
    else:
        work_state_code_list = []

    # 결재자 정보 조회
    user_dict: dict = User().get_user_info(user_id)
    if user_dict['result'] != 'fail' and user_dict['count'] != 0:
        user_dict = user_dict['data'][0]
        payment_user_name: str = user_dict['PAYMENT_USER_NAME']
    else:
        user_dict: list = []
        payment_user_name: str = ''

    payment_dict: dict = dict()
    payment_dict['payment_user_name']: str = payment_user_name

    # 보고서 상태
    payment_progress_code_dict: dict = Code().get_code_name('RPS0001')
    if payment_progress_code_dict['result'] != 'fail' and payment_progress_code_dict['count'] != 0:
        payment_progress_code: str = payment_progress_code_dict['data'][0]['CODE_NAME']
    else:
        payment_progress_code: str = ''

    code_list: dict = dict()
    code_list['work_state_code_list']: list = work_state_code_list
    code_list['payment_progress_code']: str = payment_progress_code

    # 금주 일정 조회
    work_list = Work().get_work_info(user_id, thisweek_start_day, thisweek_end_day)
    if work_list['result'] != 'fail':
        work_list = work_list['data']
    else:
        work_list = []

    # 차주 계획 조회
    plan_list = Work().get_plan_info(user_id, nextweek_start_day, nextweek_end_day)
    if plan_list['result'] != 'fail':
        plan_list = plan_list['data']
    else:
        plan_list = []

    return render_template('/work/template_workReportInsert.html', menu_list=menu_list,
                           now_top_menu_code=now_top_menu_code, now_left_menu_code=now_left_menu_code,
                           user_name=user_name, day_info=day_info, work_list=work_list,
                           project_list=project_list, code_list=code_list,
                           plan_list=plan_list, payment_dict=payment_dict, user_dict=user_dict)

from flask import render_template, request, redirect, url_for
from app import app
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from collections import defaultdict

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
        page: str = search_word.get('page')
    else:
        page: str = '1'

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
    report_list = Report().get_report_list(search_list, page)
    if report_list['result'] != 'fail':
        report_total_count = report_list['total']
        report_list = report_list['data']
    else:
        report_total_count = 0
        report_list = []
    
    # 페이징 처리
    page_info = get_page_info(int(page), report_total_count)

    return render_template('/work/template_workReportSearch.html', menu_list=menu_list,
                           now_top_menu_code=now_top_menu_code, now_left_menu_code=now_left_menu_code,
                           report_state_list=report_state_list, report_list=report_list,
                           page_info=page_info, report_total_count=report_total_count)


# 업무 보고서 등록
@app.route('/work/report/insert')
@login_required
def work_report_insert():
    '''
    보고서를 등록하기를 요청한 사용자의 주간보고서 등록
    이전에 작성한 주간보고서가 존재할 경우 작성한 주간보고서 표출
    :return:
    '''
    now_user = current_user
    user_id = now_user.user_id
    user_name = now_user.user_name

    # 메뉴 조회
    menu_list = get_menu_list()
    now_top_menu_code = 'MENWRK'
    now_left_menu_code = 'MENWRK001'

    # 날짜 관련
    day_dict: dict = get_date_info()

    # 코드 관련
    code_dict: dict = get_report_code_info()

    # 보고서 관련
    report_dict: dict = dict()

    # 주간보고서 정보 조회
    user_dict: dict = User().get_user_info(user_id)
    if user_dict['result'] == 'fail' or user_dict['count'] == 0:
        return 'alert("존재하지 않은 사용자 입니다.");location.href="/";'
    user_dict = user_dict['data'][0]
    report_id = user_dict['THISWEEK_REPORT_ID']

    if report_id != '':
        return redirect(url_for('work_report_detail', report_id=report_id))

    # 금주 일정 조회
    work_list = Work().get_report_work_info(user_id, day_dict['thisweek_start_day'], day_dict['thisweek_end_day'])
    if work_list['result'] != 'fail':
        work_list = work_list['data']
    else:
        work_list = []

    # 차주 계획 조회
    plan_list = Work().get_report_plan_info(user_id, day_dict['nextweek_start_day'], day_dict['nextweek_end_day'])
    if plan_list['result'] != 'fail':
        plan_list = plan_list['data']
    else:
        plan_list = []

    auth_dict: dict = defaultdict(lambda: 'N')
    auth_dict['update_auth'] = 'Y'

    return render_template('/work/template_workReportInsert.html', menu_list=menu_list,
                           now_top_menu_code=now_top_menu_code, now_left_menu_code=now_left_menu_code,
                           user_name=user_name, day_dict=day_dict, work_list=work_list,
                           code_dict=code_dict, report_dict=report_dict, user_dict=user_dict,
                           plan_list=plan_list, auth_dict=auth_dict)


# 업무 보고서 상세정보 조회
@app.route('/work/report/detail')
@login_required
def work_report_detail():
    '''
    주간보고서 아이디로 상세정보 조회
    :return:
    '''
    now_user = current_user
    user_id = now_user.user_id

    # 메뉴 조회
    menu_list: dict = get_menu_list()
    now_top_menu_code = 'MENWRK'
    now_left_menu_code = 'MENWRK001'

    # 날짜 관련
    day_dict: dict = get_date_info()

    # 코드 관련
    code_dict: dict = get_report_code_info()

    # 보고서 관련
    report_id: str = request.args['report_id']

    report_dict: dict = Report().get_report_info(report_id)
    if report_dict['result'] == 'fail' or report_dict['count'] == 0:
        return 'alert("존재하지 않은 보고서 입니다.");location.href="/";'
    report_dict = report_dict['data'][0]

    user_name = report_dict['USER_NAME']
    report_user_id = report_dict['USER_ID']

    # 금주 일정 조회
    work_list = Work().get_report_work_info(report_user_id, report_dict['THISWEEK_START_DATETIME'], report_dict['THISWEEK_END_DATETIME'])
    if work_list['result'] != 'fail':
        work_list = work_list['data']
    else:
        work_list = []

    # 차주 계획 조회
    plan_list = Work().get_report_plan_info(report_user_id, report_dict['NEXTWEEK_START_DATETIME'], report_dict['NEXTWEEK_END_DATETIME'])
    if plan_list['result'] != 'fail':
        plan_list = plan_list['data']
    else:
        plan_list = []

    auth_dict: dict = defaultdict(lambda: 'N')
    # 보고서를 작성한 사용자인지 확인
    if user_id == report_dict['USER_ID'] and report_dict['PAYMENT_PROGRESS_CODE'] == 'RPS0001':
        auth_dict['update_auth'] = 'Y'
    # 결재자인지 확인
    if user_id == report_dict['PAYMENT_USER_ID']:
        auth_dict['payment_auth'] = 'Y'

    return render_template('/work/template_workReportInsert.html', menu_list=menu_list,
                           now_top_menu_code=now_top_menu_code, now_left_menu_code=now_left_menu_code,
                           user_name=user_name, day_dict=day_dict, work_list=work_list,
                           code_dict=code_dict, report_dict=report_dict,
                           plan_list=plan_list, auth_dict=auth_dict)


# 보고서 날짜 정보 조회
def get_date_info() -> dict:
    # 보고서 등록 일자 조회
    today_datetime: datetime = datetime.today()
    today: str = today_datetime.strftime("%Y-%m-%d %H:%M:%S")
    weekday: int = today_datetime.weekday()

    # 금주 날짜 계산
    thisweek_start_datetime: datetime = today_datetime - timedelta(days=weekday)
    thisweek_start_day: str = thisweek_start_datetime.strftime("%Y-%m-%d")
    thisweek_end_datetime: datetime = today_datetime + timedelta(days=(4 - weekday))
    thisweek_end_day: str = thisweek_end_datetime.strftime("%Y-%m-%d")

    # 차주 날짜 계산
    nextweek_start_datetime: datetime = thisweek_start_datetime + timedelta(days=7)
    nextweek_start_day: str = nextweek_start_datetime.strftime("%Y-%m-%d")
    nextweek_end_datetime: datetime = thisweek_end_datetime + timedelta(days=7)
    nextweek_end_day: str = nextweek_end_datetime.strftime("%Y-%m-%d")

    day_dict: dict = dict()
    day_dict['today'] = today
    day_dict['thisweek_start_day'] = thisweek_start_day
    day_dict['thisweek_end_day'] = thisweek_end_day
    day_dict['nextweek_start_day'] = nextweek_start_day
    day_dict['nextweek_end_day'] = nextweek_end_day

    return day_dict


# 보고서 관련 코드 정보 조회
def get_report_code_info() -> dict:
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

    code_dict: dict = dict()
    code_dict['project_list']: list = project_list
    code_dict['work_state_code_list']: list = work_state_code_list

    return code_dict

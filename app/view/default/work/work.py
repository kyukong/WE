from flask import render_template, redirect, request
from flask_login import current_user
from app import app
from flask_login import login_required

from app.model.common.model_menu import Menu
from app.model.common.model_code import Code
from app.model.work.model_project import Project
from app.model.work.model_work import Work

from app.view.default.common.basic import set_project_code_ALL, get_menu_list, get_page_info



# 20210913 KYB add 업무 검색 추가
@app.route('/work/search')
@login_required
def work_search():
    # 메뉴 조회
    menu_list = get_menu_list()
    now_top_menu_code = 'MENWRK'
    now_left_menu_code = 'MENWRK002'

    # 프로젝트명 코드 조회
    project_list = Project().get_project_info()
    if project_list['result'] != 'fail' and project_list['count'] != 0:
        project_list = project_list['data']
    else:
        project_list = []
    project_list = set_project_code_ALL(project_list)

    # 검색어 조회
    search_word = request.args
    search_list = dict()
    search_list['page'] = search_word.get('page')
    if search_word.get('page'):
        search_list['page'] = search_word.get('page')
    else:
        search_list['page'] = '1'

    if search_word:
        search_list['search_start_word_date'] = search_word.get('searchStartWorkDate')
        search_list['search_end_word_date'] = search_word.get('searchEndWorkDate')
        if search_word.get('searchProjectCode') == 'ALL':
            search_list['search_project_code'] = ''
        else:
            search_list['search_project_code'] = search_word.get('searchProjectCode')
        search_list['search_work_user_name'] = search_word.get('searchWorkUserName')
    else:
        search_list['search_start_word_date'] = ""
        search_list['search_end_word_date'] = ""
        search_list['search_project_code'] = ""
        search_list['search_work_user_name'] = ""
    
    # 업무 정보 조회
    work_list = Work().get_work_list(search_list)
    if work_list['result'] != 'fail':
        work_total_count = work_list['total']
        work_list = work_list['data']
    else:
        work_total_count = 0
        work_list = []
    
    # 페이징 처리
    page_info = get_page_info(int(search_list['page']), work_total_count)

    return render_template('/work/template_workSearch.html', menu_list=menu_list,
                            now_top_menu_code=now_top_menu_code, now_left_menu_code=now_left_menu_code,
                            project_list=project_list,
                            search_list=search_list, page_info=page_info,
                            work_list=work_list, work_total_count=work_total_count)


# 20210918 KYB add 업무 상세조회 추가
@app.route('/work/<day>')
@login_required
def work_detail(day):
    # 메뉴 조회
    menu_list = get_menu_list()
    now_top_menu = '/work/search'
    user_id = current_user.user_id

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
    
    # 20211004 KYB add 계획 정보 조회
    plan_list = Work().get_plan_info(user_id, day)
    if plan_list['result'] != 'fail':
        plan_list = plan_list['data']
    else:
        plan_list = []

    # 20211004 KYB add 업무 정보 조회
    work_list = Work().get_work_info(user_id, day)
    if work_list['result'] != 'fail':
        work_list = work_list['data']
    else:
        work_list = []

    code_list = dict()
    code_list['work_state_code_list'] = work_state_code_list

    return render_template('/work/template_workInsert.html', menu_list=menu_list, now_top_menu=now_top_menu, 
                        project_list=project_list, work_day=day, code_list=code_list,
                        plan_list=plan_list, work_list=work_list)


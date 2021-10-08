# 20210913 KYB add view 폴더 내에서 사용하는 기본 함수

from app.model.common.model_menu import Menu

from app.config import SEARCH



# 20210913 KYB add 프로젝트 코드 리스트에서 '전체' 값 추가 (일반 코드가 아닌 테이블이 존재하여 따로 생성)
def set_project_code_ALL(code_list):
    # PROJECT_ID, PROJECT_NAME, PROJECT_START_DATETIME, PROJECT_END_DATETIME, MEMO, 
    # INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME

    ALL_info = {
        "PROJECT_ID": 'ALL',
        "PROJECT_NAME": '전체',
        "PROJECT_START_DATETIME": '',
        "PROJECT_END_DATETIME": '', 
        "MEMO": '', 
        "INSERT_USER_ID": '',
        "INSERT_DATETIME": '',
        "UPDATE_USER_ID": '', 
        "UPDATE_DATETIME": ''
    }

    code_list.insert(0, ALL_info)

    return code_list


# 20210916 KYB add 메뉴 조회
def get_menu_list():
    menu_list = Menu().get_menu_list()
    if menu_list['result'] == 'fail':
        menu_list = None
    else:
        menu_list = menu_list['data']
    
    return menu_list


# 20210916 KYB add 페이징 처리
def get_page_info(now_page, total_result_count):
    search_page_count = SEARCH['SEARCH_PAGE_COUNT']
    search_result_count = SEARCH['SEARCH_RESULT_COUNT']

    # 첫번째 페이지
    if now_page % search_page_count > 0:
        first_page = (search_page_count * (now_page // search_page_count)) + 1
    else:
        first_page = (search_page_count * ((now_page // search_page_count) - 1)) + 1
    
    # 총 페이지
    if total_result_count % search_result_count > 0:
        total_page = (total_result_count // search_result_count) + 1
    else:
        total_page = total_result_count // search_result_count
    
    # 마지막 페이지
    last_page = min(first_page + (search_page_count - 1), total_page)

    page_info = dict()
    page_info['page'] = now_page
    page_info['first_page'] = first_page
    page_info['last_page'] = last_page

    return page_info



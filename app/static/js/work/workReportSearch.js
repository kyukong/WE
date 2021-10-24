
// 페이지 이동
function getPageWorkReportList(pageEle) {
    var page = pageEle.textContent;
    getSearchWorkReportList(page);
}

// 보고서 검색 검색어 조회
function getSearchWorkReportList(page='1') {
    var searchStartReportDate = document.getElementById("searchStartReportDate").value.trim();
    var searchEndReportDate = document.getElementById("searchEndReportDate").value.trim();
    var searchReportStateCode = document.getElementById("searchReportStateCode").value.trim();
    var searchReportUserName = document.getElementById("searchReportUserName").value.trim();

    var parameters = "";
    parameters += "page=" + page + "&";
    parameters += "searchStartReportDate=" + searchStartReportDate + "&";
    parameters += "searchEndReportDate=" + searchEndReportDate + "&";
    parameters += "searchReportStateCode=" + searchReportStateCode + "&";
    parameters += "searchReportUserName=" + searchReportUserName;

    getWorkReportList(parameters);
}

// 보고서 검색 API 호출
function getWorkReportList(parameters) {
    getPageGETMethod('/work/report/search', parameters);
}

// 보고서 상세조회 화면으로 이동
function getWorkReportDetailPage(selectedWorkReportInfo) {
    var workReportInfo = selectedWorkReportInfo;
    var reportID = workReportInfo.getAttribute('id');

    var url = '/work/report/detail';
    var parameters = 'report_id=' + reportID;

    getPageGETMethod(url, parameters);
}

// 보고서 등록 화면으로 이동
function getWorkReportInsertPage() {
    var url = '/work/report/insert';

    getPageGETMethod(url);
}
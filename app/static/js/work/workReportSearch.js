
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

// TODO 보고서 상세정보 조회 추가
//// 20211005 KYB add 업무 상세조회 화면으로 이동
//function getWorkDetailPage(selectedWorkInfo) {
//    var workInfo = selectedWorkInfo;
//    var workDay = workInfo.querySelector("#workDay").textContent;
//    var url = '/work/' + workDay;
//
//    getPageGETMethod(url);
//}
//

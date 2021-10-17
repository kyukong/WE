
// 20211013 KYB add 페이지 이동
function getPageWorkReportList(pageEle) {
    var page = pageEle.textContent;
    getSearchWorkList(page);
}

// 20211013 KYB add 보고서 검색 검색어 조회
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

// 20211013 KYB add 보고서 검색 API 호출
function getWorkReportList(parameters) {
    getPageGETMethod('/work/report/search', parameters);
}

//// 20211005 KYB add 업무 상세조회 화면으로 이동
//function getWorkDetailPage(selectedWorkInfo) {
//    var workInfo = selectedWorkInfo;
//    var workDay = workInfo.querySelector("#workDay").textContent;
//    var url = '/work/' + workDay;
//
//    getPageGETMethod(url);
//}
//

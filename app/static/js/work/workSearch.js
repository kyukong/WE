
// 20211007 KYB add 페이지 이동
function getPageWorkList(pageEle) {
    var page = pageEle.textContent;
    getSearchWorkList(page);
}

// 20210916 KYB add 업무 검색 검색어 조회
function getSearchWorkList(page='1') {
    var searchStartWorkDate = document.getElementById("searchStartWorkDate").value.trim();
    var searchEndWorkDate = document.getElementById("searchEndWorkDate").value.trim();
    var searchProjectCode = document.getElementById("searchProjectCode").value.trim();
    var searchWorkUserName = document.getElementById("searchWorkUserName").value.trim();
    
    var parameters = "";
    parameters += "page=" + page + "&";
    parameters += "searchStartWorkDate=" + searchStartWorkDate + "&";
    parameters += "searchEndWorkDate=" + searchEndWorkDate + "&";
    parameters += "searchProjectCode=" + searchProjectCode + "&";
    parameters += "searchWorkUserName=" + searchWorkUserName;

    getWorkList(parameters);
}

// 20210916 KYB add 업무 검색 API 호출
function getWorkList(parameters) {
    getPageGETMethod('/work/search', parameters);
}

// 20211005 KYB add 업무 상세조회 화면으로 이동
function getWorkDetailPage(selectedWorkInfo) {
    var workInfo = selectedWorkInfo;
    var workDay = workInfo.querySelector("#workDay").textContent;
    var url = '/work/' + workDay;

    getPageGETMethod(url);
}



// 20210904 KYB add GET 페이지 이동 함수
function getPageGETMethod(path, parameters="") {
    if (parameters == "") {
        location.href = path;
    } else {
        location.href = path + "?" + parameters;
    }
}

// 20210911 KYB add POST 페이지 이동 함수
function getPagePOSTMethod(path, formID) {
    if (isElementExist(formID)) {
        document.getElementById(formID).action = path;
        document.getElementById(formID).method = 'post';
        document.getElementById(formID).submit();
    }
}

// 20210910 KYB add 요소가 존재하는지 판단
function isElementExist(element) {
    if (element != 'undefined' && element != null) {
        return true;
    } else {
        return false;
    }
}

// 20210911 KYB add 요소가 빈값인지 판단
function isElementEmpty(element) {
    if (element != "") {
        return true
    } else {
        return false
    }
}

// 20210910 KYB add 클릭이벤트 등록
function addClickEvent(element, func) {
    if (isElementExist(element)) {
        element.addEventListener('onclick', func, false);
    } else {
        alert("요소가 존재하지 않음!");
    }
}

// 20210911 KYB add 엔터키 이벤트 등록
function addEnterEvent(func) {
    if (window.event.keyCode == 13) {
        func();
    }
}

// 20210912 KYB add 로그아웃
function logout() {
    getPageGETMethod('/logout');
}

// 20210913 KYB add 로고 클릭 시 메인화면으로 이동
function getMainPage() {
    getPageGETMethod("/main");
}

// 20210922 KYB add 문자열을 dom 객체로 생성하여 태그 추가
function setStringTag(parentEle, htmlString) {
    var createDiv = document.createElement('div');
    createDiv.innerHTML = htmlString.trim();

    // 20211002 KYB exp 임의로 추가한 div 태그를 같이 추가하지 않기 위해 자식노드 첫번째것을 추가
    parentEle.appendChild(createDiv.childNodes[0]);
}

// 20211004 KYB add API 호출
async function getAPI(url, method, body) {
    var option ={
        method: method,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json;charset=utf-8'
       },
       body: JSON.stringify(body)
    };

    try {
        var data;
        var response = await fetch(url, option);
        
        if (response.ok) {
            data = await response.json();
        } else {
            data = "error: " + response.status;
        }

        return data
    } catch(error) {
        return error
    }
}
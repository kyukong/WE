
// 20210911 KYB add 로그인 입력값 확인
function chkUserInfo() {
    var userID = document.getElementById('userID').value.trim();
    var userPW = document.getElementById("userPW").value.trim();
    var loginFormID = "loginForm";

    var loginResultText = document.getElementById("loginResultText");

    if (!isElementEmpty(userID)) {
        loginResultText.textContent = "아이디 값을 입력해주세요.";
        return;
    }
    if (!isElementEmpty(userPW)) {
        loginResultText.textContent = "비밀번호 값을 입력해주세요.";
        return;
    }

    getPagePOSTMethod("login/get_info", loginFormID);
}

// 20210913 KYB add 로그인 화면에서 로고 클릭 시 로그인 화면으로 이동
function getLoginPage() {
    getPageGETMethod("/");
}

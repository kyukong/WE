
// document 로드 시
document.addEventListener("DOMContentLoaded", function() {
})

// 20211002 KYB add 계획 일정 추가
function getPlanTable() {
    var planTableDiv = document.getElementById('planTableDiv');

    var html = "";
    html += '            <table class="row_table" data-oriflag=false>';
    html += '                <thead>';
    html += '                    <colgroup>';
    html += '                        <col style="width: 20%">';
    html += '                        <col style="width: 60%">';
    html += '                        <col style="width: 20%">';
    html += '                    </colgroup>';
    html += '                </thead>';
    html += '                <tbody>';
    html += '                    <tr>';
    html += '                        <th>프로젝트명</th>';
    html += '                        <td>';
    html += '                            <label for="project_code"></label>';
    html += '                            <select name="project_code" id="projectCode" class="input_select">'

    var projectInfo = '';
    for (var i = 0; i < projectList.length; i++) {
        projectInfo = projectList[i];
        html += '<option value="' + projectInfo['PROJECT_ID'] + '">' + projectInfo['PROJECT_NAME'] + '</option>';
    }

    html += '                            </select>';
    html += '                        </td>';
    html += '                        <td rowspan="3">';
    html += '                            <div class="center_column_button_wrap">';
    html += '                                <input type="button" value="업무 등록" onclick="setPlanTable(this)">';
    html += '                                <input type="button" value="계획 삭제" onclick="delInfoTable(this)">';
    html += '                            </div>';
    html += '                        </td>';
    html += '                    </tr>';
    html += '                    <tr>';
    html += '                        <th>계획</th>';
    html += '                        <td>';
    html += '                            <input type="text" id="plan" class="input_text">';
    html += '                        </td>';
    html += '                    </tr>';
    html += '                    <tr>';
    html += '                        <th>비고</th>';
    html += '                        <td>';
    html += '                            <textarea type="text" id="memo" class="input_text" rows="3"></textarea>';
    html += '                        </td>';
    html += '                    </tr>';
    html += '                </tbody>';
    html += '            </table>';

    setStringTag(planTableDiv, html);
}

// 20211002 KYB add 작성한 계획 업무 등록
function setPlanTable(btn) {
    var insertButtonElement = btn;
    var planTable = insertButtonElement.closest("table");

    var project = planTable.querySelector("#projectCode").value;
    var plan = planTable.querySelector("#plan").value;
    var memo = planTable.querySelector("#memo").value;

    getWorkTable(project, plan, memo);
}

// 20210922 KYB add 업무 일정 추가
function getWorkTable(project=false, plan=false, memo=false) {
    var workTableDiv = document.getElementById('workTableDiv');
    var workStateCodeList = codeList['work_state_code_list'];
    
    var html = "";
    html += '            <table class="row_table" data-oriflag=false>';
    html += '                <thead>';
    html += '                    <colgroup>';
    html += '                        <col style="width: 20%">';
    html += '                        <col style="width: 60%">';
    html += '                        <col style="width: 20%">';
    html += '                    </colgroup>';
    html += '                </thead>';
    html += '                <tbody>';
    html += '                    <tr>';
    html += '                        <th>프로젝트명</th>';
    html += '                        <td>';
    html += '                            <label for="project_code"></label>';
    html += '                            <select name="project_code" id="projectCode" class="input_select">';

    var projectInfo = "";
    for (var i = 0; i < projectList.length; i++) {
        projectInfo = projectList[i];
        if (project && project === projectInfo['PROJECT_ID']) {
            html += '<option value="' + projectInfo['PROJECT_ID'] + '" selected>' + projectInfo['PROJECT_NAME'] + '</option>';
        } else {
            html += '<option value="' + projectInfo['PROJECT_ID'] + '">' + projectInfo['PROJECT_NAME'] + '</option>';
        }
    }

    html += '                            </select>';
    html += '                        </td>';
    html += '                        <td rowspan="6">';
    html += '                            <div class="center_column_button_wrap">';
    html += '                                <input type="button" value="업무 삭제" onclick="delInfoTable(this)">';
    html += '                            </div>';
    html += '                        </td>';
    html += '                    </tr>';

    if (plan) {
        html += '                    <tr>';
        html += '                        <th>계획</th>';
        html += '                        <td>';
        html += '                            <input type="text" id="plan" class="input_text" value="' + plan + '">';
        html += '                        </td>';
        html += '                    </tr>';
    }

    html += '                    <tr>';
    html += '                        <th>진행여부</th>';
    html += '                        <td>';
    html += '                            <label for="work_state_code"></label>';
    html += '                            <select name="work_state_code" id="workStateCode" class="input_select">';

    var workStateCodeInfo = "";
    for (var i = 0; i < workStateCodeList.length; i++) {
        workStateCodeInfo = workStateCodeList[i];
        html += '<option value="' + workStateCodeInfo['CODE'] + '">' + workStateCodeInfo['CODE_NAME'] + '</option>';
    }

    html += '                            </select>';
    html += '                        </td>';
    html += '                    </tr>';
    html += '                    <tr>';
    html += '                        <th>진행사항</th>';
    html += '                        <td>';
    html += '                            <textarea type="text" id="workContent" class="input_text" rows="3"></textarea>';
    html += '                        </td>';
    html += '                    </tr>';
    html += '                    <tr>';
    html += '                        <th>지연사유</th>';
    html += '                        <td>';
    html += '                            <textarea type="text" id="delayContent" class="input_text" rows="3"></textarea>';
    html += '                        </td>';
    html += '                    </tr>';
    html += '                    <tr>';
    html += '                        <th>해결방안</th>';
    html += '                        <td>';
    html += '                            <textarea type="text" id="solutionContent" class="input_text" rows="3"></textarea>';
    html += '                        </td>';
    html += '                    </tr>';
    html += '                    <tr>';
    html += '                        <th>비고</th>';
    html += '                        <td>';
    html += '                            <textarea type="text" id="memo" class="input_text" rows="3">';

    if (memo) { html += memo; }

    html += '</textarea>';
    html += '                        </td>';
    html += '                    </tr>';
    html += '                    <tr>';
    html += '                        <th>산출물 업로드 경로</th>';
    html += '                        <td>';
    html += '                            <input type="text" id="ftpPath" class="input_text">';
    html += '                        </td>';
    html += '                    </tr>';
    html += '                </tbody>';
    html += '            </table>';

    setStringTag(workTableDiv, html);
}

// 20211002 KYB add 작성한 table 정보 삭제
function delInfoTable(btn) {
    var deleteButtonElement = btn;
    btn.closest("table").remove();
}

// 20211002 KYB add 업무를 등록하기 위해 계획, 업무 정보 조회
function getWorkInfo() {
    // 계획 정보 조회
    var planInsertInfoList = [];
    var planUpdateInfoList = [];
    var planTableList = document.getElementById("planTableDiv").children;
    var planTableInfo;

    var planInfo = {};
    var project_ID, plan, memo, planOriFlag;

    for (var i = 0; i < planTableList.length; i++) {
        planInfo = {};
        planTableInfo = planTableList[i];

        project_ID = planTableInfo.querySelector("#projectCode").value;
        plan = planTableInfo.querySelector("#plan").value;
        memo = planTableInfo.querySelector("#memo").value;

        planInfo['projectID'] = project_ID;
        planInfo['planDay'] = workDay;
        planInfo['plan'] = plan;
        planInfo['memo'] = memo;
        planInfo['planID'] = "";
        
        planOriFlag = planTableInfo.getAttribute('data-oriflag');
        if (planOriFlag == 'true') {
            planInfo['planID'] = planTableInfo.getAttribute('id');

            planUpdateInfoList.push(planInfo);
        } else {
            planInsertInfoList.push(planInfo);
        }
        
    }

    // 업무 정보 조회
    var workInsertInfoList = [];
    var workUpdateInfoList = [];
    var workTableList = document.getElementById("workTableDiv").children;
    var workTableInfo;

    var workInfo = {};
    var project_ID, workStateCode, workContent, delayContent, solutionContent, memo, ftpPath, workOriFlag;

    for (var i = 0; i < workTableList.length; i++) {
        workInfo = {};
        workTableInfo = workTableList[i];

        project_ID = workTableInfo.querySelector("#projectCode").value;
        workStateCode = workTableInfo.querySelector("#workStateCode").value;
        workContent = workTableInfo.querySelector("#workContent").value;
        delayContent = workTableInfo.querySelector("#delayContent").value;
        solutionContent = workTableInfo.querySelector("#solutionContent").value;
        memo = workTableInfo.querySelector("#memo").value;
        ftpPath = workTableInfo.querySelector("#ftpPath").value;

        workInfo['projectID'] = project_ID;
        workInfo['workStateCode'] = workStateCode;
        workInfo['workDay'] = workDay;
        workInfo['workContent'] = workContent;
        workInfo['delayContent'] = delayContent;
        workInfo['solutionContent'] = solutionContent;
        workInfo['memo'] = memo;
        workInfo['ftpPath'] = ftpPath;
        workInfo['workID'] = "";

        workOriFlag = workTableInfo.getAttribute('data-oriflag');
        if (workOriFlag == 'true') {
            workInfo['workID'] = workTableInfo.getAttribute('id');

            workUpdateInfoList.push(workInfo);
        } else {
            workInsertInfoList.push(workInfo);
        }
    }

    getWorkInsertAPI(planInsertInfoList, planUpdateInfoList, workInsertInfoList, workUpdateInfoList);
}

// https://ko.javascript.info/fetch
// https://developer.mozilla.org/ko/docs/Learn/JavaScript/Asynchronous/Async_await
// 20211002 KYB add 업무 등록 api 호출
function getWorkInsertAPI(planInsertInfoList, planUpdateInfoList, workInsertInfoList, workUpdateInfoList) {
    var url = "/api/v1/work/insert";
    var body = {
        "planInsertInfoList": planInsertInfoList,
        "planUpdateInfoList": planUpdateInfoList,
        "workInsertInfoList": workInsertInfoList,
        "workUpdateInfoList": workUpdateInfoList
    }

    getAPI(url, 'POST', body)
    .then((result) => {
        if (result['result'] != 'fail') {
            var url = "/work/" + workDay;
            getPageGETMethod(url);
        } else {
            alert("업무 등록에 실패하였습니다.");
        }
    })
}
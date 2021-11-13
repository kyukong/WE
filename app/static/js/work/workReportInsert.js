
// 삭제 리스트
var planDeleteInfoList = [];

// 계획 정보 추가
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
    html += '            <tr>';
    html += '              <th>계획일자</th>';
    html += '              <td>';
    html += '                <input type="text" id="planDate" class="input_text">';
    html += '              </td>';
    html += '            </tr>';
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

// 작성한 table 정보 삭제
function delInfoTable(btn, infoType=false) {
    var deleteButtonElement = btn;

    var infoTable = btn.closest("table");
    var infoId = infoTable.getAttribute("id");

    if (infoType && infoId !== null) {
        if (infoType === "plan") {
            planDeleteInfoList.push(infoId);
        } else if (infoType === "work") {
            workDeleteInfoList.push(infoId);
        }
    }

    infoTable.remove();
}

// 보고서 저장
function saveReport() {
    var reportInfo = getReportInfo();
    reportInfo['requestType'] = 'save';

    getReportInsertAPI(reportInfo);
}

// 보고서 보고
function approvalReport() {
    var reportInfo = getReportInfo();
    reportInfo['requestType'] = 'report';

    getReportInsertAPI(reportInfo);
}

// 보고서 정보 조회
function getReportInfo() {
    // 보고서 정보 조회
    var reportDict = {};

    var registerDatetime = document.getElementById('REGISTER_DATETIME').value;
    var paymentUserId = document.getElementById('PAYMENT_USER_ID').getAttribute('data-payment_user_id');

    var thisweekStartDatetime = dayInfo['thisweek_start_day'];
    var thisweekEndDatetime = dayInfo['thisweek_end_day'];
    var nextweekStartDatetime = dayInfo['nextweek_start_day'];
    var nextweekEndDatetime = dayInfo['nextweek_end_day'];

    reportDict['report_id'] = reportID;
    reportDict['registerDatetime'] = registerDatetime;
    reportDict['paymentUserId'] = paymentUserId;
    reportDict['thisweekStartDatetime'] = thisweekStartDatetime;
    reportDict['thisweekEndDatetime'] = thisweekEndDatetime;
    reportDict['nextweekStartDatetime'] = nextweekStartDatetime;
    reportDict['nextweekEndDatetime'] = nextweekEndDatetime;

    // 업무 정보 조회
    var workIDList = [];
    var workID;

    var workTableDiv = document.getElementById('workTableDiv');

    for (var i = 0; i < workTableDiv.childElementCount; i++) {
        workID = workTableDiv.children[i].getAttribute('id');
        workIDList.push(workID);
    }

    // 계획 정보 조회
    var planInsertInfoList = [];
    var planUpdateInfoList = [];
    var planTableList = document.getElementById("planTableDiv").children;
    var planTableInfo;

    var planInfo = {};
    var projectID, plan, memo, planOriFlag;

    for (var i = 0; i < planTableList.length; i++) {
        planInfo = {};
        planTableInfo = planTableList[i];

        planDate = planTableInfo.querySelector("#planDate").value.trim();

        if (planDate === '') {
            alert('계획일자를 입력해주세요.');
            return;
        }

        projectID = planTableInfo.querySelector("#projectCode").value;
        plan = planTableInfo.querySelector("#plan").value.trim();
        memo = planTableInfo.querySelector("#memo").value.trim();

        planInfo['projectID'] = projectID;
        planInfo['planDay'] = planDate;
        planInfo['plan'] = plan;
        planInfo['memo'] = memo;
        planInfo['planID'] = '';

        planOriFlag = planTableInfo.getAttribute('data-oriflag');
        if (planOriFlag == 'true') {
            planInfo['planID'] = planTableInfo.getAttribute('id');

            planUpdateInfoList.push(planInfo);
        } else {
            planInsertInfoList.push(planInfo);
        }
    }

    var returnData = {
        'reportDict': reportDict,
        'workIDList': workIDList,
        'planInsertInfoList': planInsertInfoList,
        'planUpdateInfoList': planUpdateInfoList,
        'planDeleteInfoList': planDeleteInfoList,
    };

    return returnData;
}

// 보고서 등록 API 호출
function getReportInsertAPI(body) {
    var url = '/api/v1/workReport/insert';

    getAPI(url, 'POST', body)
        .then((result) => {
            if (result['result'] != 'fail') {
                var url = "/work/report/insert";
                getPageGETMethod(url);
            } else {
                alert("보고서 저장에 실패하였습니다.");
            }
        })
        .catch((error) => {
            alert("api error: " + error);
        })
}

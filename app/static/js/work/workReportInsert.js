
// 20211007 KYB add 삭제 리스트 추가
var planDeleteInfoList = [];

// 20211013 KYB add 계획 일정 추가
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

// 20211002 KYB add 작성한 table 정보 삭제
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

// 보고서 등록 절차
// 1. 금주 업무 정보들 상태값, 시스템값 변경
// 2. 차주 계획 정보 저장
// 3. 보고서 테이블에 저장

// 업무 상세조회에서 업무 상태값 확인하여 수정할 수 없도록 활성화

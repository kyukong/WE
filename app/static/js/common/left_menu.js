
// 20210902 KYB add 좌측메뉴 선택 시 css 설정 변경 함수
// 20211011 KYB del 방식 변경으로 삭제
// function select_left_menu(selected_menu) {
//     var menu = selected_menu;
//     var menu_list = document.getElementsByClassName("li_left_menu");
//     var menu_count = menu_list.length;
    
//     for (var i = 0; i < menu_count; i++) {
//         menu_list[i].classList.remove("on");
//     }

//     menu.classList.add("on");
// }

// 20211011 KYB add 좌측메뉴 클릭 시 해당 url 로 이동
function getLeftMenuPage(selected_menu) {
    var menu = selected_menu;
    var url = menu.getAttribute('data-url');

    getPageGETMethod(url);
}

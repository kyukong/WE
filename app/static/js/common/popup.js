
document.addEventListener("DOMContentLoaded", () => {
    // 팝업창 close
    var closeDivEle = document.getElementsByClassName('popup_close');
    for (var closeBtn of closeDivEle) {
        closeBtn.addEventListener('click', function(event) {
            this.closest('.popup').classList.remove('on');
        });
    }
});
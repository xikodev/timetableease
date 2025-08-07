function putShiftBtn() {
    var shiftBtn = '<a class="shift" href="/home/b/">B</a><a class="shift" href="/home/a/">A</a>'
    document.getElementById('buttons').innerHTML += shiftBtn
}

function putBackBtn(redirectPage) {
    var imageLocation = '/static/images/back-solid.png';
    var backBtn1 = '<a id="back" href="/';
    var backBtn2 = '/"><img src="';
    var backBtn3 = '" alt="↶"></a>';
    document.getElementById('buttons').innerHTML += backBtn1 + redirectPage + backBtn2 + imageLocation + backBtn3;
}

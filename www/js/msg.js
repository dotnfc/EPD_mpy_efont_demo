/**
 * 提示框支持
 */

var msgTimerId = -1;

// ES6 browser required
function showMessage(icoClass, bgClass, msgTitle, msgBody) {

    if (msgTimerId != -1)
        clearTimeout(msgTimerId);
    sbody = `<strong><span class="qi-ico-${icoClass}"></span>&nbsp;${msgTitle}</strong>&nbsp;${msgBody}`;
    $('#msgBody').html(sbody);

    sDivClass = `msgbox alert show fade alert-${bgClass}`;
    $('#msgDiv').removeClass().addClass(sDivClass);
    $('#msgDiv').show();

    msgTimerId = setTimeout(function() {
        $('#msgDiv').hide();
    }, 3000);
}

function showSuccess(msgTitle, msgBody) {
    showMessage("checkcirclefill", "success", msgTitle, msgBody);
}

function showFailed(msgTitle, msgBody) {
    showMessage("crosscirclefill", "danger", msgTitle, msgBody);
}

function showQuestion(msgTitle, msgBody) {
    showMessage("questioncirclefillefill", "warning", msgTitle, msgBody);
}

function showInfo(msgTitle, msgBody) {
    showMessage("infocirclefill", "secondary", msgTitle, msgBody);
}

function showExclamation(msgTitle, msgBody) {
    showMessage("exclamationcirclefill", "danger", msgTitle, msgBody);
}

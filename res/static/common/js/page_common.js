/**
 * 获取Cookie
 */
function getCookie(name) {
    var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return c ? c [ 1 ] : undefined;
}

function doRefresh() {
    window.location.reload();
}

function doBack() {
    history.back();
}

function toPage(url) {
    top.location.href = decodeURIComponent(url);
}

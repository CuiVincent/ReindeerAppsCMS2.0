/**
 * 获取Cookie
 */
function getCookie(name) {
    var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return c ? c [ 1 ] : undefined;
}

function getTopWindow() {
    var page = self;
    while (!(page.window.isTopWindow == true)) {
        page = page.parent;
    }
    return page;
}

function addEvent(obj, evt, func) {
    if (obj.addEventListener) {
        obj.addEventListener(evt, func, false);
    }
    else if (obj.attachEvent) {
        obj.attachEvent('on' + evt, func);
    }
}

function doRefresh() {
    window.location.reload();
}

function doBack() {
    history.back();
}

function toPage(url) {
    getTopWindow().location.href = url;
}

function toContent(aid, url) {
    getTopWindow().setContent(aid, url);
}

function onPageLoadFinish(){
    getTopWindow().initIFrameHeight();
}
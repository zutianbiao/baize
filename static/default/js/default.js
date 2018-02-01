/**
 * 本文件定义一些通用的方法 
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function printMsg(msg, level) {
    if (level == 'error') {
        setTimeout(function() {
            toastr.options = {
                closeButton: true,
                progressBar: true,
                showMethod: 'slideDown',
                timeOut: 4000
            };
            toastr.error(msg, 'Error');
        },
        1300);
    } else {
        setTimeout(function() {
            toastr.options = {
                closeButton: true,
                progressBar: true,
                showMethod: 'slideDown',
                timeOut: 4000
            };
            toastr.success(msg, 'Success');
        },
        1300);
    }
}
$.ajaxSetup({
    type: 'POST',
    //默认请求方式为post
    timemout: 1800,
    //默认请求超时时间
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
    error: function(e) { //默认ajax错误时的处理
        printMsg('数据加载失败！', 'error');
    },
    complete: function(xhr, response) {
        if (xhr.getResponseHeader('Timeout') == 'true' || response == '403') {
            window.location.href = "/web/403.html";
            return;
        }
    }
});
/**
 * 增加标签页
 */
function addTab(options) {
    //option:
    //tabMainName:tab标签页所在的容器
    //tabContentMainName:tab内容标签页所在的容器
    //tabName:当前tab的名称
    //tabTitle:当前tab的标题
    //tabUrl:当前tab所指向的URL地址
    //tabmainHeight:当前tab的高度
    var exists = checkTabIsExists(options.tabMainName, options.tabName);

    if (exists) {
        $("#tab_a_" + options.tabName).click();
    } else {
        $("#" + options.tabMainName).append('<li id="tab_li_' + options.tabName + '"><a href="#tab_content_' + options.tabName + '" data-toggle="tab" id="tab_a_' + options.tabName + '"><button class="close closeTab" type="button" onclick="closeTab(this);">×</button>' + options.tabTitle + '</a></li>');
        //固定TAB中IFRAME高度
        if(typeof(options.tabmainHeight)=="undefined"){
            mainHeight = $(document.body).height() - 5;
        }else{
            mainHeight = options.tabmainHeight
        }

        var content = '';
        if (options.content) {
            content = options.content;
        } else {
            content = '<iframe src="' + options.tabUrl + '" width="100%" height="' + mainHeight + 'px" frameborder="no" border="0" marginwidth="0" marginheight="0" scrolling="yes" allowtransparency="yes"></iframe>';
            $("#" + options.tabContentMainName).append('<div id="tab_content_' + options.tabName + '" role="tab-pane" class="tab-pane white-bg" id="' + options.tabName + '">' + content + '</div>');
            $("#tab_a_" + options.tabName).click();
        }
    }
}
function set_active(e,y) {
    if(y){
        e.attr("class","active");
    }else{
        e.attr("class","");
    }
}
$(".navbar-option").hover()

/**
 * 关闭标签页
 * @param button
 */
function closeTab(button) {

    //通过该button找到对应li标签的id
    var li_id = $(button).parent().parent().attr('id');
    var ul_id = $("#" + li_id).parent().attr('id');
    var id = li_id.replace("tab_li_", "");

    //关闭TAB
    $("#" + li_id).remove();
    $("#tab_content_" + id).remove();
    $("#"+ul_id).children().last().find("a").click()
}

/**
 * 判断是否存在指定的标签页
 * @param tabMainName
 * @param tabName
 * @returns {Boolean}
 */
function checkTabIsExists(tabMainName, tabName) {
    var tab = $("#" + tabMainName + " > #tab_li_" + tabName);
    //console.log(tab.length)
    return tab.length > 0;
}
function sleep(n) { //n表示的毫秒数
    var start = new Date().getTime();
    while (true) if (new Date().getTime() - start > n) break;
}

$(document).ready(function() {
    function set_active(e,y) {
        if(y){
            e.addClass("active");
        }else{
            e.removeClass("active");
        }
    }
    $(".navbar-option").click(function(){
        var e = $(this).parent()
        $(".metismenu > li.active").removeClass("active");
        set_active(e,true);
    });
});
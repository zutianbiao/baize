$(document).ready(function() {
    function set_active(e,y) {
        if(y){
            e.addClass("active");
        }else{
            e.removeClass("active");
        }
    }
    function sleep(n) { //n表示的毫秒数
        var start = new Date().getTime();
        while (true) if (new Date().getTime() - start > n) break;
    }
    $(".navbar-option").click(function(){
        var e = $(this).parent()
        $(".metismenu > li.active").removeClass("active");
        set_active(e,true);
    });

    function strip(str)
    {
        return str.replace(/(^\s*)|(\s*$)/g, "");
    }
    $(".navbar-option").click(function(){
        mainHeight = $(document.body).height() -5;
        $("#page-content").attr("height",mainHeight);
        $("#page-content").attr("src",strip($(this).attr("option")));
    });
    mainHeight = $(document.body).height() -5;
    $("#page-content").attr("height",mainHeight);
    $("#page-content").attr("src","/web/network_detect/role/index/");
});
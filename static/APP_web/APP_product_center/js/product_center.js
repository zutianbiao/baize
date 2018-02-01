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
    $("#page-content").attr("src","/web/work_manage/");
});
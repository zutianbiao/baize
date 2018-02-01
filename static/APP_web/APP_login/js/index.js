$(document).ready(function() {
    setTimeout(function() {
        toastr.options = {
            closeButton: true,
            progressBar: true,
            showMethod: 'slideDown',
            timeOut: 4000
        };
        toastr.success(MSG_USAGE, MSG_WELCOME);
    }, 1300);
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
    $("#page-content").attr("src","/web/product_center/");
});
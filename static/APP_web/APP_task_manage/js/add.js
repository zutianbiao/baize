function contains(arr, obj) {
    var i = arr.length;
    while (i--) {
        if (arr[i] === obj) {
            return true;
        }
    }
    return false;
}
function move_down(id){
    if($("#"+id).next())
        $("#"+id).next().after($("#"+id));
}
function move_up(id){
    if($("#"+id).prev())
        $("#"+id).prev().before($("#"+id));
}
function do_add_work(work_id, work_name, check_true){
    var check = '';
    if(check_true){
        check = 'checked';
    }
    var timestamp=new Date().getTime();
    var html='<li class="success-element" id="raw-parameter-' + timestamp +'"'+'work_id="' + work_id +'"' +'>'+
       '<div class="col-lg-3 col-md-3 col-sm-3 pull-left">'+
       '   <label class="pull-right padding-top-7" >'+
       '       <span class="red-content padding-5">作业</span><label><input id="checkbox_work_'+work_id+'" type="checkbox" class="i-checks" '+check+' >  向上依赖</label>'+
       '   </label>'+
       ' </div>'+
       ' <div class="col-lg-9 col-md-9 col-sm-9 pull-left">'+
       ' <div class="col-lg-4 col-md-4 col-sm-4 padding-5"></div>'+
       ' <div class="col-lg-5 col-md-5 col-sm-5 padding-5"><a class="btn btn-primary">'+ work_name +'</a></div>'+
       ' <div class="col-lg-3 col-md-3 col-sm-3 padding-5">'+
       '<a class="btn btn-primary" onclick="move_down(\'raw-parameter-'+ timestamp +'\')" ><i class="fa fa-arrow-down"></i></a>'+
       '<a class="btn btn-warning" onclick="move_up(\'raw-parameter-'+ timestamp +'\')" ><i class="fa fa-arrow-up"></i></a>'+
	   '<a class="btn btn-danger close-btn-work" option="raw-parameter-'+ timestamp +'" id="close-btn-work"><i class="fa fa-times"></i></a>'+
	'</div></div></div></li>';
    $("#add_work_and_task_content").append(html);
    $('.i-checks').iCheck({
    checkboxClass: 'icheckbox_square-green',
    radioClass: 'iradio_square-green'
    });
    $(".close-btn-work").click(function(){
    var name = $(this).attr("option");
    $("#"+name).remove();
    });
}
$(document).ready(function(){
    $('.summernote').summernote({
        minHeight: 300,
        lang:'zh-CN'
    });
$(".touchspin1").TouchSpin({
    min: 1,
    max: 10,
    buttondown_class: 'btn btn-white',
    buttonup_class: 'btn btn-white'
});
$('.i-checks').iCheck({
    checkboxClass: 'icheckbox_square-green',
    radioClass: 'iradio_square-green'
});
var config = {
    '.chosen-select': {
        search_contains: true
    },
    '.chosen-select-deselect': {
        allow_single_deselect: true
    },
    '.chosen-select-no-single': {
        disable_search_threshold: 10
    },
    '.chosen-select-no-results': {
        no_results_text: 'Oops, nothing found!'
    },
    '.chosen-select-width': {
        width: "50%"
    }
}
for (var selector in config) {
    $(selector).chosen(config[selector]);
}
$("#add_work").click(function(){
    do_add_work($('#work_list option:selected').val(), $('#work_list option:selected').text(), false);
});
$('#btn_task_save').click(function () {
    var task_name_cn = $('#name_cn').val();
    var task_name_en = $('#name_en').val();
    var time_auto_exec = $('#time_auto_exec').val();
    var task_desc = $('#desc').summernote('code');
    var list_works = [];
    $('#add_work_and_task_content').children('li').each(function () {
        var work_id = $(this).attr('work_id');
        var check = $('#checkbox_work_'+work_id).is(':checked');
        if(contains(list_works,work_id) == false){
            list_works.push({
                "id": work_id,
                "check_true": check
            });
        }
     });
    $.ajax({
        type : 'POST',
        url: "/web/configure_manage/task/save",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "name_cn": task_name_cn,
            "name_en": task_name_en,
            "desc": task_desc,
            "works": JSON.stringify(list_works),
            "time_auto_exec": time_auto_exec,
        },
        success : function(result){
            if(result.success){
                parent.parent.printMsg(result.msg,'Success');
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
    });
});
$('#time_auto_exec').datetimepicker({
    format: 'Y-m-d H:i',
    formatDate: 'Y-m-d',
    formatTime: 'H:i',
});
$.datetimepicker.setLocale('zh');

});

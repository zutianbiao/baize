$(document).ready(function(){
    $('#name_cn').val(task.name_cn);
    $('#name_cn').attr("disabled", true);
    $('#name_en').val(task.name_en);
    $('#name_en').attr("disabled", true);
    $('#time_auto_exec').val(task.time_auto_exec);
    $('#time_auto_exec').attr("readonly", true);
    $('#desc').summernote('reset');
    $('#desc').summernote('code', task.desc);
    for(var w in task.works){
        eval('do_add_work')(task.works[w].id, task.works[w].name, task.works[w].check_true);
    }
    $('#time_auto_exec').dblclick(function () {
        $(this).attr("readonly",false);
    });
    $('#time_auto_exec').change(function () {
        $(this).attr("readonly",true);
    });
});
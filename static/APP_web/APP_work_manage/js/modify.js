$(document).ready(function(){
    $('#name_cn').val(work.name_cn);
    $('#name_cn').attr("disabled", true);
    $('#name_en').val(work.name_en);
    $('#name_en').attr("disabled", true);
    $('#timeout').val(work.timeout);
    if(work.sync){
        $('#sync').iCheck('check');
    }else{
        $('#sync').iCheck('uncheck');
    }
    $('#desc').summernote('reset');
    $('#desc').summernote('code', work.desc);
    for(var j in work.jobs){
        if(work.jobs[j].type=='copy'){
            eval('add_action_'+work.jobs[j].type)(work.jobs[j].id, work.jobs[j].name, work.jobs[j].dest, work.jobs[j].authority, work.jobs[j].check_change, work.jobs[j].ignore_error);
        }else if(work.jobs[j].type=='script'){
            eval('add_action_'+work.jobs[j].type)(work.jobs[j].id, work.jobs[j].name, work.jobs[j].args, work.jobs[j].ignore_error);
        }else{
            eval('add_action_'+work.jobs[j].type)(work.jobs[j].id, work.jobs[j].name, work.jobs[j].ignore_error);
        }
    }
    add_env_test(work.test_tag.id, work.test_tag.name);
    for(var t in work.tags){
        add_env_online(work.tags[t].id, work.tags[t].name);
    }
    $('#checkbox_copy_with_pass').on( 'ifUnchecked', function () {
        $('#div_copy_url_with_pass').css('display', 'none');
    });
    $('#checkbox_copy_with_pass').on( 'ifChecked', function () {
        $('#div_copy_url_with_pass').css('display', '');
    });
});
function query_alarm_template(id) {
    $.ajax({
        type : 'POST',
        url: "/web/alarm_manage/alarm/query_alarm_template",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": id,
        },
        success : function(result){
            if(result.success){
                $('#alarm_template_name').val(result.data.name);
                $('#alarm_template_combine_period').val(result.data.combine_period);
                $('#alarm_template_key_string').val(result.data.key_string);
                $('#alarm_template_content').val(result.data.content);
                if(result.data.combine){
                    $('#alarm_template_combine').iCheck('check');
                }else{
                    $('#alarm_template_combine').iCheck('uncheck');
                }
                $('#alarm_template_id').val(result.data.id);
                $('#div_alarm_template_id').css('display', 'block');
                show_alarm_template_add(true);
                parent.parent.printMsg(result.msg,'Success');
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
    });
}
function add_alarm_template() {
    var alarm_id = $('#alarm_id').val();
    if(alarm_id){
        var alarm_template_name = $('#alarm_template_name').val();
        var alarm_template_combine = $('#alarm_template_combine').is(':checked');
        var alarm_template_combine_period = $('#alarm_template_combine_period').val();
        var alarm_template_key_string = $('#alarm_template_key_string').val();
        var alarm_template_content = $('#alarm_template_content').val();
        $.ajax({
            type : 'POST',
            url: "/web/alarm_manage/alarm/add_alarm_template",
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            data: {
                "alarm_id": alarm_id,
                "name": alarm_template_name,
                "combine": alarm_template_combine,
                "combine_period": alarm_template_combine_period,
                "key_string": alarm_template_key_string,
                "content": alarm_template_content,
            },
            success : function(result){
                if(result.success){
                    var html_btn = '<button type="button" class="btn btn-primary" onclick="query_alarm_template('+result.data.id+')">'+result.data.name+'</button>';
                    $('#alarm_template_id').val(result.data.id);
                    $('#div_alarm_template_id').css('display', 'block');
                    $('#div_alarm_manage_alarm_template').append(html_btn);
                    parent.parent.printMsg(result.msg,'Success');
                }else{
                    parent.parent.printMsg(result.msg,'error');
                }
            }
        });
    }else{
        parent.parent.printMsg('请先保存报警器基本信息','error');
    }
}
function add_alarm_person() {
    var alarm_id = $('#alarm_id').val();
    if(alarm_id){
        var alarm_person_id = $('#select_alarm_person option:selected').val();
        $.ajax({
            type : 'POST',
            url: "/web/alarm_manage/alarm/add_alarm_person",
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            data: {
                "alarm_id": alarm_id,
                "alarm_person_id": alarm_person_id,
            },
            success : function(result){
                if(result.success){
                    var html_btn = '<button type="button" class="btn btn-primary" >'+result.data.name+'</button>'
                    $('#div_alarm_manage_alarm_person').append(html_btn);
                    parent.parent.printMsg(result.msg,'Success');
                }else{
                    parent.parent.printMsg(result.msg,'error');
                }
            }
        });
    }else{
        parent.parent.printMsg('请先保存报警器基本信息','error');
    }
}
function save_alarm() {
    var name_cn = $('#alarm_name_cn').val();
    var name_en = $('#alarm_name_en').val();
    var desc = $('#alarm_desc').summernote('code');
    var method = $('#select_alarm_method option:selected').val();
    $.ajax({
        type : 'POST',
        url: "/web/alarm_manage/alarm/save",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "name_cn": name_cn,
            "desc": desc,
            "method": method,
            'name_en': name_en
        },
        success : function(result){
            if(result.success){
                $('#alarm_id').val(result.data.id);
                $('#div_alarm_id').css('display', 'block');
                $('#alarm_name_cn').attr('disabled', 'true');
                $('#alarm_name_en').attr('disabled', 'true');
                parent.parent.printMsg(result.msg,'Success');
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
    });
}
function show_alarm_person_add(tag) {
    if(tag){
        $('#div_add_alarm_person').css('display', 'block');
        $('#btn_add_alarm_person').text('关闭');
        $('#btn_add_alarm_person').attr('onclick', 'show_alarm_person_add(false)')
    }else{
        $('#div_add_alarm_person').css('display', 'none');
        $('#btn_add_alarm_person').text('添加');
        $('#btn_add_alarm_person').attr('onclick', 'show_alarm_person_add(true)')
    }

}
function show_alarm_template_add(tag) {
    if(tag){
        $('#div_add_alarm_template').css('display', 'block');
        $('#btn_add_alarm_template').text('关闭');
        $('#btn_add_alarm_template').attr('onclick', 'show_alarm_template_add(false)')
    }else{
        $('#div_add_alarm_template').css('display', 'none');
        $('#btn_add_alarm_template').text('添加');
        $('#btn_add_alarm_template').attr('onclick', 'show_alarm_template_add(true)')
    }

}
$(document).ready(function(){
    $('#alarm_desc').summernote({
        height: 130,
        maxHeight: 700
    });
    $(".touchspin1").TouchSpin({
        min: 1,
        max: 60,
        buttondown_class: 'btn btn-white',
        buttonup_class: 'btn btn-white'
    });
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
    });
    var config = {
        '.chosen-select-inner': {
            search_contains: true,
            width: "100%"
        },
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
    var alarm_desc = '';
    $('#alarm_desc').summernote('reset');
    $('#alarm_desc').summernote('code', alarm_desc);
});
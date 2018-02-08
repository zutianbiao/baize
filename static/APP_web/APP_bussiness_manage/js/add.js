function add_person() {
    var bussiness_id = $('#bussiness_id').val();
    if(bussiness_id){
        var user_id = $('#select_people option:selected').val();
        $.ajax({
            type : 'POST',
            url: "/web/bussiness_manage/add_person",
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            data: {
                "bussiness_id": bussiness_id,
                "user_id": user_id,
            },
            success : function(result){
                if(result.success){
                    var html_btn = '<button type="button" class="btn btn-primary" >'+result.data.username+'</button>'
                    $('#div_people').append(html_btn);
                    parent.parent.printMsg(result.msg,'Success');
                }else{
                    parent.parent.printMsg(result.msg,'error');
                }
            }
        });
    }else{
        parent.parent.printMsg('请先保存业务基本信息','error');
    }
}
function add_btn() {
    var bussiness_id = $('#bussiness_id').val();
    if(bussiness_id){
        var btn_desc = $('#btn_desc').val();
        var type = $('#select_bind_type option:selected').val();
        if(type=='work'){
            var work_id = $('#select_work option:selected').val();
            var task_id = '';
        }else{
            var work_id = '';
            var task_id = $('#select_task option:selected').val();
        }
        $.ajax({
            type : 'POST',
            url: "/web/bussiness_manage/add_btn",
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            data: {
                "bussiness_id": bussiness_id,
                "name": btn_desc,
                "work_id": work_id,
                "task_id": task_id,
                'type': type
            },
            success : function(result){
                if(result.success){
                    var html_btn = '<button type="button" class="btn btn-primary" onclick="do_btn(\''+result.data.type+'\','+result.data.id+')">'+result.data.name+'</button>'
                    $('#div_bussiness_manage_btns').append(html_btn);
                    parent.parent.printMsg(result.msg,'Success');
                }else{
                    parent.parent.printMsg(result.msg,'error');
                }
            }
        });
    }else{
        parent.parent.printMsg('请先保存业务基本信息','error');
    }
}
function save_bussiness() {
    var name_cn = $('#bussiness_name_cn').val();
    var name_en = $('#bussiness_name_en').val();
    var desc = $('#bussiness_desc').summernote('code');
    $.ajax({
        type : 'POST',
        url: "/web/bussiness_manage/save",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "name_cn": name_cn,
            "desc": desc,
            'name_en': name_en
        },
        success : function(result){
            if(result.success){
                $('#bussiness_id').val(result.data.id);
                $('#div_bussiness_id').css('display', 'block');
                $('#bussiness_name_cn').attr('disabled', 'true');
                $('#bussiness_name_en').attr('disabled', 'true');
                parent.parent.printMsg(result.msg,'Success');
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
    });
}
function show_btns_add(tag) {
    if(tag){
        $('#div_add_btns').css('display', 'block');
        $('#btn_add_btns').text('关闭');
        $('#btn_add_btns').attr('onclick', 'show_btns_add(false)')
    }else{
        $('#div_add_btns').css('display', 'none');
        $('#btn_add_btns').text('添加');
        $('#btn_add_btns').attr('onclick', 'show_btns_add(true)')
    }

}
function show_add_people(tag){
    if(tag){
        $('#div_add_people').css('display', 'block');
        $('#btn_add_people').text('关闭');
        $('#btn_add_people').attr('onclick', 'show_add_people(false)')
    }else{
        $('#div_add_people').css('display', 'none');
        $('#btn_add_people').text('添加');
        $('#btn_add_people').attr('onclick', 'show_add_people(true)')
    }
}
$(document).ready(function(){
    $('#bussiness_desc').summernote({
        height: 130,
        maxHeight: 700
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
    var bussiness_desc = '';
    $('#bussiness_desc').summernote('reset');
    $('#bussiness_desc').summernote('code', bussiness_desc);
    $('#select_bind_type').change(function () {
        var type = $('#select_bind_type option:selected').val();
        if(type=='work'){
            $('#div_select_work').css('display', 'block');
            $('#div_select_task').css('display', 'none');
        }else{
            $('#div_select_work').css('display', 'none');
            $('#div_select_task').css('display', 'block');
        }
    });
});
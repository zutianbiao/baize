var wait=0;
var waiting=false;
function time(type, id, timestamp) {
    $.ajax({
        type : 'POST',
        url: "/web/configure_manage/"+type+"/query_status_detail",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": id,
            "timestamp": timestamp,

        },
        success : function(result){
            if(result.success){
                $('#pre_btn_result').html();
                $('#pre_btn_result').css('display', 'block');
                if(result.data.length!=0) {
                    if(waiting){
                        $('#span_waiting').remove();
                    }
                    for (var i in result.data) {
                        $('#pre_btn_result').append('<span class="red-content">root@' + result.data[i].agent + '# </span> ' + '执行作业<' + result.data[i].work_name + '>\n');
                        $('#pre_btn_result').append(result.data[i].msg + '\n');
                    }
                    waiting=false;
                }else{
                    if(waiting){
                        $('#span_waiting').remove();
                        $('#pre_btn_result').append('<span class="green-content" id="span_waiting">========'+result.end.msg+'('+wait+')========'+'</span>');
                    }else{
                        $('#pre_btn_result').append('<span class="green-content" id="span_waiting">========'+result.end.msg+'('+wait+')========'+'</span>');
                    }
                    waiting=true;
                }
                if(result.end.tag){
                    if(waiting){
                        $('#span_waiting').remove();
                    }
                    $('#pre_btn_result').append('\n'+'======== 作业执行结束,执行结果：<'+result.end.msg + '>========'+ '\n');
                    $('#btn_status_detail').remove();
                    $('#div_btn_result').append('<button type="button" id="btn_status_detail" class="btn btn-primary" onclick="status_detail(\''+type+'\','+id+')">详情</button>');
                    if(result.end.status==2){
                        $('#btn_do_online').remove();
                        $('#div_btn_result').append('<button type="button" id="btn_do_online" class="btn btn-warning" onclick="do_btn_online(\''+type+'\','+id+')">上线</button>');
                    }
                    wait = 0;
                    waiting=false;
                }else{
                    wait++;
                    setTimeout(function() {
                        time(type, id, result.timestamp)
                    }, 1000)
                }
                $('#pre_btn_result').scrollTop($('#pre_btn_result').prop('scrollHeight'));
            }else{
                parent.parent.printMsg('查询结果失败','error');
            }
        }
    });
}
function status_detail(type, id){
    var options={
        "tabMainName": "add_bussiness_nav_tabs",
        "tabContentMainName": "add_bussiness_tab_content",
        "tabName": "tab_bussiness_status_detail"+id,
        "tabTitle": "结果详情",
        "tabUrl": "/web/"+type+"_manage/status_detail?id="+id,
        "tabmainHeight": $(document.body).height()*2
    };
    console.log(options);
    parent.addTab(options);
}
function do_btn_online(type, id) {
    if(type=='work'||type=='task'){
        var timestamp = parseInt(new Date().getTime() / 1000);
        $.ajax({
            type : 'POST',
            url: "/web/configure_manage/"+type+"/online",
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            data: {
                "id": id,
            },
            success : function(result){
                if(result.success){
                    time(type, id, 0);
                    parent.parent.printMsg(result.msg,'Success');
                }else{
                    parent.parent.printMsg(result.msg,'error');
                }
            }
        });
    }else{
        parent.parent.printMsg('执行参数异常','error');
    }
}
function do_btn_test(type, id) {
    if(type=='work'||type=='task'){
        var timestamp = parseInt(new Date().getTime() / 1000);
        $.ajax({
            type : 'POST',
            url: "/web/configure_manage/"+type+"/test",
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            data: {
                "id": id,
            },
            success : function(result){
                if(result.success){
                    time(type, id, 0);
                    parent.parent.printMsg(result.msg,'Success');
                }else{
                    parent.parent.printMsg(result.msg,'error');
                }
            }
        });
    }else{
        parent.parent.printMsg('执行参数异常','error');
    }
}
$(document).ready(function() {
    $('#bussiness_id').val(bussiness.id);
    $('#div_bussiness_id').css('display', 'block');
    $('#bussiness_name_cn').val(bussiness.name_cn);
    $('#bussiness_name_cn').attr('disabled', 'true');
    $('#bussiness_name_en').val(bussiness.name_en);
    $('#bussiness_name_en').attr('disabled', 'true');
    $('#bussiness_desc').summernote('reset');
    $('#bussiness_desc').summernote('code', bussiness.desc);
});
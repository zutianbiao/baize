function use_upload_file(tag) {
    if(tag){
        $('#remote_control_copy_source').attr('type', 'file');
        $('#a_remote_control_copy_source').text('填写地址');
        $('#a_remote_control_copy_source').attr('onclick', 'use_upload_file(false)')
    }else{
        $('#remote_control_copy_source').attr('type', 'text');
        $('#a_remote_control_copy_source').text('上传文件');
        $('#a_remote_control_copy_source').attr('onclick', 'use_upload_file(true)')
    }

}
function contains(arr, obj) {
    var i = arr.length;
    while (i--) {
        if (arr[i] === obj) {
            return true;
        }
    }
    return false;
}
function sleep(n) { //n表示的毫秒数
    var start = new Date().getTime();
    while (true) if (new Date().getTime() - start > n) break;
}
function move_down(id){
    if($("#"+id).next())
        $("#"+id).next().after($("#"+id));
}
function move_up(id){
    if($("#"+id).prev())
        $("#"+id).prev().before($("#"+id));
}
function copy_change(id){
    $.ajax({
        type : 'POST',
        url: "/web/remote_control/query_copy",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": id
        },
        success : function(result){
            if(result.success){
                parent.parent.printMsg(result.msg,'Success');
                $("#select_copy option[value='"+result.data.id+"']").attr("selected","");
                $('#select_copy').trigger("chosen:updated");
                $('#remote_control_copy_desc').val(result.data.desc);
                // $('#remote_control_copy_dest').val(result.data.dest);
                if(result.data.src_url!=''){
                    $('#remote_control_copy_source').val(result.data.src_url);
                    use_upload_file(false);
                }
                if(result.data.src_username!=''){
                    $('#remote_control_copy_src_url_username').val(result.data.src_username);
                    $('#checkbox_copy_with_pass').iCheck('check');
                }
                if(result.data.src_password!=''){
                    $('#remote_control_copy_src_url_password').val(result.data.src_password);
                    $('#checkbox_copy_with_pass').iCheck('check');
                }
                // $("#select_copy_authority option[value='"+result.data.authority+"']").attr("selected","");
                // $('#select_copy_authority').trigger("chosen:updated");
                add_copy(true);
                $('#li-copy').children('a').trigger('click')
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
    });
}
// function do_script(script_id, script_args, agent_tag) {
//     var value = false;
//     if (script_id){
//         $.ajax({
//         type : 'POST',
//         url: "/web/remote_control/do_script",
//         async:false,
//         data: {
//             "script_id": script_id,
//             "script_args": script_args,
//             "agent_tag": agent_tag
//         },
//         success : function(result){
//             if(result.success){
//                 $('#pre_work_manage').append('<span class="red-content">root@'+result.data.agent+'#</span> '+ '脚本输出如下: '+ script_args + '\n');
//                 $('#pre_work_manage').append(result.data.data.msg.stdout + '\n');
//                 $('#pre_work_manage').css('display', 'block')
//                 //printMsg(result.msg,'Success');
//                 value=true;
//             }else{
//                 if(result.data){
//                     $('#pre_work_manage').append(result.data.data.msg.stderr + '\n');
//                     $('#pre_work_manage').css('display', 'block')
//                     //printMsg(result.msg,'error');
//                 }else{
//                     //printMsg(result.msg,'error');
//                 }
//             }
//         }
//         });
//
//     }else{
//         //printMsg('请选择要执行的命令','error');
//     }
//     return value;
// }
// function do_copy(copy_id, agent_tag) {
//     var value = 0;
//     if (copy_id){
//         $.ajax({
//         type : 'POST',
//         url: "/web/remote_control/do_copy",
//         async:false,
//         data: {
//             "copy_id": copy_id,
//             "agent_tag": agent_tag
//         },
//         success : function(result){
//             if(result.success){
//                 $('#pre_work_manage').append('<span class="red-content">root@'+result.data.agent+'#</span> '+ '复制文件到: '+ result.data.data.msg.dest + '\n');
//                 if(result.data.data.msg.changed){
//                     $('#pre_work_manage').append('<span class="yellow-content">文件已更新</span> ' + '\n');
//                     value=1;
//                 }else{
//                     $('#pre_work_manage').append('<span class="green-content">文件无变化</span> ' + '\n');
//                     value=2;
//                 }
//                 $('#pre_work_manage').css('display', 'block')
//                 //printMsg(result.msg,'Success');
//
//             }else{
//                 if(result.data){
//                     $('#pre_work_manage').append('<span class="red-content">文件复制失败</span> ' + '\n');
//                     $('#pre_work_manage').css('display', 'block')
//                     //printMsg(result.msg,'error');
//                 }else{
//                     //printMsg(result.msg,'error');
//                 }
//             }
//         }
//         });
//
//     }else{
//         //printMsg('请选择要执行的命令','error');
//     }
//     return value;
// }
// function do_command(command_id,agent_tag) {
//     var value = false;
//     if (command_id){
//         $.ajax({
//         type : 'POST',
//         url: "/web/remote_control/do_command",
//         async:false,
//         data: {
//             "command_id": command_id,
//             "agent_tag": agent_tag
//         },
//         success : function(result){
//             if(result.success){
//                 $('#pre_work_manage').append('<span class="red-content">root@'+result.data.agent+'#</span> '+ result.data.data.msg.cmd+ '\n');
//                 $('#pre_work_manage').append(result.data.data.msg.stdout + '\n');
//                 $('#pre_work_manage').css('display', 'block')
//                 $("#pre_work_manage").trigger("change");
//                 //printMsg(result.msg,'Success');
//                 value=true;
//             }else{
//                 if(result.data){
//                     $('#pre_work_manage').append(result.data.data.msg.stderr + '\n');
//                     $('#pre_work_manage').css('display', 'block')
//                     $("#pre_work_manage").trigger("change");
//                     //printMsg(result.msg,'error');
//                 }else{
//                     //printMsg(result.msg,'error');
//                 }
//             }
//         }
//         });
//     }else{
//         //printMsg('请选择要执行的命令','error');
//     }
//     return value;
// }
// function work_do_test(data) {
//     for(var job_index in data['jobs']){
//         if(data['jobs'][job_index]['type']=='command'){
//             if(do_command(data['jobs'][job_index]['id'],data['test_tag'])==false&&data['jobs'][job_index]['ignore_error']==false){
//                 return false;
//             }
//         }else if(data['jobs'][job_index]['type']=='script'){
//             if(do_script(data['jobs'][job_index]['id'],data['jobs'][job_index]['args'],data['test_tag'])==false&&data['jobs'][job_index]['ignore_error']==false){
//                 return false;
//             }
//         }else if(data['jobs'][job_index]['type']=='copy'){
//             var tag = do_copy(data['jobs'][job_index]['id'],data['test_tag']);
//             if(tag==0&&data['jobs'][job_index]['ignore_error']==false){
//                 return false;
//             }
//             if(tag==2&&data['jobs'][job_index]['check_change']==true){
//                 return false;
//             }
//         }
//     }
//     return true;
// }
//
// function work_do_test_and_save() {
//     var work_name_cn = $('#name_cn').val();
//     var work_name_en = $('#name_en').val();
//     // var work_env = $('#env').val();
//     var work_timeout = $('#timeout').val();
//     var work_sync = $('#sync').is(':checked');
//     var work_desc = $('#desc').summernote('code');
//     var work_jobs = [];
//     $('#add_action_content').children('li').each(function () {
//         var action_type = $(this).attr('action_type');
//         var action_id = $(this).attr('action_id');
//         var ignore_error = $($(this).find('.ignore_error')[0]).is(':checked');
//         if (action_type=='script'){
//             var script_args = $("#script_args_disabled").val();
//             var action = {
//                 "type": action_type,
//                 "id": action_id,
//                 "args": script_args,
//                 "ignore_error": ignore_error
//             };
//         }else if (action_type=='copy'){
//             var check_change = $($(this).find('.check_change')[0]).is(':checked');
//             var action = {
//                 "type": action_type,
//                 "id": action_id,
//                 "ignore_error": ignore_error,
//                 "check_change": check_change
//             };
//         }else{
//             var action = {
//                 "type": action_type,
//                 "id": action_id,
//                 "ignore_error": ignore_error
//             };
//         }
//         if(contains(work_jobs,action) == false){
//             work_jobs.push(action);
//         }
//     });
//     var work_tags = [];
//     var work_test_tag = '';
//     $('#add_env_content').children('li').each(function () {
//         var env_type = $(this).attr('env_type');
//         var tag_id = $(this).attr('tag_id');
//         if(env_type=='test'){
//             work_test_tag = tag_id;
//         }else{
//             work_tags.push(tag_id);
//         }
//     });
//     var data = {
//         "name_cn": work_name_cn,
//         "name_en": work_name_en,
//         // "env": work_env,
//         "timeout": work_timeout,
//         "sync": work_sync,
//         "desc": work_desc,
//         "jobs": work_jobs,
//         "test_tag": work_test_tag,
//         "tags": work_tags,
//     };
//     // console.log(data);
//     var yes_or_not = work_do_test(data);
// }
function work_do_test(id) {
    $.ajax({
        type : 'POST',
        url: "/web/configure_manage/work/test",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": id
        },
        success : function(result){
            if(result.success){
                parent.parent.printMsg(result.msg,'Success');
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
    });
}
function work_do_save() {
    var work_name_cn = $('#name_cn').val();
    var work_name_en = $('#name_en').val();
    // var work_env = $('#env').val();
    var work_timeout = $('#timeout').val();
    var work_sync = $('#sync').is(':checked');
    var work_desc = $('#desc').summernote('code');
    var work_jobs = [];
    $('#add_action_content').children('li').each(function () {
        var action_type = $(this).attr('action_type');
        var action_id = $(this).attr('action_id');
        var action_name = $(this).attr('action_name');
        var timestamp = $(this).attr('timestamp');
        var ignore_error = $($(this).find('.ignore_error')[0]).is(':checked');
        if (action_type=='script'){
            var script_args = $("#script_args_disabled"+timestamp).val();
            var action = {
                "type": action_type,
                "id": action_id,
                "name": action_name,
                "args": script_args,
                "ignore_error": ignore_error
            };
        }else if (action_type=='copy'){
            var check_change = $($(this).find('.check_change')[0]).is(':checked');
            var copy_dest = $("#copy_dest_disabled"+timestamp).val();
            var copy_authority = $("#select_copy_authority_disabled"+timestamp+' option:selected').val();
            var action = {
                "type": action_type,
                "id": action_id,
                "name": action_name,
                "dest": copy_dest,
                "authority": copy_authority,
                "ignore_error": ignore_error,
                "check_change": check_change
            };
        }else{
            var action = {
                "type": action_type,
                "id": action_id,
                "name": action_name,
                "ignore_error": ignore_error
            };
        }
        work_jobs.push(action);
    });
    var work_tags = [];
    var work_test_tag = '';
    $('#add_env_content').children('li').each(function () {
        var env_type = $(this).attr('env_type');
        var tag_id = $(this).attr('tag_id');
        if(env_type=='test'){
            work_test_tag = tag_id;
        }else{
            if(contains(work_tags,tag_id) == false){
                work_tags.push(tag_id);
            }
        }
    });
    var data = {
        "name_cn": work_name_cn,
        "name_en": work_name_en,
        // "env": work_env,
        "timeout": work_timeout,
        "sync": work_sync,
        "desc": work_desc,
        "jobs": JSON.stringify(work_jobs),
        "test_tag": work_test_tag,
        "tags": JSON.stringify(work_tags),
    };
    console.log(data);
    $.ajax({
        type : 'POST',
        url: "/web/configure_manage/work/save",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: data,
        success : function(result){
            if(result.success){
                parent.parent.printMsg(result.msg,'Success');
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
    });
}
function add_env_test(tag_id, tag_name) {
    var timestamp=new Date().getTime();
    if(!tag_name){
        tag_name = $('#select_env_test option:selected').text();
    }
    if(!tag_id){
        tag_id = $('#select_env_test option:selected').val();
    }
    if(tag_id!=""){
        var html='<li env_type="test" class="success-element" id="raw-parameter-' + timestamp + '" tag_id="' + tag_id +'">'+
           '<div class="col-lg-4 col-md-4 col-sm-4 pull-left">'+
           '   <label class="pull-right padding-top-7" >'+
           '       <span class="red-content padding-5">测试环境</span>'+
           '   </label>'+
           ' </div>'+
           ' <div class="col-lg-8 col-md-8 col-sm-8 pull-left">'+
           ' <div class="col-lg-5 col-md-5 col-sm-5 padding-5"><a class="btn btn-primary">'+ tag_name +'</a></div>'+
           ' <div class="col-lg-4 col-md-4 col-sm-4 padding-5"><span class="padding-5" style="color:gray">系统将从测试环境中随机选取一台资产测试</span></div>'+
           ' <div class="col-lg-3 col-md-3 col-sm-3 padding-5">'+
           '<a class="btn btn-danger close-btn-env" option="raw-parameter-'+ timestamp +'" id="close-btn-work"><i class="fa fa-times"></i></a>'+
	    '</div></div></li>';
        $("#add_env_content").append(html);
        $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
        });
        $(".close-btn-env").click(function(){
        var name = $(this).attr("option");
            $("#"+name).remove();
        });
    }
}
function add_env_online(tag_id, tag_name) {
    var timestamp=new Date().getTime();
    if(!tag_name){
        tag_name = $('#select_env_online option:selected').text();
    }
    if(!tag_id){
        tag_id = $('#select_env_online option:selected').val();
    }
    if(tag_id!=""){
        var html='<li env_type="online" class="success-element" id="raw-parameter-' + timestamp + '" tag_id="' + tag_id +'">'+
           '<div class="col-lg-4 col-md-4 col-sm-4 pull-left">'+
           '   <label class="pull-right padding-top-7" >'+
           '       <span class="red-content padding-5">正式环境</span>'+
           '   </label>'+
           ' </div>'+
           ' <div class="col-lg-8 col-md-8 col-sm-8 pull-left">'+
           ' <div class="col-lg-5 col-md-5 col-sm-5 padding-5"><a class="btn btn-primary">'+ tag_name +'</a></div>'+
           ' <div class="col-lg-4 col-md-4 col-sm-4 padding-5"><span class="padding-5" style="color:gray">多个正式环境按照添加顺序串行升级</span></div>'+
           ' <div class="col-lg-3 col-md-3 col-sm-3 padding-5">'+
	       '<a class="btn btn-danger close-btn-env" option="raw-parameter-'+ timestamp +'" id="close-btn-work"><i class="fa fa-times"></i></a>'+
	    '</div></div></li>';
        $("#add_env_content").append(html);
        $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
        });
        $(".close-btn-env").click(function(){
        var name = $(this).attr("option");
            $("#"+name).remove();
        });
    }
}

function add_action_command(action_id, action_name, ignore_error) {
    var timestamp=new Date().getTime();
    if(ignore_error){
        var tab_ignore_error = 'checked'
    }else{
        var tab_ignore_error = ''
    }
    if(!action_name){
        action_name = $('#select_command option:selected').text();
    }
    if(!action_id){
        action_id = $('#select_command option:selected').val();
    }
    if(action_id!=""){
        var html='<li action_type="command" class="success-element" id="raw-parameter-' + timestamp + '" action_id="' + action_id +'"'+ '" action_name="' + action_name +'">'+
           '<div class="col-lg-4 col-md-4 col-sm-4 pull-left">'+
           '   <label class="pull-right padding-top-7" >'+
           '       <span class="red-content padding-5">远程命令</span><label><input type="checkbox" class="i-checks ignore_error" '+tab_ignore_error+'>  忽略报错</label>'+
           '   </label>'+
           ' </div>'+
           ' <div class="col-lg-8 col-md-8 col-sm-8 pull-left">'+
           ' <div class="col-lg-5 col-md-5 col-sm-5 padding-5"><a class="btn btn-primary" data-toggle="tooltip" title="点击编辑">'+ action_name +'</a></div>'+
           ' <div class="col-lg-4 col-md-4 col-sm-4 padding-5"></div>'+
           ' <div class="col-lg-3 col-md-3 col-sm-3 padding-5">'+
           '<a class="btn btn-primary" onclick="move_down(\'raw-parameter-'+ timestamp +'\')" ><i class="fa fa-arrow-down"></i></a>'+
           '<a class="btn btn-warning" onclick="move_up(\'raw-parameter-'+ timestamp +'\')" ><i class="fa fa-arrow-up"></i></a>'+
	       '<a class="btn btn-danger close-btn-action" option="raw-parameter-'+ timestamp +'" id="close-btn-work"><i class="fa fa-times"></i></a>'+
	    '</div></div></li>';

        $("#add_action_content").append(html);
        $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
        });
        $(".close-btn-action").click(function(){
        var name = $(this).attr("option");
        $("#"+name).remove();
        });
    }
}
function add_action_script(action_id, action_name, script_args, ignore_error) {
    var timestamp=new Date().getTime();
    if(ignore_error){
        var tab_ignore_error = 'checked'
    }else{
        var tab_ignore_error = ''
    }
    if(!action_name){
        action_name = $('#select_script option:selected').text();
    }
    if(!action_id){
        action_id = $('#select_script option:selected').val();
    }
    if(!script_args){
        script_args =  $('#remote_control_script_args').val();
    }
    if(action_id!=""){
        var html='<li action_type="script" class="success-element" id="raw-parameter-' + timestamp + '" action_id="' + action_id +'"'+ '" action_name="' + action_name +'" timestamp="' + timestamp +'">'+
           '<div class="col-lg-4 col-md-4 col-sm-4 pull-left">'+
           '   <label class="pull-right padding-top-7" >'+
           '       <span class="red-content padding-5">远程脚本</span><label><input type="checkbox" class="i-checks ignore_error" '+tab_ignore_error+'>  忽略报错</label>'+
           '   </label>'+
           ' </div>'+
           ' <div class="col-lg-8 col-md-8 col-sm-8 pull-left">'+
           ' <div class="col-lg-5 col-md-5 col-sm-5 padding-5"><a class="btn btn-primary" data-toggle="tooltip" title="点击编辑" >'+ action_name +'</a></div>'+
           ' <div class="col-lg-4 col-md-4 col-sm-4 padding-5"><input readonly ondblclick="this.readOnly=false" onchange="this.readOnly=true" id="script_args_disabled'+ timestamp +'" type="text" placeholder="脚本参数" class="form-control"></div>'+
           ' <div class="col-lg-3 col-md-3 col-sm-3 padding-5">'+
           '<a class="btn btn-primary" onclick="move_down(\'raw-parameter-'+ timestamp +'\')" ><i class="fa fa-arrow-down"></i></a>'+
           '<a class="btn btn-warning" onclick="move_up(\'raw-parameter-'+ timestamp +'\')" ><i class="fa fa-arrow-up"></i></a>'+
	       '<a class="btn btn-danger close-btn-action" option="raw-parameter-'+ timestamp +'" id="close-btn-work"><i class="fa fa-times"></i></a>'+
	    '</div></div></li>';

        $("#add_action_content").append(html);
        $("#script_args_disabled"+timestamp).val(script_args);
        $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
        });
        $(".close-btn-action").click(function(){
        var name = $(this).attr("option");
        $("#"+name).remove();
        });
    }
}
function add_action_copy(action_id, action_name, copy_dest, copy_authority, check_change, ignore_error) {
    var timestamp=new Date().getTime();
    if(check_change){
        var tab_check_change = 'checked'
    }else{
        var tab_check_change = ''
    }
    if(ignore_error){
        var tab_ignore_error = 'checked'
    }else{
        var tab_ignore_error = ''
    }
    if(!action_name){
        action_name = $('#select_copy option:selected').text();
    }
    if(!action_id){
        action_id = $('#select_copy option:selected').val();
    }
    if(!copy_dest){
        copy_dest = $('#remote_control_copy_dest').val();
    }
    if(!copy_authority){
        copy_authority = $('#select_copy_authority option:selected').val();
    }
    if(action_id!=""){
        var html='<li action_type="copy" class="success-element" id="raw-parameter-' + timestamp + '" action_id="' + action_id +'"'+ '" action_name="' + action_name+'" timestamp="' + timestamp +'">'+
           '<div class="col-lg-4 col-md-4 col-sm-4 pull-left">'+
           '   <label class="pull-right padding-top-7" >'+
           '       <span class="red-content padding-5">远程copy</span><label><input type="checkbox" class="i-checks ignore_error" '+tab_ignore_error+'>  忽略报错</label>'+
           '   </label>'+
           ' </div>'+
           ' <div class="col-lg-8 col-md-8 col-sm-8 pull-left">'+
           ' <div class="col-lg-5 col-md-5 col-sm-5 padding-5"><a class="btn btn-primary" data-toggle="tooltip" title="点击编辑" onclick="copy_change('+ action_id +')">'+ action_name +'</a>'+
            '<input readonly ondblclick="this.readOnly=false" onchange="this.readOnly=true" id="copy_dest_disabled'+ timestamp +'" type="text" placeholder="目标路径" class="form-control">'+
            '<select readonly ondblclick="this.readOnly=false" onchange="this.readOnly=true" class="chosen-select-inner" tabindex="2" id="select_copy_authority_disabled'+ timestamp +'">' +
            '                                                          <option value=""> 请选择权限</option>' +
            '                                                          <option value="755"> 读写执行</option>' +
            '                                                          <option value="644"> 读写</option>' +
            '                                                          <option value="444"> 只读</option>' +
            '                                                      </select>'+
            '</div>'+
           ' <div class="col-lg-4 col-md-4 col-sm-4 padding-5">'+
            '<input type="checkbox" class="i-checks check_change" '+tab_check_change+'>  确认变更'+
            '</div>'+
           ' <div class="col-lg-3 col-md-3 col-sm-3 padding-5">'+
           '<a class="btn btn-primary" onclick="move_down(\'raw-parameter-'+ timestamp +'\')" ><i class="fa fa-arrow-down"></i></a>'+
           '<a class="btn btn-warning" onclick="move_up(\'raw-parameter-'+ timestamp +'\')" ><i class="fa fa-arrow-up"></i></a>'+
	       '<a class="btn btn-danger close-btn-action" option="raw-parameter-'+ timestamp +'" id="close-btn-work"><i class="fa fa-times"></i></a>'+
	    '</div></div></li>';

        $("#add_action_content").append(html);
        $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
        });
        $(".close-btn-action").click(function(){
        var name = $(this).attr("option");
        $("#"+name).remove();
        });
        $('#checkbox_copy_with_pass').on( 'ifUnchecked', function () {
            $('#div_copy_url_with_pass').css('display', 'none');
        });
        $('#checkbox_copy_with_pass').on( 'ifChecked', function () {
            $('#div_copy_url_with_pass').css('display', '');
        });
        var config = {
            '.chosen-select-inner': {
                search_contains: true,
                width: "100%"
            }
        }
        for (var selector in config) {
            $(selector).chosen(config[selector]);
        }
        $("#copy_dest_disabled"+timestamp).val(copy_dest);
        $('#select_copy_authority_disabled'+timestamp+ " option[value='"+copy_authority+"']").attr("selected","");
        $('#select_copy_authority_disabled'+timestamp).trigger("chosen:updated");
    }
}
function add_command(tag) {
    if (tag == true){
        $('#div_add_command').css('display', 'block');
        $('#btn_add_command').text('关闭');
        $('#btn_add_command').attr('onclick', 'add_command(false)')
    }else{
        $('#div_add_command').css('display', 'none');
        $('#btn_add_command').text('添加');
        $('#btn_add_command').attr('onclick', 'add_command(true)')
    }
}
function add_script(tag) {
    if (tag == true){
        $('#div_add_script').css('display', 'block');
        $('#btn_add_script').text('关闭');
        $('#btn_add_script').attr('onclick', 'add_script(false)')
    }else{
        $('#div_add_script').css('display', 'none');
        $('#btn_add_script').text('添加');
        $('#btn_add_script').attr('onclick', 'add_script(true)')
    }
}
function add_copy(tag) {
    if (tag == true){
        $('#div_add_copy').css('display', 'block');
        $('#btn_add_copy').text('关闭');
        $('#btn_add_copy').attr('onclick', 'add_copy(false)')
    }else{
        $('#div_add_copy').css('display', 'none');
        $('#btn_add_copy').text('添加');
        $('#btn_add_copy').attr('onclick', 'add_copy(true)')
    }
}
function change_script(){
    var script_args =  $('#select_script option:selected').attr('args');
    if(script_args){
        $('#remote_control_script_args').css('display', 'block');
    }else{
        $('#remote_control_script_args').css('display', 'none');
    }
}
function save_command() {
    var desc = $('#remote_control_desc').val();
    var command = $('#remote_control_command').val();
    if (desc&&command){
        $.ajax({
        type : 'POST',
        url: "/web/remote_control/add_command",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "desc": desc,
            'command': command
        },
        success : function(result){
            if(result.success){
                $('#select_command').append("<option value='"+result.data.command_id+"'>"+result.data.desc+"</option>");
                $('#select_command').trigger("chosen:updated");
                parent.parent.printMsg(result.msg,'Success');
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
        });

    }else{
        parent.parent.printMsg('命令或者描述都不能为空！','error');
    }
}
function save_script() {
    $.ajaxFileUpload({
        url: '/web/remote_control/add_script',
        type: 'POST',
        dataType: 'json',
        fileElementId: 'remote_control_script',
        data: {
            "desc": $('#remote_control_script_desc').val(),
            "args": $('#remote_control_script_args').is(':checked')
        },
        success: function(result){
            if(result.success){
                $('#select_script').append("<option value='"+result.data.script_id+"' args='"+ result.data.script_args +"'>"+result.data.desc+"</option>");
                $('#select_script').trigger("chosen:updated");
                parent.parent.printMsg(result.msg,'Success');
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
    });
}
function save_copy() {
    var copy_type = $('#remote_control_copy_source').attr('type');
    if(copy_type=='file') {
        $.ajaxFileUpload({
            url: '/web/remote_control/add_copy',
            type: 'POST',
            dataType: 'json',
            fileElementId: 'remote_control_copy_source',
            data: {
                "desc": $('#remote_control_copy_desc').val(),
                "copy_dest": $('#remote_control_copy_dest').val(),
                "authority": $('#select_copy_authority option:selected').val()
            },
            success: function (result) {
                if (result.success) {
                    $('#select_copy').append("<option value='" + result.data.copy_id + "'>" + result.data.desc + "</option>");
                    $('#select_copy').trigger("chosen:updated");
                    parent.parent.printMsg(result.msg, 'Success');
                } else {
                    parent.parent.printMsg(result.msg, 'error');
                }
            }
        });
    }else{
        $.ajax({
            url: '/web/remote_control/add_copy',
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            type: 'POST',
            dataType: 'json',
            data: {
                "desc": $('#remote_control_copy_desc').val(),
                "copy_src": $('#remote_control_copy_source').val(),
                "with_pass": $('#checkbox_copy_with_pass').is(':checked'),
                "username": $('#remote_control_copy_src_url_username').val(),
                "password": $('#remote_control_copy_src_url_password').val(),
            },
            success: function (result) {
                if (result.success) {
                    $('#select_copy').append("<option value='" + result.data.copy_id + "'>" + result.data.desc + "</option>");
                    $('#select_copy').trigger("chosen:updated");
                    parent.parent.printMsg(result.msg, 'Success');
                } else {
                    parent.parent.printMsg(result.msg, 'error');
                }
            }
        });
    }
}
function del_command() {
    var command_id =  $('#select_command option:selected').val();
    if (command_id){
        $.ajax({
        type : 'POST',
        url: "/web/remote_control/del_command",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "command_id": command_id
        },
        success : function(result){
            if(result.success){
                $("#select_command option[value='"+''+"']").attr("selected","");
                $("#select_command option[value='"+command_id+"']").remove();
                $('#select_command').trigger("chosen:updated");
                parent.parent.printMsg(result.msg,'Success');
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
        });

    }else{
        parent.parent.printMsg('请选择要删除的命令','error');
    }
}
function del_script() {
    var script_id =  $('#select_script option:selected').val();
    if (script_id){
        $.ajax({
        type : 'POST',
        url: "/web/remote_control/del_script",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "script_id": script_id
        },
        success : function(result){
            if(result.success){
                $("#select_script option[value='"+''+"']").attr("selected","");
                $("#select_script option[value='"+script_id+"']").remove();
                $('#select_script').trigger("chosen:updated");
                $('#remote_control_script_args').css('display', 'none');
                parent.parent.printMsg(result.msg,'Success');
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
        });

    }else{
        parent.parent.printMsg('请选择要删除的脚本','error');
    }
}
function del_copy() {
    var copy_id =  $('#select_copy option:selected').val();
    if (copy_id){
        $.ajax({
        type : 'POST',
        url: "/web/remote_control/del_copy",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "copy_id": copy_id
        },
        success : function(result){
            if(result.success){
                $("#select_copy option[value='"+''+"']").attr("selected","");
                $("#select_copy option[value='"+copy_id+"']").remove();
                $('#select_copy').trigger("chosen:updated");
                parent.parent.printMsg(result.msg,'Success');
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
        });

    }else{
        parent.parent.printMsg('请选择要删除的脚本','error');
    }
}

function formToJson(form) {
    var result = {};
    var fieldArray = $('#' + form).serializeArray();
    for (var i = 0; i < fieldArray.length; i++) {
        var field = fieldArray[i];
        if (field.name in result) {
            result[field.name] += ',' + field.value;
        } else {
            result[field.name] = field.value;
        }
    }
    return result;
}
$(document).ready(function(){
    $('#desc').summernote({
        height: 230,
        maxHeight: 700
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
    var desc = '';
    $('#desc').summernote('reset');
    $('#desc').summernote('code', desc);

    $('#checkbox_test').on( 'ifUnchecked', function () {
        $('#div_test').css('display', 'none');
    });
    $('#checkbox_test').on( 'ifChecked', function () {
        $('#div_test').css('display', '');
    });
    $('#btn_work_do_save').click(function () {
        work_do_save();
    });
    $('#checkbox_copy_with_pass').on( 'ifUnchecked', function () {
        $('#div_copy_url_with_pass').css('display', 'none');
    });
    $('#checkbox_copy_with_pass').on( 'ifChecked', function () {
        $('#div_copy_url_with_pass').css('display', '');
    });
});

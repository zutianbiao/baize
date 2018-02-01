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
$('.collapse-link-inner').click(function () {
        var ibox = $(this).closest('div.ibox');
        var button = $(this).find('i');
        var content = ibox.find('div.ibox-content');
        content.slideToggle(200);
        button.toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
        ibox.toggleClass('').toggleClass('border-bottom');
        setTimeout(function () {
            ibox.resize();
            ibox.find('[id^=map-]').resize();
        }, 50);
    });
$('.i-checks-inner').iCheck({
    checkboxClass: 'icheckbox_square-green',
    radioClass: 'iradio_square-green'
});
var config = {
    '.chosen-select-inner': {
        search_contains: true,
        width: "100%"
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
function add_command(id,tag) {
    if (tag == true){
        $('#div_add_command'+id).css('display', 'block');
        $('#btn_add_command'+id).text('关闭');
        $('#btn_add_command'+id).attr('onclick', 'add_command('+id+',false)')
    }else{
        $('#div_add_command'+id).css('display', 'none');
        $('#btn_add_command'+id).text('添加');
        $('#btn_add_command'+id).attr('onclick', 'add_command('+id+',true)')
    }
}
function add_script(id,tag) {
    if (tag == true){
        $('#div_add_script'+id).css('display', 'block');
        $('#btn_add_script'+id).text('关闭');
        $('#btn_add_script'+id).attr('onclick', 'add_script('+id+',false)')
    }else{
        $('#div_add_script'+id).css('display', 'none');
        $('#btn_add_script'+id).text('添加');
        $('#btn_add_script'+id).attr('onclick', 'add_script('+id+',true)')
    }
}
function add_copy(id,tag) {
    if (tag == true){
        $('#div_add_copy'+id).css('display', 'block');
        $('#btn_add_copy'+id).text('关闭');
        $('#btn_add_copy'+id).attr('onclick', 'add_copy('+id+',false)')
    }else{
        $('#div_add_copy'+id).css('display', 'none');
        $('#btn_add_copy'+id).text('添加');
        $('#btn_add_copy'+id).attr('onclick', 'add_copy('+id+',true)')
    }
}
function change_script(id){
    var script_args =  $('#select_script'+id + ' option:selected').attr('args');
    if(script_args){
        $('#remote_control_script_args'+id).css('display', 'block');
    }else{
        $('#remote_control_script_args'+id).css('display', 'none');
    }
}
function save_command(id) {
    var desc = $('#remote_control_desc'+id).val();
    var command = $('#remote_control_command'+id).val();
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
                $('#select_command'+id).append("<option value='"+result.data.command_id+"'>"+result.data.desc+"</option>");
                $('#select_command'+id).trigger("chosen:updated");
                printMsg(result.msg,'Success');
            }else{
                printMsg(result.msg,'error');
            }
        }
        });

    }else{
        printMsg('命令或者描述都不能为空！','error');
    }
}
function save_script(id) {
    $.ajaxFileUpload({
        url: '/web/remote_control/add_script',
        type: 'POST',
        dataType: 'json',
        fileElementId: 'remote_control_script'+id,
        data: {
            "desc": $('#remote_control_script_desc'+id).val(),
            "args": $('#remote_control_script_args'+id).is(':checked')
        },
        success: function(result){
            if(result.success){
                $('#select_script'+id).append("<option value='"+result.data.script_id+"' args='"+ result.data.script_args +"'>"+result.data.desc+"</option>");
                $('#select_script'+id).trigger("chosen:updated");
                printMsg(result.msg,'Success');
            }else{
                printMsg(result.msg,'error');
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
                    parent.printMsg(result.msg, 'Success');
                } else {
                    parent.printMsg(result.msg, 'error');
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
                "copy_dest": $('#remote_control_copy_dest').val(),
                "authority": $('#select_copy_authority option:selected').val(),
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
function del_command(id) {
    var command_id =  $('#select_command'+id + ' option:selected').val();
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
                $('#select_command'+id + " option[value='"+''+"']").attr("selected","");
                $('#select_command'+id + " option[value='"+command_id+"']").remove();
                $('#select_command'+id).trigger("chosen:updated");
                printMsg(result.msg,'Success');
            }else{
                printMsg(result.msg,'error');
            }
        }
        });

    }else{
        printMsg('请选择要删除的命令','error');
    }
}
function del_script(id) {
    var script_id =  $('#select_script'+id + ' option:selected').val();
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
                $('#select_script'+id + " option[value='"+''+"']").attr("selected","");
                $('#select_script'+id + " option[value='"+script_id+"']").remove();
                $('#select_script'+id).trigger("chosen:updated");
                $('#remote_control_script_args'+id).css('display', 'none');
                printMsg(result.msg,'Success');
            }else{
                printMsg(result.msg,'error');
            }
        }
        });

    }else{
        printMsg('请选择要删除的脚本','error');
    }
}
function del_copy(id) {
    var copy_id =  $('#select_copy'+id + ' option:selected').val();
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
                $('#select_copy'+id + " option[value='"+''+"']").attr("selected","");
                $('#select_copy'+id + " option[value='"+copy_id+"']").remove();
                $('#select_copy'+id).trigger("chosen:updated");
                printMsg(result.msg,'Success');
            }else{
                printMsg(result.msg,'error');
            }
        }
        });

    }else{
        printMsg('请选择要删除的脚本','error');
    }
}
function do_command(id) {
    var command_id =  $('#select_command'+id + ' option:selected').val();
    if (command_id){
        $.ajax({
        type : 'POST',
        url: "/web/remote_control/do_command",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "command_id": command_id,
            "agent_id": id
        },
        success : function(result){
            if(result.success){
                $('#pre_command'+id).append('<span class="red-content">root@'+result.data.agent+'#</span> '+ result.data.data.msg.cmd+ '\n');
                $('#pre_command'+id).append(result.data.data.msg.stdout + '\n');
                $('#pre_command'+id).css('display', 'block')
                printMsg(result.msg,'Success');
            }else{
                if(result.data){
                    $('#pre_command'+id).append(result.data.data.msg.stderr + '\n');
                    $('#pre_command'+id).css('display', 'block')
                    printMsg(result.msg,'error');
                }else{
                    printMsg(result.msg,'error');
                }
            }
        }
        });

    }else{
        printMsg('请选择要执行的命令','error');
    }
}
function do_script(id) {
    var script_id =  $('#select_script'+id + ' option:selected').val();
    var script_args =  $('#remote_control_script_args'+id).val();
    if (script_id){
        $.ajax({
        type : 'POST',
        url: "/web/remote_control/do_script",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "script_id": script_id,
            "script_args": script_args,
            "agent_id": id
        },
        success : function(result){
            if(result.success){
                $('#pre_script'+id).append('<span class="red-content">root@'+result.data.agent+'#</span> '+ '脚本输出如下: '+ script_args + '\n');
                $('#pre_script'+id).append(result.data.data.msg.stdout + '\n');
                $('#pre_script'+id).css('display', 'block')
                printMsg(result.msg,'Success');
            }else{
                if(result.data){
                    $('#pre_script'+id).append(result.data.data.msg.stderr + '\n');
                    $('#pre_script'+id).css('display', 'block')
                    printMsg(result.msg,'error');
                }else{
                    printMsg(result.msg,'error');
                }
            }
        }
        });

    }else{
        printMsg('请选择要执行的命令','error');
    }
}
function do_copy(id) {
    var copy_id =  $('#select_copy'+id + ' option:selected').val();
    if (copy_id){
        $.ajax({
        type : 'POST',
        url: "/web/remote_control/do_copy",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "copy_id": copy_id,
            "agent_id": id
        },
        success : function(result){
            if(result.success){
                $('#pre_copy'+id).append('<span class="red-content">root@'+result.data.agent+'#</span> '+ '复制文件到: '+ result.data.data.msg.dest + '\n');
                if(result.data.data.msg.changed){
                    $('#pre_copy'+id).append('<span class="yellow-content">文件已更新</span> ' + '\n');
                }else{
                    $('#pre_copy'+id).append('<span class="green-content">文件无变化</span> ' + '\n');
                }

                $('#pre_copy'+id).css('display', 'block')
                printMsg(result.msg,'Success');
            }else{
                if(result.data){
                    $('#pre_copy'+id).append('<span class="red-content">文件复制失败</span> ' + '\n');
                    $('#pre_copy'+id).css('display', 'block')
                    printMsg(result.msg,'error');
                }else{
                    printMsg(result.msg,'error');
                }
            }
        }
        });

    }else{
        printMsg('请选择要执行的命令','error');
    }
}


$(document).ready(function() {
    var table_test = $('#editable_result_test').DataTable({
        dom: '<"html5buttons"B>lTfgitp',
        buttons: [{
            extend: 'copy'
        },
        {
            extend: 'csv'
        },
        {
            extend: 'excel',
            title: 'ExampleFile'
        },
        {
            extend: 'pdf',
            title: 'ExampleFile'
        }],
        "language": {
            "lengthMenu": '<div class="dataTables_length" id="editable_length"><label>每页显示 </label><select name="editable_length" aria-controls="editable" class="form-control input-sm"><option value="10">10</option><option value="25">25</option><option value="50">50</option><option value="100">100</option><option value="-1">All</option></select><label> 条记录</label></div>',
            "info": "从 _START_ 到 _END_ /共 _TOTAL_ 条数据",
            "paginate": {
                "first": "首页",
                "last": "尾页",
                "next": "后一页",
                "previous": "前一页"
            }
        },
        "searching": true
    });
    var table_online = $('#editable_result_online').DataTable({
        dom: '<"html5buttons"B>lTfgitp',
        buttons: [{
            extend: 'copy'
        },
        {
            extend: 'csv'
        },
        {
            extend: 'excel',
            title: 'ExampleFile'
        },
        {
            extend: 'pdf',
            title: 'ExampleFile'
        }],
        "language": {
            "lengthMenu": '<div class="dataTables_length" id="editable_length"><label>每页显示 </label><select name="editable_length" aria-controls="editable" class="form-control input-sm"><option value="10">10</option><option value="25">25</option><option value="50">50</option><option value="100">100</option><option value="-1">All</option></select><label> 条记录</label></div>',
            "info": "从 _START_ 到 _END_ /共 _TOTAL_ 条数据",
            "paginate": {
                "first": "首页",
                "last": "尾页",
                "next": "后一页",
                "previous": "前一页"
            }
        },
        "searching": true
    });
    $('#editable_result_test tbody').on('click', 'tr', function () {
        var type = $(this).attr('r_type');
        var success = $(this).attr('r_success');
        var id = $(this).attr('r_id');
        var result = JSON.parse(result_detail.data.result_summary[type][success][id]['result']);
        var hostname = result_detail.data.result_summary[type][success][id]['hostname'];
        var header = '<span class="red-content">root@'+hostname+'#</span> ';
        $('#pre_result_test').empty();
        for(var i in result){
            console.log(result[i].msg);
            if(result[i].msg.invocation.module_name=='shell'){
                $('#pre_result_test').append(header+result[i].msg.cmd+'\n');
                if(result[i].success){
                    if(result[i].msg.stderr!=''){
                        $('#pre_result_test').append('<span class="yellow-content">'+result[i].msg.stderr+'</span>'+'\n');
                    }
                    if(result[i].msg.stdout!=''){
                        $('#pre_result_test').append(result[i].msg.stdout+'\n');
                    }
                }else{
                    $('#pre_result_test').append('<span class="red-content">执行失败</span> ' +'\n');
                    if(result[i].msg.stderr!=''){
                        $('#pre_result_test').append('<span class="yellow-content">'+result[i].msg.stderr+'</span>'+'\n');
                    }
                    if(result[i].msg.stdout!=''){
                        $('#pre_result_test').append(result[i].msg.stdout+'\n');
                    }
                }
            }else if(result[i].msg.invocation.module_name=='copy'){
                if(result[i].success){
                    $('#pre_result_test').append(header + '复制文件到: ' + result[i].msg.dest + '\n');
                    if(result[i].msg.changed) {
                        $('#pre_result_test').append('<span class="yellow-content">文件已更新</span> ' + '\n');
                    }else{
                        $('#pre_result_test').append('<span class="green-content">文件无变化</span> ' + '\n');
                    }
                }else{
                    $('#pre_result_test').append('<span class="red-content">文件复制失败</span> ' + '\n');
                }
            }
        }
        $('#div_result_test').css('display', 'block');
    });
    $('#editable_result_online tbody').on('click', 'tr', function () {
        var type = $(this).attr('r_type');
        var success = $(this).attr('r_success');
        var id = $(this).attr('r_id');
        var result = JSON.parse(result_detail.data.result_summary[type][success][id]['result']);
        var hostname = result_detail.data.result_summary[type][success][id]['hostname'];
        var header = '<span class="red-content">root@'+hostname+'#</span> ';
        $('#pre_result_online').empty();
        for(var i in result){
            console.log(result[i].msg);
            if(result[i].msg.invocation.module_name=='shell'){
                $('#pre_result_online').append(header+result[i].msg.cmd+'\n');
                if(result[i].success){
                    if(result[i].msg.stderr!=''){
                        $('#pre_result_online').append('<span class="yellow-content">'+result[i].msg.stderr+'</span>'+'\n');
                    }
                    if(result[i].msg.stdout!=''){
                        $('#pre_result_online').append(result[i].msg.stdout+'\n');
                    }
                }else{
                    $('#pre_result_online').append('<span class="red-content">执行失败</span> ' +'\n');
                    if(result[i].msg.stderr!=''){
                        $('#pre_result_online').append('<span class="yellow-content">'+result[i].msg.stderr+'</span>'+'\n');
                    }
                    if(result[i].msg.stdout!=''){
                        $('#pre_result_online').append(result[i].msg.stdout+'\n');
                    }
                }
            }else if(result[i].msg.invocation.module_name=='copy'){
                if(result[i].success){
                    $('#pre_result_online').append(header + '复制文件到: ' + result[i].msg.dest + '\n');
                    if(result[i].msg.changed) {
                        $('#pre_result_online').append('<span class="yellow-content">文件已更新</span> ' + '\n');
                    }else{
                        $('#pre_result_online').append('<span class="green-content">文件无变化</span> ' + '\n');
                    }
                }else{
                    $('#pre_result_online').append('<span class="red-content">文件复制失败</span> ' + '\n');
                }
            }
        }
        $('#div_result_online').css('display', 'block');
    });
    $('#i_shut_test').click(function () {
        $('#div_result_test').css('display', 'none');
    });
    $('#i_shut_online').click(function () {
        $('#div_result_online').css('display', 'none');
    });
});
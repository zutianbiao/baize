var wait=0;
function time(e, id, status) {
    $.ajax({
        type : 'POST',
        url: "/web/configure_manage/task/query_status",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": id
        },
        success : function(result){
            if(result.success){
                if(status==result.data.status){
                    var content = '<span class="yellow-content" status="'+result.data.status+'">'+result.data.msg+'('+wait+')'+'</span>\n' +
                        '<a class="btn btn-primary btn-xs" onclick="task_status_detail('+id+')">详情</a>';
                    $($(e).parent('td').prev()[0]).html(content);
                    wait++;
                    setTimeout(function() {
                        time(e, id, result.data.status)
                    }, 1000)
                }else{
                    var content = '<span class="yellow-content" status="'+result.data.status+'">'+result.data.msg+'</span>\n' +
                        '<a class="btn btn-primary btn-xs" onclick="task_status_detail('+id+')">详情</a>';
                    $($(e).parent('td').prev()[0]).html(content);
                    wait = 0;
                }
            }
        }
    });
}
function task_do_test(e, id) {
    $.ajax({
        type : 'POST',
        url: "/web/configure_manage/task/test",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": id
        },
        success : function(result){
            if(result.success){
                var content = '<span class="yellow-content" status="1">测试中</span>\n' +
                    '<a class="btn btn-primary btn-xs" onclick="task_status_detail('+id+')">详情</a>';
                $($(e).parent('td').prev()[0]).html(content);
                time(e, id, 1);
                printMsg(result.msg,'Success');
            }else{
                printMsg(result.msg,'error');
            }
        }
    });
}
function task_do_online(e, id) {
    $.ajax({
        type : 'POST',
        url: "/web/configure_manage/task/online",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": id
        },
        success : function(result){
            if(result.success){
                var content = '<span class="yellow-content" status="4">执行中</span>\n' +
                    '<a class="btn btn-primary btn-xs" onclick="task_status_detail('+id+')">详情</a>';
                $($(e).parent('td').prev()[0]).html(content);
                time(e, id, 4);
                printMsg(result.msg,'Success');
            }else{
                printMsg(result.msg,'error');
            }
        }
    });
}
function task_do_online_continue(e, id) {
    $.ajax({
        type : 'POST',
        url: "/web/configure_manage/task/continue",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": id
        },
        success : function(result){
            if(result.success){
                var content = '<span class="yellow-content" status="4">执行中</span>\n' +
                    '<a class="btn btn-primary btn-xs" onclick="task_status_detail('+id+')">详情</a>';
                $($(e).parent('td').prev()[0]).html(content);
                printMsg(result.msg,'Success');
            }else{
                printMsg(result.msg,'error');
            }
        }
    });
}
function task_do_test_continue(e, id) {
    $.ajax({
        type : 'POST',
        url: "/web/configure_manage/task/continue",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": id
        },
        success : function(result){
            if(result.success){
                var content = '<span class="yellow-content" status="1">测试中</span>\n' +
                    '<a class="btn btn-primary btn-xs" onclick="task_status_detail('+id+')">详情</a>';
                $($(e).parent('td').prev()[0]).html(content);
                printMsg(result.msg,'Success');
            }else{
                printMsg(result.msg,'error');
            }
        }
    });
}
function task_delete(e, id) {
    $.ajax({
        type : 'POST',
        url: "/web/configure_manage/task/delete",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": id
        },
        success : function(result){
            if(result.success){
                printMsg(result.msg,'Success');
                $(e).parents('tr').remove();
            }else{
                printMsg(result.msg,'error');
            }
        }
    });
}
function task_status_detail(id){
    var options={
        "tabMainName": "add_task_nav_tabs",
        "tabContentMainName": "add_task_tab_content",
        "tabName": "task_status_detail"+id,
        "tabTitle": "任务结果详情",
        "tabUrl": "/web/task_manage/status_detail?id="+id,
        "tabmainHeight": $(document.body).height()*2
    };
    addTab(options);
}
function task_modify(id) {
    var options={
        "tabMainName": "add_task_nav_tabs",
        "tabContentMainName": "add_task_tab_content",
        "tabName": "modify_task"+id,
        "tabTitle": "编辑任务",
        "tabUrl": "/web/task_manage/modify?id="+id,
        "tabmainHeight": $(document.body).height()*2
    };
    addTab(options);
}
$(document).ready(function() {
    printMsg('数据加载成功！','Success');
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
    var table = $('#editable').DataTable({
        dom: '<"html5buttons"B>lrtip',
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
        },
        {
            extend: 'print',
            customize: function(win) {
                $(win.document.body).addClass('white-bg');
                $(win.document.body).css('font-size', '10px');
                $(win.document.body).find('table').addClass('compact').css('font-size', 'inherit');
            }
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
    $('.checkall').on('ifChecked',
    function(event) {
        table.page.len( -1 ).draw();
        $('.checkchild').iCheck('check');
    });
    $('.checkall').on('ifUnchecked',
    function(event) {
        $('.checkchild').iCheck('uncheck');
        table.page.len( 10 ).draw();
    });
    $('.checkall').iCheck('uncheck');
    $('#add_task').click(function(){
        var options={
            "tabMainName": "add_task_nav_tabs",
            "tabContentMainName": "add_task_tab_content",
            "tabName": "tab_add_task",
            "tabTitle": "新增任务",
            "tabUrl": "/web/task_manage/add",
            "tabmainHeight": $(document.body).height()*2
        };
        addTab(options);
    });
    $("#btn_search_task").click(function() {
        var value = $("#input_search_task").val();
        table.search(value).draw();
    });
    $("#input_search_task").keydown(function(event) {
        if(event.keyCode == "13") {
            var value = $("#input_search_task").val();
            table.search(value).draw();
        }
    });
});
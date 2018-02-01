function work_status_detail(id){
    var options={
        "tabMainName": "add_task_nav_tabs",
        "tabContentMainName": "add_task_tab_content",
        "tabName": "task_status_detail"+id,
        "tabTitle": "作业结果详情",
        "tabUrl": "/web/work_manage/status_detail?id="+id,
        "tabmainHeight": $(document.body).height()*2
    };
    parent.addTab(options);
}
function work_status_refesh(e, id) {
    $.ajax({
        type : 'POST',
        url: "/web/configure_manage/work/status_refresh",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": id
        },
        success : function(result){
            if(result.success){
                $($(e).prev('span')[0]).attr('class', 'green-content');
                $($(e).prev('span')[0]).text(result.msg);
                parent.printMsg(result.msg,'Success');
            }else{
                $($(e).prev('span')[0]).attr('class', 'red-content');
                $($(e).prev('span')[0]).text(result.msg);
                parent.printMsg(result.msg,'error');
            }
        }
    });
}
$(document).ready(function() {
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
    $("#btn_search_work").click(function() {
        var value = $("#input_search_work").val();
        table.search(value).draw();
    });
    $("#input_search_work").keydown(function() {
        if(event.keyCode == "13") {
            var value = $("#input_search_work").val();
            table.search(value).draw();
        }
    });
});
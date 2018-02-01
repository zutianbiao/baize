$(document).ready(function() {
    printMsg('数据加载成功！','Success');
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
    });
    var config = {
        '.chosen-select': {
            search_contains: true,
            width: "80%"
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
    var role_checked = new Array();
    var table = $('#editable').DataTable({
        /* 1. `l` 代表 length，左上角的改变每页显示条数控件
           2. `f` 代表 filtering，右上角的过滤搜索框控件
           3. `t` 代表 table，表格本身
           4. `i` 代表 info，左下角的表格信息显示控件
           5. `p` 代表 pagination，右下角的分页控件
           6. `r` 代表 processing，表格中间的数据加载等待提示框控件
           7. `B` 代表 button，Datatables可以提供的按钮控件，默认显示在左上角
        */
        dom: '<"html5buttons"B>lrtip',
        "columnDefs":[
        {
            //设置第一列不参与搜索
            "targets":[0],
            "searchable":false
        }],
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
    $('.check-column').on( 'ifChecked', function () {
        var column = table.column( $(this).attr('data-column') );
        column.visible( true );
    });
    $('.check-column').on( 'ifUnchecked', function () {
        var column = table.column( $(this).attr('data-column') );
        column.visible( false );
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
    $("#table_search").click(function() {
        value = $("#table_search_input").val();
        table.search(value).draw();
    });
    $('.checkchild').on('ifUnchecked', function(event) {
        role_checked.pop($(this).val());
    });
    $('.checkchild').on('ifChecked', function(event) {
        role_checked.push($(this).val());
    });
    $("#table_search_input").keydown(function() {
        if(event.keyCode == "13") {
            var value = $("#table_search_input").val();
            table.search(value).draw();
        }
    });
    $('#role_handle').on('change', function(e, params) {
        console.log(role_checked);
        var value = $('#role_handle option:selected').val();
        if(value=='del'){
            $.ajax({
               type : 'POST',
               url: "/web/network_detect/role/delete_multiple/",
               headers: {
                   Accept: "application/json; charset=utf-8"
               },
               data: {
                   "role": JSON.stringify(role_checked),
               },
               success : function(result){
                   if(result.success){
                       console.log(result.data);
                       printMsg('5秒后页面将自动刷新...','Success');
                       printMsg(result.msg,'Success');
                       setTimeout(function() {
                           window.location.reload();
                       },5000);
                   }else{
                       printMsg(result.msg,'error');
                   }
               }
            });
        }
    });
    $('#editable').on('draw.dt',function() {
        $('.checkchild').on('ifUnchecked', function(event) {
            role_checked.pop($(this).val());
        });
        $('.checkchild').on('ifChecked', function(event) {
            role_checked.push($(this).val());
        });
    });

});
$(document).ready(function() {
//    printMsg('数据加载成功！','Success');
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
        "searching": false
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

    $('#file_proxy_hosts').change(function(){
        var file = $('#file_proxy_hosts').val();
        $('#file_proxy_hosts_name').text(file);
    });
    $('#import_proxy_hosts').click(function(){
        var file = $('#file_proxy_hosts').val();
        var list_file_split = file.split('.');
        var suffix_file = list_file_split[list_file_split.length-1];
        if (suffix_file!='xlsx'&&suffix_file!='xls'){
            $('#modal_alert_import_proxy_hosts').html('<div class="text-danger">文件类型不合法，请确保上传的文件类型是xls、xlsx</div>');
        }else{
            $('#form_proxy_hosts').ajaxSubmit({
                type: 'POST',
                url: "/web/master/import_proxy_hosts/",
                dataType : 'json',
                success: function(result){
                    if (result.success) {
                        printMsg(result.msg, 'success');
                    }else{
                        printMsg(result.msg, 'error');
                    }
                }
            });
        }
    });
});
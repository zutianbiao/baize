Array.prototype.remove = function(val){
    var index = this.indexOf(val);
    if (index > -1) {
        this.splice(index, 1);
    }
};
var table = window.table;
$(document).ready(function() {
    window.check_asset_id = new Array();
    $('.tag-list-option').click(function(){
        $('.tag-list >li>a.active').removeClass("active");
        $(this).attr("class","tag-list-option active");
    });
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
    });
    $('.check-column').on( 'ifChecked', function () {
        var column = table.column( $(this).attr('data-column') );
        column.visible( true );
    });
    $('.check-column').on( 'ifUnchecked', function () {
        var column = table.column( $(this).attr('data-column') );
        column.visible( false );
    });

    $('.checkall').on('ifChecked', function(event) {
        table.page.len( -1 ).draw();
        $('.checkchild').iCheck('check');
    });
    $('.checkchild').on('ifChecked', function(event) {
        check_asset_id.push($(this).attr('asset_id'));
    });
    $('.checkall').on('ifUnchecked', function(event) {
        $('.checkchild').iCheck('uncheck');
        table.page.len( 10 ).draw();
    });
    $('.checkchild').on('ifUnchecked', function(event) {
        check_asset_id.remove($(this).attr('asset_id'));
    });
    $('.checkall').iCheck('uncheck');

});
function show_detail(id) {
    $.ajax({
    type : 'POST',
    url: "/web/asset_manage/show_detail",
    headers: {
        Accept: "application/json; charset=utf-8"
    },
    data: {
        "asset_id": id,
    },
    success : function(data){
        if(data){
            $('#asset_detail').html(data);
            $('#myModal'+id).modal('show');
            printMsg('查询资产详情成功','Success');
        }else{
            printMsg('查询资产详情失败','error');
        }
    }
    });
}
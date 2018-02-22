Date.prototype.format = function(fmt)
{ //author: meizz
  var o = {
    "m+" : this.getMonth()+1,                 //月份
    "d+" : this.getDate(),                    //日
    "H+" : this.getHours(),                   //小时
    "M+" : this.getMinutes(),                 //分
    "S+" : this.getSeconds(),                 //秒
    "q+" : Math.floor((this.getMonth()+3)/3), //季度
    "s"  : this.getMilliseconds()             //毫秒
  };
  if(/(Y+)/.test(fmt))
    fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
  for(var k in o)
    if(new RegExp("("+ k +")").test(fmt))
  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
  return fmt;
};
function ignore_alarm_msg(id, tag){
    $.ajax({
        type : 'POST',
        url: "/web/alarm_manage/ignore_alarm_msg",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": id,
            "tag": tag
        },
        success : function(data){
            if(data.success){
                printMsg(data.msg,'Success');
            }else{
                printMsg(data.msg,'error');
            }
        }
    });
}
printMsg('视图加载中...','Success');
var list_status = ['未处理', '处理中', '发送成功', '发送失败', '重新发送中', '重新发送成功', '重新发送失败', '忽略报警', '合并发送成功', '合并发送失败', '合并发送进行中'];
function query_msg(min) {
    $.ajax({
        type : 'POST',
        url: "/web/alarm_manage/query_alarm_msg",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "min": min,
        },
        success : function(data){
            if(data.success){
                table.clear();
                var table_data = new Array();
                var table_row = new Array();
                for(var i in data['data']){
                    if(i!='remove'){
                        table_row[0] = data['data'][i]['alarm_name'];
                        table_row[1] = data['data'][i]['person'].join("<br>");
                        table_row[2] = new Date(data['data'][i]['time']*1000).format("YYYY-mm-dd HH:MM:SS");
                        if(data['data'][i]['status']!=7){
                            table_row[3] = list_status[data['data'][i]['status']]+'<a class="btn btn-xs btn-warning" type="button" onclick="ignore_alarm_msg('+data['data'][i]['id']+', true)">忽略同类报警</a>';
                        }else{
                            table_row[3] = list_status[data['data'][i]['status']]+'<a class="btn btn-xs btn-primary" type="button" onclick="ignore_alarm_msg('+data['data'][i]['id']+', false)">解除忽略</a>';
                        }
                        table_row[4] = data['data'][i]['msg'];
                        table_data.push(table_row);
                        table_row = new Array();
                    }
                }
                if(table_data.length != 0){
                    table.rows.add(table_data).draw();
                }
                printMsg(data.msg,'Success');
            }else{
                printMsg(data.msg,'error');
            }
        }
    });
}
function init_table(){
    window.table = $('#editable').DataTable({
        dom: '<"html5buttons"B>lrtip',
        buttons: [{
                text: '最近五分钟',
                action: function ( e, dt, node, config ) {
                    query_msg(5);
                }
            },{
                text: '最近十五分钟',
                action: function ( e, dt, node, config ) {
                    query_msg(15);
                }
            },{
                text: '最近半小时',
                action: function ( e, dt, node, config ) {
                    query_msg(30);
                }
            },
        ],
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
    $("#btn_msg_search").click(function() {
        table.page.len( -1 ).draw();
        var value = $("#input_msg_search").val();
        table.search(value).draw();
    });
    $("#input_msg_search").keydown(function() {
        if(event.keyCode == "13") {
            table.page.len( -1 ).draw();
            var value = $("#input_msg_search").val();
            table.search(value).draw();
        }
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
}
$(document).ready(function() {
    init_table();
    query_msg(5);
})
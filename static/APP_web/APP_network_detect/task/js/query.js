

var planePath = 'path://M1705.06,1318.313v-89.254l-319.9-221.799l0.073-208.063c0.521-84.662-26.629-121.796-63.961-121.491c-37.332-0.305-64.482,36.829-63.961,121.491l0.073,208.063l-319.9,221.799v89.254l330.343-157.288l12.238,241.308l-134.449,92.931l0.531,42.034l175.125-42.917l175.125,42.917l0.531-42.034l-134.449-92.931l12.238-241.308L1705.06,1318.313z';
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
}

function randomColor(color, str) {
    return color[Math.round(str.length%color.length)];
}
function randomData() {
    return Math.round(Math.random());
}
function query_detect_history() {
    var column_now_id = $('#history_type_item option:selected').val();
    detect_source = $('#detect_source').val();
    detect_target = $('#detect_target').val();
    if (column_now_id == 4){
        var db = 'network_detect_ping';
        var item = 'rtt';
    }else if (column_now_id == 5){
        var db = 'network_detect_ping';
        var item = 'lost_rate';
    }else if (column_now_id == 6){
        var db = 'network_detect_curl';
        var item = 'time_conn';
    }else if (column_now_id == 7){
        var db = 'network_detect_curl';
        var item = 'time_total';
    }else if (column_now_id == 8){
        var db = 'network_detect_curl';
        var item = 'speed';
    }else if (column_now_id == 9){
        var db = 'network_detect_curl';
        var item = 'file_size';
    }else{
        var db = '';
        var item = '';
    }
    if (db != ''){
        $.ajax({
            type : 'POST',
            url: "/web/network_detect/task/query/history",
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            data: {
                "db": db,
                'item': item,
                'source': detect_source,
                'target': detect_target,
                'period': $('#history_period option:selected').val()
            },
            success : function(result){
                if(result.success){
                    var resizeWorldMapContainer = function () {
                        document.getElementById('echarts_detect_history').style.width = window.innerWidth+'px';
                        document.getElementById('echarts_detect_history').style.height = window.innerHeight+'px';
                    };
                    resizeWorldMapContainer();
                    var series_data = [];
                    for (var i in result.data) {
                        series_data.push(result.data[i]);
                    }
                    var echarts_detect_history = echarts.init(document.getElementById('echarts_detect_history'));
                    option = {
                        title: {
                            text: '动态数据 + 时间坐标轴'
                        },
                        legend: {
                            show: false,
                            height: document.getElementById('echarts_detect_history').style.height,
                            width: document.getElementById('echarts_detect_history').style.width,
                        },
                        tooltip: {
                            trigger: 'axis',
                            formatter: function (params) {
                                params = params[0];
                                var date = new Date(params.value[0]);
                                return date.format("YYYY-mm-dd HH:MM:SS") + ' : ' + params.value[1];
                            },
                            axisPointer: {
                                animation: false
                            }
                        },
                        xAxis: {
                            type: 'time',
                            splitLine: {
                                show: false
                            }
                        },
                        yAxis: {
                            type: 'value',
                            boundaryGap: [0, '100%'],
                            splitLine: {
                                show: false
                            }
                        },
                        series: [{
                            name: '模拟数据',
                            type: 'line',
                            showSymbol: false,
                            hoverAnimation: false,
                            itemStyle: {
                                normal: {
                                    color: '#1ab394'
                                }
                            },
                            data: series_data
                        }]
                    };
                    echarts_detect_history.setOption(option);
                    $('#div_history').css({"display": "block"});
                    printMsg(result.msg,'Success');
                }else{
                    printMsg(result.msg,'error');
                }
            }
        });
    }
}
var convertData = function (data) {
    var res = [];
    var fromCoord = [data.source.longitude, data.source.latitude];
    var toCoord = [data.target.longitude, data.target.latitude];
    if (fromCoord && toCoord) {
        res.push({
            fromName: data.source.geo,
            toName: data.target.geo,
            coords: [fromCoord, toCoord]
        });
    }
    return res;
};

var color = ['#a6c84c', '#ffa022', '#FF4500'];
var series = [];

function query_task(id) {
    $.ajax({
        type : 'POST',
        url: "/web/network_detect/task/query/index",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": id
        },
        success : function(result){
            if(result.success){
                $('#task_id'+id).val(result.data.id);
                $('#task_name'+id).val(result.data.name);
                $('#task_desc'+id).val(result.data.desc);
                $('#ping_detect_steps'+id).val(result.data.ping_detect_steps);
                $('#ping_detect_num'+id).val(result.data.ping_detect_num);
                $('#ping_detect_interval'+id).val(result.data.ping_detect_interval);
                $('#ping_detect_timeout'+id).val(result.data.ping_detect_timeout);
                $('#ping_detect_size'+id).val(result.data.ping_detect_size);
                $('#traceroute_detect_steps'+id).val(result.data.traceroute_detect_steps);
                $('#traceroute_detect_num'+id).val(result.data.traceroute_detect_num);
                $('#traceroute_detect_timeout'+id).val(result.data.traceroute_detect_timeout);
                $('#curl_detect_steps'+id).val(result.data.curl_detect_steps);
                $('#curl_detect_timeout_dns'+id).val(result.data.curl_detect_timeout_dns);
                $('#curl_detect_timeout_conn'+id).val(result.data.curl_detect_timeout_conn);
                $('#curl_detect_timeout_total'+id).val(result.data.curl_detect_timeout_total);
                $('#task_uri'+id).val(result.data.curl_detect_uri);
                var resizeWorldMapContainer = function () {
                    document.getElementById('echarts_detect_network'+asset_id).style.width = window.innerWidth+'px';
                    document.getElementById('echarts_detect_network'+asset_id).style.height = window.innerHeight+'px';
                };
                var task = result.data;
                var series = [];
                var list_legend = [];
                $('#task_id'+id).val(task.id);
                $('#task_id'+id).attr("disabled",true);
                $('#div_task_id'+id).css({'display': 'block'});
                for(num in task.task_source_to_target){
                    data = task.task_source_to_target[num];
                    color_now_1 = color[data.level];
                    color_now_2 = color[data.level];
                    list_legend.push(
                        data.source.geo + '-' + data.source.name
                    );
                    list_legend.push(
                        data.target.geo + '-' + data.target.name
                    );
                    series.push({
                        name: data.source.geo + '-' + data.source.name,
                        type: 'lines',
                        zlevel: 1,
                        effect: {
                            show: true,
                            period: 6,
                            trailLength: 0.7,
                            color: '#fff',
                            symbolSize: 3
                        },
                        lineStyle: {
                            normal: {
                                color: color_now_1,
                                width: 0,
                                curveness: 0.2
                            }
                        },
                        data: convertData(data)
                    },
                    {
                        name: data.source.geo + '-' + data.source.name,
                        type: 'lines',
                        zlevel: 2,
                        symbol: ['none', 'arrow'],
                        symbolSize: 10,
                        effect: {
                            show: true,
                            period: 6,
                            trailLength: 0,
                            symbol: planePath,
                            symbolSize: 15
                        },
                        lineStyle: {
                            normal: {
                                color: color_now_1,
                                width: 1,
                                opacity: 0.6,
                                curveness: 0.2
                            }
                        },
                        data: convertData(data)
                    },
                    {
                        name: data.source.geo + '-' + data.source.name,
                        type: 'effectScatter',
                        coordinateSystem: 'geo',
                        zlevel: 2,
                        rippleEffect: {
                            brushType: 'stroke'
                        },
                        label: {
                            normal: {
                                show: true,
                                position: 'right',
                                formatter: '{b}'
                            }
                        },
                        symbolSize: function (val) {
                            return val[2] / 8;
                        },
                        itemStyle: {
                            normal: {
                                color: color[0]
                            }
                        },
                        data: [
                            {
                                name: data.source.geo + '-' + data.source.name,
                                value: [data.source.longitude, data.source.latitude, 90]
                            },
                            {
                                name: data.target.geo + '-' + data.target.name,
                                value: [data.target.longitude, data.target.latitude, 90]
                            }
                        ]
                    },
                    {
                        name: data.target.geo + '-' + data.target.name,
                        type: 'lines',
                        zlevel: 1,
                        effect: {
                            show: true,
                            period: 6,
                            trailLength: 0.7,
                            color: '#fff',
                            symbolSize: 3
                        },
                        lineStyle: {
                            normal: {
                                color: color_now_2,
                                width: 0,
                                curveness: 0.2
                            }
                        },
                        data: convertData(data)
                    },
                    {
                        name: data.target.geo + '-' + data.target.name,
                        type: 'lines',
                        zlevel: 2,
                        symbol: ['none', 'arrow'],
                        symbolSize: 10,
                        effect: {
                            show: true,
                            period: 6,
                            trailLength: 0,
                            symbol: planePath,
                            symbolSize: 15
                        },
                        lineStyle: {
                            normal: {
                                color: color_now_2,
                                width: 1,
                                opacity: 0.6,
                                curveness: 0.2
                            }
                        },
                        data: convertData(data)
                    },
                    {
                        name: data.target.geo + '-' + data.target.name,
                        type: 'effectScatter',
                        coordinateSystem: 'geo',
                        zlevel: 2,
                        rippleEffect: {
                            brushType: 'stroke'
                        },
                        label: {
                            normal: {
                                show: true,
                                position: 'right',
                                formatter: '{b}'
                            }
                        },
                        symbolSize: function (val) {
                            return val[2] / 8;
                        },
                        itemStyle: {
                            normal: {
                                color: color[0]
                            }
                        },
                        data: [
                            {
                                name: data.source.geo + '-' + data.source.name,
                                value: [data.source.longitude, data.source.latitude, 90]
                            },
                            {
                                name: data.target.geo + '-' + data.target.name,
                                value: [data.target.longitude, data.target.latitude, 90]
                            }
                        ]
                    });
                }
                option = {
                    backgroundColor: '#404a59',
                    title : {
                        text: '探测网络',
                        left: 'center',
                        textStyle : {
                            color: '#fff'
                        }
                    },
                    tooltip : {
                        trigger: 'item'
                    },
                    legend: {
                        show: false,
                        orient: 'vertical',
                        top: 'bottom',
                        left: 'right',
                        data: list_legend,
                        height: document.getElementById('echarts_detect_network'+id).style.height,
                        width: document.getElementById('echarts_detect_network'+id).style.width,
                        textStyle: {
                            color: '#fff'
                        },
                        selectedMode: 'multiple'
                    },
                    geo: {
                        map: 'china',
                        label: {
                            emphasis: {
                                show: false
                            }
                        },
                        roam: true,
                        itemStyle: {
                            normal: {
                                areaColor: '#323c48',
                                borderColor: '#404a59'
                            },
                            emphasis: {
                                areaColor: '#2a333d'
                            }
                        }
                    },
                    series: series
                };
                echarts.dispose(document.getElementById('echarts_detect_network'+id));
                resizeWorldMapContainer();
                var echarts_detect_network = echarts.init(document.getElementById('echarts_detect_network'+id));
                echarts_detect_network.setOption(option);
                echarts_detect_network.on('click', function (params) {
                    console.log(params.name);
                    if(contains(list_legend, params.name)){
                        for(le in list_legend){
                            if(params.name == list_legend[le]){
                                echarts_detect_network.dispatchAction({
                                    type: 'legendSelect',
                                    // 图例名称
                                    name: list_legend[le]
                                });
                            }else{
                                echarts_detect_network.dispatchAction({
                                    type: 'legendUnSelect',
                                    // 图例名称
                                    name: list_legend[le]
                                });
                            }

                        }
                    }else{
                        for(le in list_legend){
                            echarts_detect_network.dispatchAction({
                                type: 'legendSelect',
                                // 图例名称
                                name: list_legend[le]
                            });
                        }
                    }

                });
                window.onresize = function () {
                    //重置容器高宽
                    resizeWorldMapContainer();
                    echarts_detect_network.resize();
                };
                var table_detect_tasks_data = new Array();
                var dt_type = ['Normal', 'Warning', 'Error'];
                for(t in task.task_source_to_target){
                    table_detect_tasks_data[t] = new Array();
                    table_detect_tasks_data[t][0] = task.task_source_to_target[t].source.name;
                    table_detect_tasks_data[t][1] = task.task_source_to_target[t].target.name;
                    table_detect_tasks_data[t][2] = task.task_source_to_target[t].type;
                    table_detect_tasks_data[t][3] = dt_type[task.task_source_to_target[t].level];
                    table_detect_tasks_data[t][4] = parseFloat(task.task_source_to_target[t].ping_rtt).toFixed(3);
                    table_detect_tasks_data[t][5] = task.task_source_to_target[t].ping_lost_rate + '%';
                    table_detect_tasks_data[t][6] = parseFloat(task.task_source_to_target[t].curl_time_conn).toFixed(3);
                    table_detect_tasks_data[t][7] = parseFloat(task.task_source_to_target[t].curl_time_total).toFixed(3);
                    table_detect_tasks_data[t][8] = task.task_source_to_target[t].curl_speed;
                    table_detect_tasks_data[t][9] = task.task_source_to_target[t].curl_file_size;
                    table_detect_tasks_data[t][10] = task.task_source_to_target[t].modtime;
                }
                var table_detect_tasks = $('#detect_tasks'+id).DataTable({
                    dom: '<"html5buttons"B>frtipl',
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
                    "searching": true,
                    "aaData": table_detect_tasks_data,
                    "aoColumns": [
                        { "sTitle": "探测源" },
                        { "sTitle": "探测目标" },
                        { "sTitle": "探测类型" },
                        { "sTitle": "探测状态" },
                        { "sTitle": "Ping延迟" },
                        { "sTitle": "Ping丢包" },
                        { "sTitle": "Curl建连耗时" },
                        { "sTitle": "Curl总耗时" },
                        { "sTitle": "Curl下载速度" },
                        { "sTitle": "Curl文件大小" },
                        { "sTitle": "更新时间" }
                    ],
                    "destroy": true
                });
                $('#detect_tasks'+id+' tbody tr td').dblclick(function(e){
                    var column_now_id = $(this).context._DT_CellIndex.column;
                    var row_now_id = $(this).context._DT_CellIndex.row;
                    var detect_source = table_detect_tasks_data[row_now_id][0];
                    var detect_target = table_detect_tasks_data[row_now_id][1];
                    $('#detect_source').val(detect_source);
                    $('#detect_target').val(detect_target);
                    $("#history_type_item option[value='"+column_now_id+"']").attr("selected","");
                    $('#history_type_item').trigger("chosen:updated");
                    $("#history_period option[value='"+'1d'+"']").attr("selected","");
                    $('#history_period').trigger("chosen:updated");
                    if (column_now_id == 4){
                        var db = 'network_detect_ping';
                        var item = 'rtt';

                    }else if (column_now_id == 5){
                        var db = 'network_detect_ping';
                        var item = 'lost_rate';
                    }else if (column_now_id == 6){
                        var db = 'network_detect_curl';
                        var item = 'time_conn';
                    }else if (column_now_id == 7){
                        var db = 'network_detect_curl';
                        var item = 'time_total';
                    }else if (column_now_id == 8){
                        var db = 'network_detect_curl';
                        var item = 'speed';
                    }else if (column_now_id == 9){
                        var db = 'network_detect_curl';
                        var item = 'file_size';
                    }else{
                        var db = '';
                        var item = '';
                    }
                    if (db != ''){
                        $.ajax({
                            type : 'POST',
                            url: "/web/network_detect/task/query/history",
                            headers: {
                                Accept: "application/json; charset=utf-8"
                            },
                            data: {
                                "db": db,
                                'item': item,
                                'source': detect_source,
                                'target': detect_target,
                                'period': $('#history_period option:selected').val(),
                                'task_id': asset_id
                            },
                            success : function(result){
                                if(result.success){
                                    var resizeWorldMapContainer = function () {
                                        document.getElementById('echarts_detect_history').style.width = window.innerWidth+'px';
                                        document.getElementById('echarts_detect_history').style.height = window.innerHeight+'px';
                                    };
                                    resizeWorldMapContainer();
                                    var series_data = [];
                                    for (var i in result.data) {
                                        series_data.push(result.data[i]);
                                    }
                                    var echarts_detect_history = echarts.init(document.getElementById('echarts_detect_history'));
                                    option = {
                                        title: {
                                            text: '查询数据'
                                        },
                                        legend: {
                                            show: false,
                                            height: document.getElementById('echarts_detect_history').style.height,
                                            width: document.getElementById('echarts_detect_history').style.width,
                                        },
                                        tooltip: {
                                            trigger: 'axis',
                                            formatter: function (params) {
                                                params = params[0];
                                                var date = new Date(params.value[0]);
                                                return date.format("YYYY-mm-dd HH:MM:SS") + ' : ' + params.value[1];
                                            },
                                            axisPointer: {
                                                animation: false
                                            }
                                        },
                                        xAxis: {
                                            type: 'time',
                                            splitLine: {
                                                show: false
                                            }
                                        },
                                        yAxis: {
                                            type: 'value',
                                            boundaryGap: [0, '100%'],
                                            splitLine: {
                                                show: false
                                            }
                                        },
                                        series: [{
                                            name: '查询数据',
                                            type: 'line',
                                            showSymbol: false,
                                            hoverAnimation: false,
                                            itemStyle: {
                                                normal: {
                                                    color: '#1ab394'
                                                }
                                            },
                                            data: series_data
                                        }]
                                    };
                                    echarts_detect_history.setOption(option);
                                    $('#div_history').css({"display": "block"});
                                    printMsg(result.msg,'Success');
                                }else{
                                    printMsg(result.msg,'error');
                                }
                            }
                        });
                    }

                });
                $('#detect_tasks'+id).on('draw.dt',function() {
                $('#detect_tasks'+id+' tbody tr td').unbind("dblclick");
                $('#detect_tasks'+id+' tbody tr td').dblclick(function(e){
                    var column_now_id = $(this).context._DT_CellIndex.column;
                    var row_now_id = $(this).context._DT_CellIndex.row;
                    var detect_source = table_detect_tasks_data[row_now_id][0];
                    var detect_target = table_detect_tasks_data[row_now_id][1];
                    $('#detect_source').val(detect_source);
                    $('#detect_target').val(detect_target);
                    $("#history_type_item option[value='"+column_now_id+"']").attr("selected","");
                    $('#history_type_item').trigger("chosen:updated");
                    $("#history_period option[value='"+'1d'+"']").attr("selected","");
                    $('#history_period').trigger("chosen:updated");
                    if (column_now_id == 4){
                        var db = 'network_detect_ping';
                        var item = 'rtt';

                    }else if (column_now_id == 5){
                        var db = 'network_detect_ping';
                        var item = 'lost_rate';
                    }else if (column_now_id == 6){
                        var db = 'network_detect_curl';
                        var item = 'time_conn';
                    }else if (column_now_id == 7){
                        var db = 'network_detect_curl';
                        var item = 'time_total';
                    }else if (column_now_id == 8){
                        var db = 'network_detect_curl';
                        var item = 'speed';
                    }else if (column_now_id == 9){
                        var db = 'network_detect_curl';
                        var item = 'file_size';
                    }else{
                        var db = '';
                        var item = '';
                    }
                    if (db != ''){
                        $.ajax({
                            type : 'POST',
                            url: "/web/network_detect/task/query/history",
                            headers: {
                                Accept: "application/json; charset=utf-8"
                            },
                            data: {
                                "db": db,
                                'item': item,
                                'source': detect_source,
                                'target': detect_target,
                                'period': $('#history_period option:selected').val(),
                                'task_id': asset_id
                            },
                            success : function(result){
                                if(result.success){
                                    var resizeWorldMapContainer = function () {
                                        document.getElementById('echarts_detect_history').style.width = window.innerWidth+'px';
                                        document.getElementById('echarts_detect_history').style.height = window.innerHeight+'px';
                                    };
                                    resizeWorldMapContainer();
                                    var series_data = [];
                                    for (var i in result.data) {
                                        series_data.push(result.data[i]);
                                    }
                                    var echarts_detect_history = echarts.init(document.getElementById('echarts_detect_history'));
                                    option = {
                                        title: {
                                            text: '查询数据'
                                        },
                                        legend: {
                                            show: false,
                                            height: document.getElementById('echarts_detect_history').style.height,
                                            width: document.getElementById('echarts_detect_history').style.width,
                                        },
                                        tooltip: {
                                            trigger: 'axis',
                                            formatter: function (params) {
                                                params = params[0];
                                                var date = new Date(params.value[0]);
                                                return date.format("YYYY-mm-dd HH:MM:SS") + ' : ' + params.value[1];
                                            },
                                            axisPointer: {
                                                animation: false
                                            }
                                        },
                                        xAxis: {
                                            type: 'time',
                                            splitLine: {
                                                show: false
                                            }
                                        },
                                        yAxis: {
                                            type: 'value',
                                            boundaryGap: [0, '100%'],
                                            splitLine: {
                                                show: false
                                            }
                                        },
                                        series: [{
                                            name: '查询数据',
                                            type: 'line',
                                            showSymbol: false,
                                            hoverAnimation: false,
                                            itemStyle: {
                                                normal: {
                                                    color: '#1ab394'
                                                }
                                            },
                                            data: series_data
                                        }]
                                    };
                                    echarts_detect_history.setOption(option);
                                    $('#div_history').css({"display": "block"});
                                    printMsg(result.msg,'Success');
                                }else{
                                    printMsg(result.msg,'error');
                                }
                            }
                        });
                    }

                });
                });
                printMsg(result.msg,'Success');
            }else{
                printMsg(result.msg,'error');
            }
        }
    });
    $('#myModal'+ id).modal('show');
}
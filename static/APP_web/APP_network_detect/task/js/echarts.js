
var planePath = 'path://M1705.06,1318.313v-89.254l-319.9-221.799l0.073-208.063c0.521-84.662-26.629-121.796-63.961-121.491c-37.332-0.305-64.482,36.829-63.961,121.491l0.073,208.063l-319.9,221.799v89.254l330.343-157.288l12.238,241.308l-134.449,92.931l0.531,42.034l175.125-42.917l175.125,42.917l0.531-42.034l-134.449-92.931l12.238-241.308L1705.06,1318.313z';


function randomColor(color, str) {
    return color[Math.round(str.length%color.length)];
}
function randomData() {
    return Math.round(Math.random());
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
var resizeWorldMapContainer = function () {
    document.getElementById('echarts_detect_network').style.width = (parseInt(window.innerWidth)-20)+'px';
    document.getElementById('echarts_detect_network').style.height = window.innerHeight+'px';
};
var color = ['#a6c84c', '#ffa022', '#FF4500'];
var series = [];
function network_detect_task_add_single(){
    $.ajax({
        type : 'POST',
        url: "/web/network_detect/task/add_single/",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": $('#task_id').val(),
            "name": $('#task_name').val(),
            "desc": $('#task_desc').val(),
            "ping": $('#switch_ping').is(':checked'),
            "ping_detect_steps": $('#ping_detect_steps').val(),
            "ping_detect_num": $('#ping_detect_num').val(),
            "ping_detect_interval": $('#ping_detect_interval').val(),
            "ping_detect_timeout": $('#ping_detect_timeout').val(),
            "ping_detect_size": $('#ping_detect_size').val(),
            "traceroute": $('#switch_traceroute').is(':checked'),
            "traceroute_detect_steps": $('#traceroute_detect_steps').val(),
            "traceroute_detect_num": $('#traceroute_detect_num').val(),
            "traceroute_detect_timeout": $('#traceroute_detect_timeout').val(),
            "curl": $('#switch_curl').is(':checked'),
            "curl_detect_steps": $('#curl_detect_steps').val(),
            "curl_detect_timeout_dns": $('#curl_detect_timeout_dns').val(),
            "curl_detect_timeout_conn": $('#curl_detect_timeout_conn').val(),
            "curl_detect_timeout_total": $('#curl_detect_timeout_total').val(),
            "task_source":  $('#task_source option:selected').val(),
            "task_target":  $('#task_target option:selected').val(),
            "task_uri": $('#task_uri').val(),
        },
        success : function(result){
            if(result.success){
                $('#task_id').val(result.data.id);
                $('#task_name').val(result.data.name);
                $('#task_desc').val(result.data.desc);
                $('#ping_detect_steps').val(result.data.ping_detect_steps);
                $('#ping_detect_num').val(result.data.ping_detect_num);
                $('#ping_detect_interval').val(result.data.ping_detect_interval);
                $('#ping_detect_timeout').val(result.data.ping_detect_timeout);
                $('#ping_detect_size').val(result.data.ping_detect_size);
                $('#traceroute_detect_steps').val(result.data.traceroute_detect_steps);
                $('#traceroute_detect_num').val(result.data.traceroute_detect_num);
                $('#traceroute_detect_timeout').val(result.data.traceroute_detect_timeout);
                $('#curl_detect_steps').val(result.data.curl_detect_steps);
                $('#curl_detect_timeout_dns').val(result.data.curl_detect_timeout_dns);
                $('#curl_detect_timeout_conn').val(result.data.curl_detect_timeout_conn);
                $('#curl_detect_timeout_total').val(result.data.curl_detect_timeout_total);
                $('#task_uri').val(result.data.curl_detect_uri);
                var resizeWorldMapContainer = function () {
                    document.getElementById('echarts_detect_network').style.width = window.innerWidth+'px';
                    document.getElementById('echarts_detect_network').style.height = window.innerHeight+'px';
                };
                var task = result.data;
                var series = [];
                var list_legend = [];
                $('#task_id').val(task.id);
                $('#task_id').attr("disabled",true);
                $('#div_task_id').css({'display': 'block'});
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
                        height: document.getElementById('echarts_detect_network').style.height,
                        width: document.getElementById('echarts_detect_network').style.width,
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
                echarts.dispose(document.getElementById('echarts_detect_network'));
                resizeWorldMapContainer();
                var echarts_detect_network = echarts.init(document.getElementById('echarts_detect_network'));
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
                var table_detect_tasks = $('#detect_tasks').DataTable({
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
                        { "sTitle": "更新时间" },
                    ],
                    "destroy": true
                });
                printMsg(result.msg,'Success');
            }else{
                printMsg(result.msg,'error');
            }

        }
    });
};

function network_detect_task_del_single(){
    $.ajax({
        type : 'POST',
        url: "/web/network_detect/task/del_single/",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "id": $('#task_id').val(),
            "name": $('#task_name').val(),
            "desc": $('#task_desc').val(),
            "ping": $('#switch_ping').is(':checked'),
            "ping_detect_steps": $('#ping_detect_steps').val(),
            "ping_detect_num": $('#ping_detect_num').val(),
            "ping_detect_interval": $('#ping_detect_interval').val(),
            "ping_detect_timeout": $('#ping_detect_timeout').val(),
            "ping_detect_size": $('#ping_detect_size').val(),
            "traceroute": $('#switch_traceroute').is(':checked'),
            "traceroute_detect_steps": $('#traceroute_detect_steps').val(),
            "traceroute_detect_num": $('#traceroute_detect_num').val(),
            "traceroute_detect_timeout": $('#traceroute_detect_timeout').val(),
            "curl": $('#switch_curl').is(':checked'),
            "curl_detect_steps": $('#curl_detect_steps').val(),
            "curl_detect_timeout_dns": $('#curl_detect_timeout_dns').val(),
            "curl_detect_timeout_conn": $('#curl_detect_timeout_conn').val(),
            "curl_detect_timeout_total": $('#curl_detect_timeout_total').val(),
            "task_source":  $('#task_source option:selected').val(),
            "task_target":  $('#task_target option:selected').val(),
            "task_uri": $('#task_uri').val(),
        },
        success : function(result){
            if(result.success){
                $('#task_id').val(result.data.id);
                $('#task_name').val(result.data.name);
                $('#task_desc').val(result.data.desc);
                $('#ping_detect_steps').val(result.data.ping_detect_steps);
                $('#ping_detect_num').val(result.data.ping_detect_num);
                $('#ping_detect_interval').val(result.data.ping_detect_interval);
                $('#ping_detect_timeout').val(result.data.ping_detect_timeout);
                $('#ping_detect_size').val(result.data.ping_detect_size);
                $('#traceroute_detect_steps').val(result.data.traceroute_detect_steps);
                $('#traceroute_detect_num').val(result.data.traceroute_detect_num);
                $('#traceroute_detect_timeout').val(result.data.traceroute_detect_timeout);
                $('#curl_detect_steps').val(result.data.curl_detect_steps);
                $('#curl_detect_timeout_dns').val(result.data.curl_detect_timeout_dns);
                $('#curl_detect_timeout_conn').val(result.data.curl_detect_timeout_conn);
                $('#curl_detect_timeout_total').val(result.data.curl_detect_timeout_total);
                $('#task_uri').val(result.data.curl_detect_uri);
                var resizeWorldMapContainer = function () {
                    document.getElementById('echarts_detect_network').style.width = window.innerWidth+'px';
                    document.getElementById('echarts_detect_network').style.height = window.innerHeight+'px';
                };
                var task = result.data;
                var series = [];
                var list_legend = [];
                $('#task_id').val(task.id);
                $('#task_id').attr("disabled",true);
                $('#div_task_id').css({'display': 'block'});
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
                        height: document.getElementById('echarts_detect_network').style.height,
                        width: document.getElementById('echarts_detect_network').style.width,
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
                echarts.dispose(document.getElementById('echarts_detect_network'));
                resizeWorldMapContainer();
                var echarts_detect_network = echarts.init(document.getElementById('echarts_detect_network'));
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
                var table_detect_tasks = $('#detect_tasks').DataTable({
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
                        { "sTitle": "更新时间" },
                    ],
                    "destroy": true
                });
                printMsg(result.msg,'Success');
            }else{
                printMsg(result.msg,'error');
            }

        }
    });
};

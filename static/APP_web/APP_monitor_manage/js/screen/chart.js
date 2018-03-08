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
function resizeChartContainer() {
    document.getElementById('echarts_query_history').style.width = window.innerWidth+'px';
    document.getElementById('echarts_query_history').style.height = (window.innerHeight-30)+'px';
}
function init_chart(chart) {
    resizeChartContainer();
    var echarts_query_history = echarts.init(document.getElementById('echarts_query_history'));
    option = {
        title: {
            text: chart.title
        },
        legend: {
            show: false,
            height: document.getElementById('echarts_query_history').style.height,
            width: document.getElementById('echarts_query_history').style.width,
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
            name: chart.data.data.name,
            type: 'line',
            showSymbol: false,
            hoverAnimation: false,
            itemStyle: {
                normal: {
                    color: '#1ab394'
                }
            },
            "markLine": {
                "data": [
                    {
                        "type": "max",
                        "name": "最大值",
                        "valueDim": null
                    },
                    {
                        "type": "average",
                        "name": "平均值",
                        "valueDim": null
                    }
                ],
                "symbolSize": 10
            },
            data: chart.data.data
        }]
    };
    echarts_query_history.setOption(option);
}
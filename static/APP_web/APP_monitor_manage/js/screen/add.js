function update_screen(){
    $('#div_chart').find('iframe').each(function () {
        var asset_id = $('#select_asset option:selected').val();
        var time_start = $('#time_chart_start').val();
        var time_end = $('#time_chart_end').val();
        var url = $(this).attr('src');
        var chart_id = $(this).data('id');
        if(!url){
            url = "/web/monitor_manage/screen/show_chart?id="+chart_id;
        }
        url = change_url_arg(url, 'asset_id', asset_id);
        url = change_url_arg(url, 'time_start', time_start);
        url = change_url_arg(url, 'time_end', time_end);
        $(this).attr('src', url);
    });
}
function change_url_arg(url,arg,arg_val){
       var pattern=arg+'=([^&]*)';
       var replaceText=arg+'='+arg_val;
       if(url.match(pattern)){
           var tmp='/('+ arg+'=)([^&]*)/gi';
           tmp=url.replace(eval(tmp),replaceText);
           return tmp;
       }else{
           if(url.match('[\?]')){
               return url+'&'+replaceText;
           }else{
               return url+'?'+replaceText;
           }
      }
       return url+'\n'+arg+'\n'+arg_val;
   }
function add_chart() {
    var screen_id = $('#screen_id').val();
    if(screen_id){
        var title = $('#chart_title').val();
        var type = $('#select_chart_type option:selected').val();
        var item = $('#select_property option:selected').val();
        var asset_id = $('#select_asset option:selected').val();
        var time_start = $('#time_chart_start').val();
        var time_end = $('#time_chart_end').val();
        $.ajax({
            type : 'POST',
            url: "/web/monitor_manage/screen/add_chart",
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            data: {
                "title": title,
                "type": type,
                "item": item,
                "screen_id": screen_id,
            },
            success : function(result){
                if(result.success){
                    var url = "/web/monitor_manage/screen/show_chart?id="+result.data.id+"&time_start="+time_start+"&time_end="+time_end+"&asset_id="+asset_id;
                    var html = '<div class="col-lg-6 col-md-6 col-sm-6"><iframe data-id="'+result.data.id+'" id="page-content"  height="400px" width="100%" frameborder="no" border="0" marginwidth="0" marginheight="0" scrolling="yes" allowtransparency="yes" src="'+url+'"></iframe></div>';
                    $('#div_chart').append(html);
                    parent.parent.printMsg(result.msg,'Success');
                }else{
                    parent.parent.printMsg(result.msg,'error');
                }
            }
        });
    }else{
        parent.parent.printMsg('请先保存屏幕基本信息','error');
    }

}
function update_select_asset() {
    var tag = $('#select_tag option:selected').val();
    $.ajax({
        type : 'POST',
        url: "/web/asset_manage/tag/query_asset",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "tag_id": tag,
        },
        success : function(result){
            if(result.success){
                $('#select_asset').empty();
                for(var i in result.data){
                    $('#select_asset').append("<option value='"+result.data[i].id+"'>"+result.data[i].hostname+"</option>");
                }
                $("#select_asset option[value='"+result.data[0].id+"']").attr("selected","");
                $('#select_asset').trigger("chosen:updated");
                update_select_property();
                update_screen();
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
    });

}
function update_select_property() {
    var asset = $('#select_asset option:selected').val();
    $.ajax({
        type : 'POST',
        url: "/web/asset_manage/query_property",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "asset_id": asset,
        },
        success : function(result){
            if(result.success){
                $('#select_property').empty();
                for(var i in result.data){
                    $('#select_property').append("<option value='"+i+"'>"+i+"</option>");
                }
                $('#select_property').trigger("chosen:updated");
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
    });
}
function init_time() {
    $('#time_chart_start').datetimepicker({
        format: 'Y-m-d H:i',
        formatDate: 'Y-m-d',
        formatTime: 'H:i',
    });
    $('#time_chart_end').datetimepicker({
        format: 'Y-m-d H:i',
        formatDate: 'Y-m-d',
        formatTime: 'H:i',
    });
    $.datetimepicker.setLocale('zh');
    var time_now = new Date();
    $('#time_chart_start').val(timestampToTime(time_now-3600000));
    $('#time_chart_end').val(timestampToTime(time_now));
}
function getzf(num){
    if(parseInt(num) < 10){
        num = '0'+num;
    }
    return num;
}
function timestampToTime(timestamp) {
    var date = new Date(timestamp);
    var Y = date.getFullYear() + '-';
    var M = (date.getMonth()+1) + '-';
    var D = date.getDate() + ' ';
    var h = date.getHours() + ':';
    var m = date.getMinutes();
    return Y+getzf(M)+getzf(D)+getzf(h)+getzf(m);
}
function add_person() {
    var screen_id = $('#screen_id').val();
    if(screen_id){
        var user_id = $('#select_people option:selected').val();
        $.ajax({
            type : 'POST',
            url: "/web/monitor_manage/screen/add_person",
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            data: {
                "screen_id": screen_id,
                "user_id": user_id,
            },
            success : function(result){
                if(result.success){
                    var html_btn = '<button type="button" class="btn btn-primary" >'+result.data.username+'</button>'
                    $('#div_people').append(html_btn);
                    parent.parent.printMsg(result.msg,'Success');
                }else{
                    parent.parent.printMsg(result.msg,'error');
                }
            }
        });
    }else{
        parent.parent.printMsg('请先保存屏幕基本信息','error');
    }
}
function show_add_people(tag){
    if(tag){
        $('#div_add_people').css('display', 'block');
        $('#btn_add_people').text('关闭');
        $('#btn_add_people').attr('onclick', 'show_add_people(false)')
    }else{
        $('#div_add_people').css('display', 'none');
        $('#btn_add_people').text('添加');
        $('#btn_add_people').attr('onclick', 'show_add_people(true)')
    }
}
function show_add_chart(tag){
    if(tag){
        $('#div_add_chart').css('display', 'block');
        $('#btn_add_chart').text('关闭');
        $('#btn_add_chart').attr('onclick', 'show_add_chart(false)')
    }else{
        $('#div_add_chart').css('display', 'none');
        $('#btn_add_chart').text('添加');
        $('#btn_add_chart').attr('onclick', 'show_add_chart(true)')
    }
}
function save_screen() {
    var name_cn = $('#screen_name_cn').val();
    var name_en = $('#screen_name_en').val();
    var tag = $('#select_tag option:selected').val();
    $.ajax({
        type : 'POST',
        url: "/web/monitor_manage/screen/save",
        dataType: 'json',
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "name_cn": name_cn,
            "name_en": name_en,
            "tag": tag
        },
        success : function(result){
            if(result.success){
                $('#screen_id').val(result.data.id);
                $('#div_screen_id').css('display', 'block');
                update_select_asset();
                parent.parent.printMsg(result.msg,'Success');
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
    });
}
$(document).ready(function() {
    var config = {
        '.chosen-select-inner': {
            search_contains: true,
            width: "100%"
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
    init_time();
});

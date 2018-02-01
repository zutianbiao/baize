$("#ping_detect_steps" + asset_id).TouchSpin({
    min: 60,
    max: 300,
    buttondown_class: 'btn btn-white',
    buttonup_class: 'btn btn-white'
});
$("#ping_detect_num" + asset_id).TouchSpin({
    min: 1,
    max: 100,
    buttondown_class: 'btn btn-white',
    buttonup_class: 'btn btn-white'
});
$("#ping_detect_interval" + asset_id).TouchSpin({
    min: 0.01,
    max: 1,
    step: 0.1,
    decimals: 2,
    buttondown_class: 'btn btn-white',
    buttonup_class: 'btn btn-white'
});
$("#ping_detect_timeout" + asset_id).TouchSpin({
    min: 1,
    max: 3,
    buttondown_class: 'btn btn-white',
    buttonup_class: 'btn btn-white'
});
$("#ping_detect_size" + asset_id).TouchSpin({
    min: 1,
    max: 256,
    buttondown_class: 'btn btn-white',
    buttonup_class: 'btn btn-white'
});
$("#traceroute_detect_steps" + asset_id).TouchSpin({
    min: 60,
    max: 300,
    buttondown_class: 'btn btn-white',
    buttonup_class: 'btn btn-white'
});
$("#traceroute_detect_num" + asset_id).TouchSpin({
    min: 1,
    max: 100,
    buttondown_class: 'btn btn-white',
    buttonup_class: 'btn btn-white'
});
$("#traceroute_detect_timeout" + asset_id).TouchSpin({
    min: 1,
    max: 3,
    buttondown_class: 'btn btn-white',
    buttonup_class: 'btn btn-white'
});
$("#curl_detect_steps" + asset_id).TouchSpin({
    min: 300,
    max: 3600,
    buttondown_class: 'btn btn-white',
    buttonup_class: 'btn btn-white'
});
$("#curl_detect_timeout_dns" + asset_id).TouchSpin({
    min: 3,
    max: 10,
    buttondown_class: 'btn btn-white',
    buttonup_class: 'btn btn-white'
});
$("#curl_detect_timeout_conn" + asset_id).TouchSpin({
    min: 3,
    max: 10,
    buttondown_class: 'btn btn-white',
    buttonup_class: 'btn btn-white'
});
$("#curl_detect_timeout_total" + asset_id).TouchSpin({
    min: 300,
    max: 600,
    buttondown_class: 'btn btn-white',
    buttonup_class: 'btn btn-white'
});

var elem = document.querySelector('#switch_ping' + asset_id);
var switchery_ping = new Switchery(elem, { color: '#1AB394' });
var elem = document.querySelector('#switch_traceroute' + asset_id);
var switchery_traceroute = new Switchery(elem, { color: '#1AB394' });
var elem = document.querySelector('#switch_curl' + asset_id);
var switchery_curl = new Switchery(elem, { color: '#1AB394' });
$('#switch_ping' + asset_id).change(function(){
    $("#collapse_link_ping" + asset_id).click();
});
$('#switch_traceroute' + asset_id).change(function(){
    $("#collapse_link_traceroute" + asset_id).click();
});
$('#switch_curl' + asset_id).change(function(){
    $("#collapse_link_curl" + asset_id).click();
});
function detect_save_role(){
    $.ajax({
        type : 'POST',
        url: "/web/network_detect/role/save/",
        data: {
            "desc": $('#role_desc' + asset_id).val(),
            "name": $('#role_name' + asset_id).val(),
            "target": $('#role_target' + asset_id).val(),
            "asset": $('#role_asset'+ asset_id + 'option:selected').val(),
            "country": $('#role_country'+ asset_id + ' option:selected').val(),
            "province": $('#role_province'+ asset_id + ' option:selected').val(),
            "city": $('#role_city'+ asset_id + ' option:selected').val(),
            "area": $('#role_area'+ asset_id + ' option:selected').val(),
            "isp": $('#role_isp'+ asset_id + ' option:selected').val()
        },
        success : function(result){
            if(result.success){
                printMsg(result.msg,'Success');
            }else{
                printMsg(result.msg,'error');
            }

        }
    });
}

function contains(arr, obj) {
    var i = arr.length;
    while (i--) {
        if (arr[i] === obj) {
            return true;
        }
    }
    return false;
}

$('#role_country'+ asset_id).change(function(){
    var country = $('#role_country'+ asset_id + ' option:selected').val();
    var province = $('#role_province'+ asset_id + ' option:selected').val();
    var city = $('#role_city'+ asset_id + ' option:selected').val();
    var area = $('#role_area'+ asset_id + ' option:selected').val();
    var obj_province = $('#role_province'+ asset_id);
    var obj_city = $('#role_city'+ asset_id);
    var obj_area = $('#role_area'+ asset_id);
    var list_province = new Array();
    var list_area = new Array();
    var list_city = new Array();
    $("#role_province"+ asset_id).empty();
    $("#role_city"+ asset_id).empty();
    $('#role_area'+ asset_id).empty();
    obj_province.append("<option value='"+"'>"+"省份"+"</option>");
    obj_city.append("<option value='"+"'>"+"城市"+"</option>");
    obj_area.append("<option value='"+"'>"+"区县"+"</option>");
    if(country!=''){
        for(i in list_geo){
            if(list_geo[i].country==country){
                if(list_geo[i].province!=''){
                    if(!contains(list_province, list_geo[i].province)){
                        obj_province.append("<option value='"+list_geo[i].province+"'>"+list_geo[i].province+"</option>");
                        list_province.push(list_geo[i].province);
                    }
                }
                if(list_geo[i].city!=''){
                    if(!contains(list_city, list_geo[i].city)){
                        obj_city.append("<option value='"+list_geo[i].city+"'>"+list_geo[i].city+"</option>");
                        list_city.push(list_geo[i].city);
                    }
                }
                if(list_geo[i].area!=''){
                    if(!contains(list_area, list_geo[i].area)){
                        obj_area.append("<option value='"+list_geo[i].area+"'>"+list_geo[i].area+"</option>");
                        list_area.push(list_geo[i].area);
                    }
                }
            }
        }
        $("#role_province"+ asset_id +" option[value='"+province+"']").attr("selected","");
        $("#role_city"+ asset_id +" option[value='"+city+"']").attr("selected","");
        $("#role_area"+ asset_id +" option[value='"+area+"']").attr("selected","");
        obj_province.trigger("chosen:updated");
        obj_city.trigger("chosen:updated");
        obj_area.trigger("chosen:updated");
    }
});

$('#role_province'+ asset_id).change(function(){
    var country = $('#role_country'+ asset_id + ' option:selected').val();
    var province = $('#role_province'+ asset_id + ' option:selected').val();
    var city = $('#role_city'+ asset_id + ' option:selected').val();
    var area = $('#role_area'+ asset_id + ' option:selected').val();
    var obj_country = $('#role_country'+ asset_id);
    var obj_city = $('#role_city'+ asset_id);
    var obj_area = $('#role_area'+ asset_id);
    var list_country = new Array();
    var list_area = new Array();
    var list_city = new Array();
    $("#role_country"+ asset_id).empty();
    $("#role_city"+ asset_id).empty();
    $('#role_area'+ asset_id).empty();
    obj_country.append("<option value='"+"'>"+"国家"+"</option>");
    obj_city.append("<option value='"+"'>"+"城市"+"</option>");
    obj_area.append("<option value='"+"'>"+"区县"+"</option>");
    if(province!=''){
        for(i in list_geo){
            if(list_geo[i].province==province){
                if(list_geo[i].country!=''){
                    if(!contains(list_country, list_geo[i].country)){
                        obj_country.append("<option value='"+list_geo[i].country+"'>"+list_geo[i].country+"</option>");
                        list_country.push(list_geo[i].country);
                    }
                }
                if(list_geo[i].city!=''){
                    if(!contains(list_city, list_geo[i].city)){
                        obj_city.append("<option value='"+list_geo[i].city+"'>"+list_geo[i].city+"</option>");
                        list_city.push(list_geo[i].city);
                    }
                }
                if(list_geo[i].area!=''){
                    if(!contains(list_area, list_geo[i].area)){
                        obj_area.append("<option value='"+list_geo[i].area+"'>"+list_geo[i].area+"</option>");
                        list_area.push(list_geo[i].area);
                    }
                }
            }
        }
        $("#role_country"+ asset_id + " option[value='"+country+"']").attr("selected","");
        $("#role_city"+ asset_id + " option[value='"+city+"']").attr("selected","");
        $("#role_area"+ asset_id + " option[value='"+area+"']").attr("selected","");
        obj_country.trigger("chosen:updated");
        obj_city.trigger("chosen:updated");
        obj_area.trigger("chosen:updated");
    }
});

$('#role_city'+ asset_id).change(function(){
    var country = $('#role_country'+ asset_id + ' option:selected').val();
    var province = $('#role_province'+ asset_id + ' option:selected').val();
    var city = $('#role_city'+ asset_id + ' option:selected').val();
    var area = $('#role_area'+ asset_id + ' option:selected').val();
    var obj_country = $('#role_country'+ asset_id);
    var obj_province = $('#role_province'+ asset_id);
    var obj_area = $('#role_area'+ asset_id);
    var list_country = new Array();
    var list_area = new Array();
    var list_province = new Array();
    $("#role_country"+ asset_id).empty();
    $("#role_province"+ asset_id).empty();
    $('#role_area'+ asset_id).empty();
    obj_country.append("<option value='"+"'>"+"国家"+"</option>");
    obj_province.append("<option value='"+"'>"+"省份"+"</option>");
    obj_area.append("<option value='"+"'>"+"区县"+"</option>");
    if(city!=''){
        for(i in list_geo){
            if(list_geo[i].city==city){
                if(list_geo[i].country!=''){
                    if(!contains(list_country, list_geo[i].country)){
                        obj_country.append("<option value='"+list_geo[i].country+"'>"+list_geo[i].country+"</option>");
                        list_country.push(list_geo[i].country);
                    }
                }
                if(list_geo[i].province!=''){
                    if(!contains(list_province, list_geo[i].province)){
                        obj_province.append("<option value='"+list_geo[i].province+"'>"+list_geo[i].province+"</option>");
                        list_province.push(list_geo[i].province);
                    }
                }
                if(list_geo[i].area!=''){
                    if(!contains(list_area, list_geo[i].area)){
                        obj_area.append("<option value='"+list_geo[i].area+"'>"+list_geo[i].area+"</option>");
                        list_area.push(list_geo[i].area);
                    }
                }
            }
        }
        $("#role_country"+ asset_id + " option[value='"+country+"']").attr("selected","");
        $("#role_province"+ asset_id + " option[value='"+province+"']").attr("selected","");
        $("#role_area"+ asset_id + " option[value='"+area+"']").attr("selected","");
        obj_country.trigger("chosen:updated");
        obj_province.trigger("chosen:updated");
        obj_area.trigger("chosen:updated");
    }
});

$('#role_area'+ asset_id).change(function(){
    var country = $('#role_country option:selected').val();
    var province = $('#role_province option:selected').val();
    var city = $('#role_city option:selected').val();
    var area = $('#role_area option:selected').val();
    var obj_country = $('#role_country'+ asset_id);
    var obj_province = $('#role_province'+ asset_id);
    var obj_city = $('#role_city'+ asset_id);
    var list_country = new Array();
    var list_city = new Array();
    var list_province = new Array();
    $("#role_country"+ asset_id).empty();
    $("#role_province"+ asset_id).empty();
    $('#role_city'+ asset_id).empty();
    obj_country.append("<option value='"+"'>"+"国家"+"</option>");
    obj_province.append("<option value='"+"'>"+"省份"+"</option>");
    obj_city.append("<option value='"+"'>"+"城市"+"</option>");
    if(area!=''){
        for(i in list_geo){
            if(list_geo[i].area==area){
                if(list_geo[i].country!=''){
                    if(!contains(list_country, list_geo[i].country)){
                        obj_country.append("<option value='"+list_geo[i].country+"'>"+list_geo[i].country+"</option>");
                        list_country.push(list_geo[i].country);
                    }
                }
                if(list_geo[i].province!=''){
                    if(!contains(list_province, list_geo[i].province)){
                        obj_province.append("<option value='"+list_geo[i].province+"'>"+list_geo[i].province+"</option>");
                        list_province.push(list_geo[i].province);
                    }
                }
                if(list_geo[i].city!=''){
                    if(!contains(list_city, list_geo[i].city)){
                        obj_city.append("<option value='"+list_geo[i].city+"'>"+list_geo[i].city+"</option>");
                        list_city.push(list_geo[i].city);
                    }
                }
            }
        }
        $("#role_country option[value='"+country+"']").attr("selected","");
        $("#role_province option[value='"+province+"']").attr("selected","");
        $("#role_city option[value='"+city+"']").attr("selected","");
        obj_country.trigger("chosen:updated");
        obj_province.trigger("chosen:updated");
        obj_city.trigger("chosen:updated");
    }
});







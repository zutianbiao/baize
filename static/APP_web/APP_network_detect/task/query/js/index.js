function input_readonly() {
    $('#task_id'+asset_id).attr("disabled",true);
    $('#task_name'+asset_id).attr("disabled",true);
    $('#task_desc'+asset_id).attr("disabled",true);
    $('#switch_ping'+asset_id).is(':unchecked'),
    $('#ping_detect_steps'+asset_id).attr("disabled",true);
    $('#ping_detect_num'+asset_id).attr("disabled",true);
    $('#ping_detect_interval'+asset_id).attr("disabled",true);
    $('#ping_detect_timeout'+asset_id).attr("disabled",true);
    $('#ping_detect_size'+asset_id).attr("disabled",true);
    $('#switch_traceroute'+asset_id).is(':unchecked'),
    $('#traceroute_detect_steps'+asset_id).attr("disabled",true);
    $('#traceroute_detect_num'+asset_id).attr("disabled",true);
    $('#traceroute_detect_timeout'+asset_id).attr("disabled",true);
    $('#switch_curl'+asset_id).is(':unchecked'),
    $('#curl_detect_steps'+asset_id).attr("disabled",true);
    $('#curl_detect_timeout_dns'+asset_id).attr("disabled",true);
    $('#curl_detect_timeout_conn'+asset_id).attr("disabled",true);
    $('#curl_detect_timeout_total'+asset_id).attr("disabled",true);
    $('#task_source'+asset_id + ' option:selected').attr("disabled",true);
    $('#task_target'+asset_id + ' option:selected').attr("disabled",true);
    $('#task_uri'+asset_id).attr("disabled",true);
}
function input_modify() {
    $('#task_id'+asset_id).removeAttr("disabled");
    $('#task_name'+asset_id).removeAttr("disabled");
    $('#task_desc'+asset_id).removeAttr("disabled");
    $('#switch_ping'+asset_id).is(':checked'),
    $('#ping_detect_steps'+asset_id).removeAttr("disabled");
    $('#ping_detect_num'+asset_id).removeAttr("disabled");
    $('#ping_detect_interval'+asset_id).removeAttr("disabled");
    $('#ping_detect_timeout'+asset_id).removeAttr("disabled");
    $('#ping_detect_size'+asset_id).removeAttr("disabled");
    $('#switch_traceroute'+asset_id).is(':checked'),
    $('#traceroute_detect_steps'+asset_id).removeAttr("disabled");
    $('#traceroute_detect_num'+asset_id).removeAttr("disabled");
    $('#traceroute_detect_timeout'+asset_id).removeAttr("disabled");
    $('#switch_curl'+asset_id).is(':checked'),
    $('#curl_detect_steps'+asset_id).removeAttr("disabled");
    $('#curl_detect_timeout_dns'+asset_id).removeAttr("disabled");
    $('#curl_detect_timeout_conn'+asset_id).removeAttr("disabled");
    $('#curl_detect_timeout_total'+asset_id).removeAttr("disabled");
    $('#task_source'+asset_id+' option:selected').removeAttr("disabled");
    $('#task_target'+asset_id+' option:selected').removeAttr("disabled");
    $('#task_uri'+asset_id).removeAttr("disabled");
}
input_readonly()


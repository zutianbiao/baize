$(document).ready(function() {
    $('#alarm_id').val(alarm.id);
    $('#div_alarm_id').css('display', 'block');
    $('#alarm_name_cn').val(alarm.name_cn);
    $('#alarm_name_cn').attr('disabled', 'true');
    $('#alarm_name_en').val(alarm.name_en);
    $('#alarm_name_en').attr('disabled', 'true');
    $('#alarm_desc').summernote('reset');
    $('#alarm_desc').summernote('code', alarm.desc);
    $("#select_alarm_method option[value='"+alarm.method+"']").attr("selected","");
    $("#select_alarm_method").trigger("chosen:updated");
});
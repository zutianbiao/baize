function save_alarm_person() {
    var name = $('#alarm_person_name').val();
    var phone = $('#alarm_person_phone').val();
    var email = $('#alarm_person_email').val();
    $.ajax({
        type : 'POST',
        url: "/web/alarm_manage/alarm_person/save",
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        data: {
            "name": name,
            "phone": phone,
            'email': email
        },
        success : function(result){
            if(result.success){
                $('#alarm_person_id').val(result.data.id);
                $('#div_alarm_person_id').css('display', 'block');
                parent.parent.printMsg(result.msg,'Success');
            }else{
                parent.parent.printMsg(result.msg,'error');
            }
        }
    });
}
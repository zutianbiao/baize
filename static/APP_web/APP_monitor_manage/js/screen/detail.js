function sleep(n) { //n表示的毫秒数
    var start = new Date().getTime();
    while (true) if (new Date().getTime() - start > n) break;
}
$(document).ready(function() {
    $('#screen_id').val(screen.id);
    $('#div_screen_id').css('display', 'block');
    $('#screen_name_cn').val(screen.name_cn);
    $('#screen_name_en').val(screen.name_en);
    $("#select_tag option[value='"+screen.tag_id+"']").attr("selected","");
    $("#select_tag").trigger("chosen:updated");
    $('#screen_name_cn').attr('disabled', 'true');
    $('#screen_name_en').attr('disabled', 'true');
    update_select_asset();
});
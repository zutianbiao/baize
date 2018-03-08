$(document).ready(function() {
    $('#item_name_cn').val(item.name_cn);
    $('#item_name_en').val(item.name_en);
    $('#item_id').val(item.id);
    $("#select_test_tag option[value='"+item.test_tag+"']").attr("selected","");
    $("#select_test_tag").trigger("chosen:updated");
    $("#select_online_tag option[value='"+item.online_tag+"']").attr("selected","");
    $("#select_online_tag").trigger("chosen:updated");
    $('#div_item_id').css('display', 'block');
});
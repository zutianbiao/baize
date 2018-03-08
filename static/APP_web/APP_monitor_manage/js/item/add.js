function save_item() {
    var name_cn = $('#item_name_cn').val();
    var name_en = $('#item_name_en').val();
    var test_tag = $('#select_test_tag option:selected').val();
    var online_tag = $('#select_online_tag option:selected').val();
    $.ajaxFileUpload({
        type : 'POST',
        url: "/web/monitor_manage/item/save",
        dataType: 'json',
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        fileElementId: 'item_script',
        data: {
            "name_cn": name_cn,
            "name_en": name_en,
            "test_tag": test_tag,
            'online_tag': online_tag
        },
        success : function(result){
            if(result.success){
                $('#item_id').val(result.data.id);
                $('#div_item_id').css('display', 'block');
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
});

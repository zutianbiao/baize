Array.prototype.remove = function(val){
    var index = this.indexOf(val);
    if (index > -1) {
        this.splice(index, 1);
    }
};
function delete_tag_for_asset(e, asset_id, tag_name){
    $.ajax({
           type : 'POST',
           url: "/web/asset_manage/tag/unbind",
           headers: {
               Accept: "application/json; charset=utf-8"
           },
           data: {
               "asset_id": asset_id,
               "tag_name": tag_name
           },
           success : function(result){
               if(result.success){
                   $(e).parent().next().remove()
                   $(e).parent().remove();
                   printMsg(result.msg,'Success');
               }else{
                   printMsg(result.msg,'error');
               }
           }
    });
}

function save_tree(jstree, tag) {
    var inst = $.jstree.reference(jstree);
    var tree_data = inst.get_json();
    $.ajax({
           type : 'POST',
           url: "/web/asset_manage/tree/save",
           headers: {
               Accept: "application/json; charset=utf-8"
           },
           data: {
               "json_tree": JSON.stringify(tree_data),
           },
           success : function(result){
               if(result.success){
                   $('#jstree1').jstree().destroy();
                   var jstree1 = $('#jstree1').jstree({
                       'core': {
                           'check_callback': true,
                           'data': result.data
                       },
                       'plugins': ['types', 'dnd', 'json_data'],
                       'types': {
                           'default': {
                               'icon': 'fa fa-folder'
                           },
                           'html': {
                               'icon': 'fa fa-file-code-o'
                           },
                           'svg': {
                               'icon': 'fa fa-file-picture-o'
                           },
                           'css': {
                               'icon': 'fa fa-file-code-o'
                           },
                           'img': {
                               'icon': 'fa fa-file-image-o'
                           },
                           'js': {
                               'icon': 'fa fa-file-text-o'
                           }
                       }
                   });
                   jstree1.bind('dblclick.jstree',function(event){
                       var tag = $(event.target).attr('tag');
                       if(tag){
                           query_asset(tag);
                       }
                       console.log(tag);
                   });
                   if(tag!=false){
                       printMsg(result.msg,'Success');
                   }
               }else{
                   printMsg(result.msg,'error');
               }
           }
        });
}
function query_asset(tag) {
    $.ajax({
            type : 'POST',
            url: "/web/asset_manage/tag/query_asset",
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            data: {
                "tag_name": tag
            },
            success : function(data){
                if(data.success){
                    table.clear();
                    var table_data = new Array();
                    var table_row = new Array();
                    for(var i in data['data']){
                        if(i!='remove'){
                            table_row[0] = '<input asset_id='+data['data'][i]['id']+' type="checkbox" class="i-checks checkchild" name="input[]" />';
                            table_row[1] = data['data'][i]['hostname'];
                            var data_tag_list="";
                            for(var tag in data['data'][i]['tag_list']){
                                if(tag!='remove'){
                                    data_tag_list=data_tag_list+'<span>'+data['data'][i]['tag_list'][tag]+' <a class="green fa fa-times" onclick="delete_tag_for_asset(this,'+data['data'][i]['id']+', \''+data['data'][i]['tag_list'][tag]+'\');"></a></span></br>'
                                }

                            }
                            table_row[2] = data_tag_list;
                            table_row[3] = data['data'][i]['all_ipv4_addresses'].join('<br>');
                            table_row[4] = '<button type="button" class="btn btn-primary btn-xs"  onclick="show_detail('+data['data'][i]['id']+')">详情</button>';
                            table_data.push(table_row);
                            table_row = new Array();
                        }
                    }
                    table.rows.add(table_data).draw();
                    jQuery.getScript("/static/APP_web/APP_asset_manage/js/index_2.js");
                    printMsg(data.msg,'Success');
                }else{
                    printMsg(data.msg,'error');
                }
            }
        });
}
$(document).ready(function() {
    window.check_asset_id = new Array();
    printMsg('数据加载成功！','Success');
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
    });
    $('.check-column').on( 'ifChecked', function () {
        var column = table.column( $(this).attr('data-column') );
        column.visible( true );
    });
    $('.check-column').on( 'ifUnchecked', function () {
        var column = table.column( $(this).attr('data-column') );
        column.visible( false );
    });

    $('.checkall').on('ifChecked', function(event) {
        table.page.len( -1 ).draw();
        $('.checkchild').iCheck('check');
    });
    $('.checkchild').on('ifChecked', function(event) {
        check_asset_id.push($(this).attr('asset_id'));
    });
    $('.checkall').on('ifUnchecked', function(event) {
        table.page.len( -1 ).draw();
        $('.checkchild').iCheck('uncheck');
        table.page.len( 10 ).draw();
    });
    $('.checkchild').on('ifUnchecked', function(event) {
        check_asset_id.remove($(this).attr('asset_id'));
    });
    $('.checkall').iCheck('uncheck');

    $('.tag-list-option').click(function(){
        $('.tag-list >li>a.active').removeClass("active");
        $(this).attr("class","tag-list-option active");
    });
    window.table = $('#editable').DataTable({
        dom: '<"html5buttons"B>lrtip',
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
        },
        {
            text: 'AddToTree',
            action: function ( e, dt, node, config ) {
                var inst = $.jstree.reference($('#jstree1'));
                var clickedNode = inst.get_selected(true);
                var timestamp = new Date().getTime();
                clickedNode[0].a_attr['tag'] = clickedNode[0].text + '-'+ timestamp;
                save_tree($('#jstree1'),false);
                console.log(check_asset_id);
                $.ajax({
                    type : 'POST',
                    url: "/web/asset_manage/tree/bind",
                    headers: {
                        Accept: "application/json; charset=utf-8"
                    },
                    data: {
                        "node": clickedNode[0].a_attr['tag'],
                        "asset": JSON.stringify(check_asset_id)
                    },
                    success : function(data){
                        if(data.success){
                            printMsg(data.msg,'Success');
                        }else{
                            printMsg(data.msg,'error');
                        }
                    }
                });
            }
        },
        {
            text: 'BindToTag',
            action: function ( e, dt, node, config ) {
                var tag_id = $('.tag-list >li>a.active').attr('tag_id');
                console.log(check_asset_id);
                $.ajax({
                    type : 'POST',
                    url: "/web/asset_manage/tag/bind",
                    headers: {
                        Accept: "application/json; charset=utf-8"
                    },
                    data: {
                        "tag_id": tag_id,
                        "asset": JSON.stringify(check_asset_id)
                    },
                    success : function(data){
                        if(data.success){
                            printMsg(data.msg,'Success');
                        }else{
                            printMsg(data.msg,'error');
                        }
                    }
                });
            }
        }
        ],
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
        "searching": true
    });
    $("#btn_asset_search").click(function() {
        table.page.len( -1 ).draw();
        $('.checkchild').iCheck('uncheck');
        var value = $("#input_asset_search").val();
        table.search(value).draw();
    });
    $("#input_asset_search").keydown(function() {
        if(event.keyCode == "13") {
            table.page.len( -1 ).draw();
            $('.checkchild').iCheck('uncheck');
            var value = $("#input_asset_search").val();
            table.search(value).draw();
        }
    });
    $.ajax({
       type : 'POST',
       url: "/web/asset_manage/tree/query",
       headers: {
           Accept: "application/json; charset=utf-8"
       },
       dataType: "json",
       data: {
           "name": "已分配资源池",
       },
       success : function(result){
           if(result.success){
               var tree_data = result.data;

               var jstree1 = $('#jstree1').jstree({
                   'core': {
                       'check_callback': true,
                       'data': tree_data
                   },
                   'plugins': ['types', 'dnd'],
                   'types': {
                       'default': {
                           'icon': 'fa fa-folder'
                       },
                       'html': {
                           'icon': 'fa fa-file-code-o'
                       },
                       'svg': {
                           'icon': 'fa fa-file-picture-o'
                       },
                       'css': {
                           'icon': 'fa fa-file-code-o'
                       },
                       'img': {
                           'icon': 'fa fa-file-image-o'
                       },
                       'js': {
                           'icon': 'fa fa-file-text-o'
                       }
                   }
               });
               jstree1.bind('dblclick.jstree',function(event){
                   var tag = $(event.target).attr('tag');
                   if(tag){
                       query_asset(tag);
                   }
                   console.log(tag);
               });
               // printMsg(result.msg,'Success');
           }else{
               tree_data = [
                   {
                       "id": "j1_1",
                       "text": "已分配资源池",
                       "icon": "fa fa-folder",
                       "li_attr": {
                           "id": false,
                           "class": "jstree"
                       },
                       "a_attr": {
                           "href": "#",
                           "id": "j1_1_anchor"
                       },
                       "state": {
                           "loaded": true,
                           "opened": false,
                           "selected": false,
                           "disabled": false
                       },
                       "data": {},
                       "children": [],
                       "type": "default"
                   }
               ];
               var jstree1 = $('#jstree1').jstree({
                   'core': {
                       'check_callback': true,
                       'data': tree_data
                   },
                   'plugins': ['types', 'dnd'],
                   'types': {
                       'default': {
                           'icon': 'fa fa-folder'
                       },
                       'html': {
                           'icon': 'fa fa-file-code-o'
                       },
                       'svg': {
                           'icon': 'fa fa-file-picture-o'
                       },
                       'css': {
                           'icon': 'fa fa-file-code-o'
                       },
                       'img': {
                           'icon': 'fa fa-file-image-o'
                       },
                       'js': {
                           'icon': 'fa fa-file-text-o'
                       }
                   }
               });
               jstree1.bind('dblclick.jstree',function(event){
                   var tag = $(event.target).attr('tag');
                   if(tag){
                       query_asset(tag);
                   }
                   console.log(tag);
               });
               printMsg(result.msg,'error');
           }
       }
    });
    var tree_data2 = [
            {
                "id": "j1_1",
                "text": "空闲资源池",
                "icon": "fa fa-folder",
                "li_attr": {
                    "id": false,
                    "class": "jstree"
                },
                "a_attr": {
                    "href": "#",
                    "id": "j1_1_anchor",
                    "tag": "空闲资源池"
                },
                "state": {
                    "loaded": true,
                    "opened": false,
                    "selected": false,
                    "disabled": false
                },
                "data": {},
                "children": [],
                "type": "default"
            }
        ];
    window.jstree2 = $('#jstree2').jstree({
        'core': {
            'check_callback': true,
            'data': tree_data2

        },
        'plugins': ['types', 'dnd'],
        'types': {
            'default': {
                'icon': 'fa fa-folder'
            },
            'html': {
                'icon': 'fa fa-file-code-o'
            },
            'svg': {
                'icon': 'fa fa-file-picture-o'
            },
            'css': {
                'icon': 'fa fa-file-code-o'
            },
            'img': {
                'icon': 'fa fa-file-image-o'
            },
            'js': {
                'icon': 'fa fa-file-text-o'
            }

        }
    });
    window.jstree2.bind('dblclick.jstree',function(event){
        var tag = $(event.target).attr('tag');
        if(tag){
            query_asset(tag);
        }
        console.log(tag);
    });
    var config = {
        '.chosen-select': {
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

    $('.tag-list-option').dblclick(function(){
        var tag_id = $(this).attr("tag_id");
        $.ajax({
            type : 'POST',
            url: "/web/asset_manage/tag/query_asset",
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            data: {
                "tag_id": tag_id
            },
            success : function(data){
                if(data.success){
                    table.clear();
                    var table_data = new Array();
                    var table_row = new Array();
                    for(var i in data['data']){
                        if(i!='remove'){
                            table_row[0] = '<input asset_id='+data['data'][i]['id']+' type="checkbox" class="i-checks checkchild" name="input[]" />';
                            table_row[1] = data['data'][i]['hostname'];
                            var data_tag_list="";
                            for(var tag in data['data'][i]['tag_list']){
                                if(tag!='remove'){
                                    data_tag_list=data_tag_list+'<span>'+data['data'][i]['tag_list'][tag]+' <a class="green fa fa-times" onclick="delete_tag_for_asset(this,'+data['data'][i]['id']+', \''+data['data'][i]['tag_list'][tag]+'\');"></a></span></br>'
                                }

                            }
                            table_row[2] = data_tag_list;
                            table_row[3] = data['data'][i]['all_ipv4_addresses'].join('<br>');
                            table_row[4] = '<button type="button" class="btn btn-primary btn-xs"  onclick="show_detail('+data['data'][i]['id']+')">详情</button>';
                            table_data.push(table_row);
                            table_row = new Array();
                        }
                    }
                    table.rows.add(table_data).draw();
                    jQuery.getScript("/static/APP_web/APP_asset_manage/js/index_2.js");
                    printMsg(data.msg,'Success');
                }else{
                    printMsg(data.msg,'error');
                }
            }
        });
    });

    $('#btn_add_tag_save').click(function(){
        var tag_name=$('#tag_name').val();
        $.ajax({
            type : 'POST',
            url: "/web/asset_manage/tag/add",
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            data: {
                "tag_name": tag_name
            },
            success : function(data){
                if(data.success){
                    printMsg(data.msg,'Success');
                }else{
                    printMsg(data.msg,'error');
                }
            }
            });
    });
    $('#btn_query_tag').click(function(){
        var tag_pattern=$('#tag_pattern').val();
        if(tag_pattern.length != 0){
            $.ajax({
            type : 'POST',
            url: "/web/asset_manage/tag/query",
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            data: {
                "tag_pattern": tag_pattern
            },
            success : function(data){
                if(data.success){
                    $('#ul_tag_list li').remove();
                    for(li in data.data){
                        if(data.data[li].name.length != 0) {
                            $('#ul_tag_list').append("<li><a class='tag-list-option' tag_id='"+ data.data[li].id +"'>" + data.data[li].name + "</a></li>");
                        }
                    }
                    $('.tag-list-option').click(function(){
                        $('.tag-list >li>a.active').removeClass("active");
                        $(this).attr("class","tag-list-option active");
                    });
                    $('.tag-list-option').dblclick(function(){
                        var tag_id = $(this).attr("tag_id");
                        $.ajax({
                            type : 'POST',
                            url: "/web/asset_manage/tag/query_asset",
                            headers: {
                                Accept: "application/json; charset=utf-8"
                            },
                            data: {
                                "tag_id": tag_id
                            },
                            success : function(data){
                                if(data.success){
                                    table.clear();
                                    var table_data = new Array();
                                    var table_row = new Array();
                                    for(var i in data['data']){
                                        if(i!='remove'){
                                            table_row[0] = '<input asset_id='+data['data'][i]['id']+' type="checkbox" class="i-checks checkchild" name="input[]" />';
                                            table_row[1] = data['data'][i]['hostname'];
                                            var data_tag_list="";
                                            for(var tag in data['data'][i]['tag_list']){
                                                if(tag!='remove'){
                                                    data_tag_list=data_tag_list+'<span>'+data['data'][i]['tag_list'][tag]+' <a class="green fa fa-times" onclick="delete_tag_for_asset(this,'+data['data'][i]['id']+', \''+data['data'][i]['tag_list'][tag]+'\');"></a></span></br>'
                                                }

                                            }
                                            table_row[2] = data_tag_list;
                                            table_row[3] = data['data'][i]['all_ipv4_addresses'].join('<br>');
                                            table_row[4] = '<button type="button" class="btn btn-primary btn-xs"  onclick="show_detail('+data['data'][i]['id']+')">详情</button>';
                                            table_data.push(table_row);
                                            table_row = new Array();
                                        }
                                    }
                                    table.rows.add(table_data).draw();
                                    jQuery.getScript("/static/APP_web/APP_asset_manage/js/index_2.js");
                                    printMsg(data.msg,'Success');
                                }else{
                                    printMsg(data.msg,'error');
                                }
                            }
                        });
                    });
                    printMsg(data.msg,'Success');
                }else{
                    printMsg(data.msg,'error');
                }
            }
            });
        }
    });
    $('#tag_pattern').bind('keydown',function(event){
        if(event.keyCode == "13"){
            var tag_pattern=$('#tag_pattern').val();
            if(tag_pattern.length != 0){
                $.ajax({
                type : 'POST',
                url: "/web/asset_manage/tag/query",
                headers: {
                    Accept: "application/json; charset=utf-8"
                },
                data: {
                    "tag_pattern": tag_pattern
                },
                success : function(data){
                    if(data.success){
                        $('#ul_tag_list li').remove();
                        for(li in data.data){
                            if(data.data[li].name.length != 0){
                                $('#ul_tag_list').append("<li><a class='tag-list-option' tag_id='"+ data.data[li].id +"'>" + data.data[li].name + "</a></li>");
                            }
                        }
                        $('.tag-list-option').click(function(){
                            $('.tag-list >li>a.active').removeClass("active");
                            $(this).attr("class","tag-list-option active");
                        });
                        $('.tag-list-option').dblclick(function(){
                            var tag_id = $(this).attr("tag_id");
                            $.ajax({
                                type : 'POST',
                                url: "/web/asset_manage/tag/query_asset",
                                headers: {
                                    Accept: "application/json; charset=utf-8"
                                },
                                data: {
                                    "tag_id": tag_id
                                },
                                success : function(data){
                                    if(data.success){
                                        table.clear();
                                        var table_data = new Array();
                                        var table_row = new Array();
                                        for(var i in data['data']){
                                            if(i!='remove'){
                                                table_row[0] = '<input asset_id='+data['data'][i]['id']+' type="checkbox" class="i-checks checkchild" name="input[]" />';
                                                table_row[1] = data['data'][i]['hostname'];
                                                var data_tag_list="";
                                                for(var tag in data['data'][i]['tag_list']){
                                                    if(tag!='remove'){
                                                        data_tag_list=data_tag_list+'<span>'+data['data'][i]['tag_list'][tag]+' <a class="green fa fa-times" onclick="delete_tag_for_asset(this,'+data['data'][i]['id']+', \''+data['data'][i]['tag_list'][tag]+'\');"></a></span></br>'
                                                    }

                                                }
                                                table_row[2] = data_tag_list;
                                                table_row[3] = data['data'][i]['all_ipv4_addresses'].join('<br>');
                                                table_row[4] = '<button type="button" class="btn btn-primary btn-xs"  onclick="show_detail('+data['data'][i]['id']+')">详情</button>';
                                                table_data.push(table_row);
                                                table_row = new Array();
                                            }
                                        }
                                        table.rows.add(table_data).draw();
                                        jQuery.getScript("/static/APP_web/APP_asset_manage/js/index_2.js");
                                        printMsg(data.msg,'Success');
                                    }else{
                                        printMsg(data.msg,'error');
                                    }
                                }
                            });
                        });
                        printMsg(data.msg,'Success');
                    }else{
                        printMsg(data.msg,'error');
                    }
                }
            });
            }
        }
    });
    $('#btn_del_tag').click(function(){
        var tag_name=$('#tag_name').val();
        $.ajax({
            type : 'POST',
            url: "/web/asset_manage/tag/del",
            headers: {
                Accept: "application/json; charset=utf-8"
            },
            data: {
                "tag_name": tag_name
            },
            success : function(data){
                if(data.success){
                    printMsg(data.msg,'Success');
                }else{
                    printMsg(data.msg,'error');
                }
            }
            });
    });
});
function change_tree1(tag){
    if(tag){
        var inst = $.jstree.reference($('#jstree1'));
        var tree_data = inst.get_json();
        $('#jstree1').jstree().destroy();
        $('#jstree1').jstree({
            'core': {
                'check_callback': true,
                'data': tree_data
            },
            'plugins': ["contextmenu", "dnd", "types", "json_data"],
            "contextmenu": {
                "items": {
                    "create": null,
                    "rename": {
                        "label": "重命名",
                        "action": function (obj) {
                            var inst = $.jstree.reference($('#jstree1'));
                            var clickedNode = inst.get_node(obj.reference);
                            inst.edit(clickedNode,clickedNode.val);
                        }
                    },
                    "remove": null,
                    "copy": {
                        "label": "复制",
                        "action": function (obj) {
                            var inst = $.jstree.reference($('#jstree1'));
                            inst.copy(obj.reference);
                        }
                    },
                    "paste": {
                        "label": "粘贴",
                        "action": function (obj) {
                            var inst = $.jstree.reference($('#jstree1'));
                            inst.paste(obj.reference);
                        }
                    },
                    "add": {
                        "label": "新增",
                        "action": function (obj) {
                            var inst = $.jstree.reference($('#jstree1'));
                            var clickedNode = inst.get_node(obj.reference);
                            var newNode = inst.create_node(clickedNode,'请输入分类名称',"first","","");
                            inst.edit(newNode,newNode.val);
                        }
                    },
                    "delete": {
                        "label": "删除",
                        "action": function (obj) {
                            var inst = $.jstree.reference($('#jstree1'));
                            inst.delete_node(obj.reference);
                        }
                    }
                }
            },
            'types': {
                'default': {
                    'icon': 'fa fa-folder'
                },
                'html': {
                    'icon': 'fa fa-file-code-o'
                },
                'svg': {
                    'icon': 'fa fa-file-picture-o'
                },
                'css': {
                    'icon': 'fa fa-file-code-o'
                },
                'img': {
                    'icon': 'fa fa-file-image-o'
                },
                'js': {
                    'icon': 'fa fa-file-text-o'
                }

            }
        });
        $('#btn_change_tree1').text('保存');
        $('#btn_change_tree1').attr('onclick', 'change_tree1(false)');
        console.log('保存');
    }else{
        save_tree($('#jstree1'));
        $('#btn_change_tree1').text('修改');
        $('#btn_change_tree1').attr('onclick', 'change_tree1(true)');
        console.log('修改');
    }

}
function show_detail(id) {
    $.ajax({
    type : 'POST',
    url: "/web/asset_manage/show_detail",
    headers: {
        Accept: "application/json; charset=utf-8"
    },
    data: {
        "asset_id": id,
    },
    success : function(data){
        if(data){
            $('#asset_detail').html(data);
            $('#myModal'+id).modal('show');
            printMsg('查询资产详情成功','Success');
        }else{
            printMsg('查询资产详情失败','error');
        }
    }
    });
}
function add_tag(tag) {
    if (tag == true){
        $('#div_add_tag').css('display', '');
        $('#btn_add_tag').text('关闭');
        $('#btn_add_tag').attr('onclick', 'add_tag(false)');
    }else{
        $('#div_add_tag').css('display', 'none');
        $('#btn_add_tag').text('新建');
        $('#btn_add_tag').attr('onclick', 'add_tag(true)');
    }
}




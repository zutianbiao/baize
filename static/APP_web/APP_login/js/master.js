$(document).ready(function () {
    $("#form").steps({
        bodyTag: "fieldset",
        labels: {
            cancel: "取消",
            finish: "完成",
            next: "下一步",
            previous: "上一步",
            loading: "Loading ..."
            },
        onStepChanging: function (event, currentIndex, newIndex) {
            // Always allow going backward even if the current step contains invalid fields!
            if (currentIndex > newIndex) {
                return true;
            }
            // Forbid suppressing "Warning" step if the user is to young
            if (newIndex === 3 && Number($("#age").val()) < 18) {
                return false;
            }
            var form = $(this);
            // Clean up if user went backward before
            if (currentIndex < newIndex) {
                // To remove error styles
                $(".body:eq(" + newIndex + ") label.error", form).remove();
                $(".body:eq(" + newIndex + ") .error", form).removeClass("error");
            }
            // Disable validation on fields that are disabled or hidden.
            form.validate().settings.ignore = ":disabled,:hidden";
            // Start validation; Prevent going forward if false
            return form.valid();
        },
        onStepChanged: function (event, currentIndex, priorIndex) {
            // Suppress (skip) "Warning" step if the user is old enough.
            if (currentIndex === 2 && Number($("#age").val()) >= 18) {
                $(this).steps("next");
            }
            // Suppress (skip) "Warning" step if the user is old enough and wants to the previous step.
            if (currentIndex === 2 && priorIndex === 3) {
                $(this).steps("previous");
            }
        },
        onFinishing: function (event, currentIndex) {
            if (currentIndex === 0) {
                return true
            }else{
                var form = $(this);
                // Disable validation on fields that are disabled.
                // At this point it's recommended to do an overall check (mean ignoring only disabled fields)
                form.validate().settings.ignore = ":disabled";
                // Start validation; Prevent form submission if false
                return form.valid();
            }

        },
        onFinished: function (event, currentIndex) {
            window.location.href = '/web/index';
        }
    }).validate({
        errorPlacement: function (error, element) {
                element.before(error);
            },
            rules: {
                confirm: {
                    equalTo: "#password"
                }
            }
    });
    function refresh_log(jobid,id){
        $.ajax({
            type : 'POST',
            url: "/web/init/job/?action=check",
            data: {
                "id": id,
                "jobid": jobid
            },
            success : function(result){
                if(result.status >= 2){
                    $(".log-box").append(result.data);
                    $(".log-box").scrollTop($(".log-box")[0].scrollHeight);
                }else{
                    $(".log-box").append(result.data);
                    $(".log-box").scrollTop($(".log-box")[0].scrollHeight);
                    sleep(1000);
                    refresh_log(jobid,result.id);
                }

            }
        });
    }
    function refresh_log3(jobid,id){
        $.ajax({
            type : 'POST',
            url: "/web/init/job/?action=check",
            data: {
                "id": id,
                "jobid": jobid
            },
            success : function(result){
                if(result.status >= 2){
                    $(".log-box3").append(result.data);
                    $(".log-box3").scrollTop($(".log-box3")[0].scrollHeight);
                }else{
                    $(".log-box3").append(result.data);
                    $(".log-box3").scrollTop($(".log-box3")[0].scrollHeight);
                    sleep(1000);
                    refresh_log3(jobid,result.id);
                }

            }
        });
    }
    $('#btn_begin_init').click(function(){
        $(".log-box").empty();
        $(".log-box").append('<p style="margin: 0 0 10px;">&emsp;整个安装过程大约需要10分钟请耐心等待.....</p>');
        $('#check_log').click();
        var ip = $("#ip_init").val();
        var password = $("#master_password_ssh").val();
        $.ajax({
            type : 'POST',
            url: "/web/init/job/?action=add",
            data: {
                "ip": ip,
                "role": "master",
                "password": password
            },
            dataType : 'json',
            success : function(result){
                if(result.success){
                    $.ajax({
                        type : 'POST',
                        url: "/web/init/job/?action=begin",
                        data: {
                            "jobid": result.jobid
                        },
                        dataType : 'json',
                        success : function(result){
                            if(result.success){
                                printMsg('Master安装成功！', 'success');
                            }else{
                                printMsg('Master安装失败！', 'error');
                            }

                        }
                    });
                    sleep(1000);
                    refresh_log(result.jobid,0);
                }else{
                    printMsg('Master安装任务添加失败！', 'error');
                }
            }
        });
    });
    $('#check_log').click(function(){
        $('.log-box').removeClass('hide');
        $('#check_log').addClass('hide');
        $('#hide_log').removeClass('hide');
    });
    $('#hide_log').click(function(){
        $('.log-box').addClass('hide');
        $('#check_log').removeClass('hide');
        $('#hide_log').addClass('hide');
    });
    $('#proxy_check_log').click(function(){
        $('.log-box3').removeClass('hide');
        $('#proxy_check_log').addClass('hide');
        $('#proxy_hide_log').removeClass('hide');
    });
    $('#proxy_hide_log').click(function(){
        $('.log-box3').addClass('hide');
        $('#proxy_check_log').removeClass('hide');
        $('#proxy_hide_log').addClass('hide');
    });
    $('#btn_test').click(function(){
        var ip = $("#ip_init").val();
        var timestamp = new Date().getTime();
        $.ajax({
            type : 'POST',
            url: "/web/master/check_active/",
            data: {
                "master_ip": ip
            },
            dataType : 'json',
            success: function(result){
                if (result.success) {
                    printMsg(result.msg, 'success');
                }else{
                    printMsg(result.msg, 'error');
                }
            }
        });
    });
    $('#btn_access_master').click(function(){
        var master_ip = $("#master_ip").val();
        var web_server_ip = $("#web_server_ip").val();
        var master_user = $("#master_user").val();
        var master_password = $("#master_password").val();
        $.ajax({
            type: 'POST',
            url: "/web/master/bind_ip/",
            data: {
                "master_ip": master_ip,
                "web_server_ip": web_server_ip,
                "master_user": master_user,
                "master_password": master_password
            },
            dataType : 'json',
            success: function(result){
                if (result.success) {
                    printMsg(result.msg, 'success');
                }else{
                    printMsg(result.msg, 'error');
                }
            }
        });
    });
    $('#btn_access_master_originally').click(function(){
        var master_ip = $("#master_ip_originally").val();
        var web_server_ip = $("#web_server_ip_originally").val();
        var master_user = $("#master_user_originally").val();
        var master_password = $("#master_password_originally").val();
        $.ajax({
            type: 'POST',
            url: "/web/master/bind_ip/",
            data: {
                "master_ip": master_ip,
                "web_server_ip": web_server_ip,
                "master_user": master_user,
                "master_password": master_password
            },
            dataType : 'json',
            success: function(result){
                if (result.success) {
                    printMsg(result.msg, 'success');
                }else{
                    printMsg(result.msg, 'error');
                }
            }
        });
    });
    $('#btn_proxy_begin_init').click(function(){
        $(".log-box3").empty();
        $(".log-box3").append('<p style="margin: 0 0 10px;">&emsp;整个安装过程大约需要10分钟请耐心等待.....</p>');
        $('#proxy_check_log').click();
        var ip = $("#ip_proxy_init").val();
        var password = $("#proxy_password_ssh").val();
        $.ajax({
            type : 'POST',
            url: "/web/init/job/?action=add",
            data: {
                "ip": ip,
                "role": "proxy",
                "password": password
            },
            dataType : 'json',
            success : function(result){
                if(result.success){
                    $.ajax({
                        type : 'POST',
                        url: "/web/init/job/?action=begin",
                        data: {
                            "jobid": result.jobid
                        },
                        dataType : 'json',
                        success : function(result){
                            if(result.success){
                                printMsg('Proxy安装成功！', 'success');
                            }else{
                                printMsg('Proxy安装失败！', 'error');
                            }

                        }
                    });
                    sleep(1000);
                    refresh_log3(result.jobid,0);
                }else{
                    printMsg('Proxy安装任务添加失败！', 'error');
                }
            }
        });
    });
    $('#btn_proxy_test').click(function(){
        var ip = $("#ip_proxy_init").val();
        var timestamp = new Date().getTime();
        $.ajax({
            type : 'POST',
            url: "/web/master/check_active/",
            data: {
                "proxy_ip": ip
            },
            dataType : 'json',
            success: function(result){
                if (result.success) {
                    printMsg(result.msg, 'success');
                }else{
                    printMsg(result.msg, 'error');
                }
            }
        });
    });
    $('#btn_proxy_access').click(function(){
        var proxy_ip = $("#proxy_ip").val();
        var web_server_ip = $("#web_server_ip_proxy").val();
        var master_user = $("#user_proxy").val();
        var master_password = $("#master_password_ssh2").val();
        $.ajax({
            type: 'POST',
            url: "/web/master/bind_ip/",
            data: {
                "proxy_ip": proxy_ip,
                "web_server_ip": web_server_ip,
                "master_user": master_user,
                "master_password": master_password
            },
            dataType : 'json',
            success: function(result){
                if (result.success) {
                    printMsg(result.msg, 'success');
                }else{
                    printMsg(result.msg, 'error');
                }
            }
        });
    });
});
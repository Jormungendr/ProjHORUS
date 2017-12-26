function rest_url(url) {
    return 'http://127.0.0.1:8000' + url;
}

function xpPostReq(url, data, success, fail) {
    var payload = data;
    if(!payload){
        payload = {};
    }
    $.post(url, payload)
    .done(function(resp){
        if(success){
            success(resp);
        }
        else{
            if(!resp.success && resp.message){
                alert(resp.message);
            }
        }
    })
    .fail(function(){
        if(fail){
            fail();
        }
        else{
            alert('通信失败。请稍后再试。');
        }
    });
}

function xpGetReq(url, success, fail) {
    $.get(url)
    .done(function(resp){
        if(success){
            success(resp);
        }
        else{
            if(!resp.success && resp.message){
                alert(resp.message);
            }
        }
    })
    .fail(function(resp, txt){
        if(fail){
            fail(resp, txt);
        }
        else{
            alert('通信失败。请稍后重试。');
        }
    });
}

function xpCheckTask(task_db_id, task_id, offset, consoleId) {
    xpGetReq('/api/task/check/'+task_db_id+'/'+task_id+'/'+offset,
        function(resp){
            if(resp.success){
                if(resp.logs.length > 0){
                    $('#iConsole_'+consoleId+' .cContent').append(resp.logs.join('<br>')+'<br>');
                }
                if(!resp.finish){
                    setTimeout( function(){
                                    xpCheckTask(task_db_id, task_id, resp.offset, consoleId);
                                },
                                2000);
                }
                else{
                    $('#iConsole_'+consoleId+' .cContent').append($('<button onclick="xpHideTaskConsole(\'iConsole_'+consoleId+'\');">关闭</button>'));
                }
                $('#iConsole_'+consoleId).scrollTop($('#iConsole_'+consoleId)[0].scrollHeight);
            }
            else{
                alert(resp.message);
            }
        }
        ,null);
}

function xpCheckManyTask(task_db_id, task_id, offset, consoleId) {
    xpGetReq('/api/task/check/'+task_db_id+'/'+task_id+'/'+offset,
        function(resp){
            if(resp.success){
                if(resp.logs.length > 0){
                    $('#iConsole_'+consoleId+' .cContent').append(resp.logs.join('<br>')+'<br>');
                }
                if(!resp.finish){
                    setTimeout( function(){
                                    xpCheckManyTask(task_db_id, task_id, resp.offset, consoleId);
                                },
                                2000);
                }
                else{
                    $('#iConsole_'+consoleId+' .cContent').append('"################"<br>');
                }
            }
            else{
                alert(resp.message);
            }
        }
        ,null);
}

function xpInitTaskConsole(task_db_id, task_id) {
    var consoleId = Date.now();
    var console = $('<div id="iConsole_'+consoleId+'" style="position:absolute;overflow-x:hidden;z-index:65535;padding:10px;top:0;right:0;bottom:0;background:#dddddd"></div>');
    console.css('width', parseInt($('body').css('width')) / 2);
    var closeBtn = $('<button onclick="xpHideTaskConsole(\'iConsole_'+consoleId+'\');">关闭</button>');
    console.append(closeBtn);
    console.append('<div class="cContent" style="margin-top:10px"></div>');
    $('body').append(console);
    xpCheckTask(task_db_id, task_id, 0, consoleId);
}

function xpInitManyTaskConsole(task_db_id, task_id) {
    var consoleId = Date.now();
    var console = $("#iConsole_"+consoleId);
    if(console.length > 0){
    }
    else{
        var new_console = $('<div id="iConsole_'+consoleId+'" style="position:absolute;overflow-x:hidden;z-index:65535;padding:10px;top:0;right:0;bottom:0;background:#dddddd"></div>');
        new_console.css('width', parseInt($('body').css('width')) / 2);
        var closeBtn = $('<button onclick="xpHideTaskConsole(\'iConsole_'+consoleId+'\');">关闭</button>');
        new_console.append(closeBtn);
        new_console.append('<div class="cContent" style="margin-top:10px"></div>');
        $('body').append(new_console);
    }
    xpCheckManyTask(task_db_id, task_id, 0, consoleId);
}

function xpHideTaskConsole(console_id) {
    var console = $('#'+console_id);
    console.hide();
//    console.css('right', 0-10-parseInt(console.css('width')));
}

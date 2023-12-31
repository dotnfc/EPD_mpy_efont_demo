/**
 * eforecast backend script
 */
function isEmpty(obj) {
    if (typeof obj == "undefined" || obj == null || obj == "") {
        return true;
    } else {
        return false;
    }
}

function sleep(delay) {
    let endTime = new Date().getTime() + parseInt(delay);
    while (new Date().getTime() < endTime);
}

//----------------------------------------------------------------
// toggle password visibility
$('#password + .glyphicon').on('click', function () {
    $(this).toggleClass('glyphicon-eye-close').toggleClass('glyphicon-eye-open');
    $('#password').togglePassword(); // activate the hideShowPassword plugin
});

//----------------------------------------------------------------
// 左右滑动事件处理
var myElement = document.getElementById('gestureZone');

var mc = new Hammer(myElement); // document.body
mc.add(new Hammer.Swipe({ direction: Hammer.DIRECTION_HORIZONTAL }));
//console.log(document.body.style.touchAction)
var swipedir;
mc.on("panend panleft panright", function (ev) {

    if (ev.type == "panleft") {
        swipedir = 1;
    } else if (ev.type == "panright") {
        swipedir = 2;
    } else {
        console.log(" swipe " + swipedir);
        if (swipedir == 2) {
            if (tabIndex >= 1)
                tabIndex -= 1;
        }
        else {
            if (tabIndex <= 1)
                tabIndex += 1;
        }

        $('#pillNavTab li button').eq(tabIndex).click();
    }
});

function rssiToStrength(rssi) {
    var signalLevel;

    if (rssi <= -80) {
      signalLevel = 0;  // 信号非常弱
    } else if (rssi <= -70) {
      signalLevel = 1;  // 信号弱
    } else if (rssi <= -60) {
      signalLevel = 2;  // 信号中等
    } else {
      signalLevel = 3;  // 信号强
    }

    return signalLevel;
}

function jRequest(url, method, data, callback) {
    $.ajax({
        url: url,
        method: method, // "GET" "POST",
        data: data, // { key1: value1, key2: value2 }
        success: function(response) {
          // 请求成功
          callback(response);
        },
        error: function(xhr, status, error) {
          // 请求失败
          console.log("POST请求失败: " + status + ", " + error);
          showFailed("糟糕", "请求失败 " + error);
        }
    });
}

//----------------------------------------------------------------
// WIFI 列表点击事件
function scanWiFi() {
    
    //var jsonArray = '[{"ssid":"7Days","rssi":-60, "type":1}, {"ssid":"DOTNFC-HOS","rssi":-70, "type":1}, {"ssid":"DOTNFC-IP8","rssi":-30, "type":0}]';
    //var jsonObjects = JSON.parse(jsonArray);
    jRequest("/wifi/scan", "GET", "{msg:'hi'}", function(response) {
        var iid = 0;
        innerHtml = '';
        var jsonObjects = response;
        jsonObjects.forEach(function(item) {
            
            var signalStrength = rssiToStrength(item['rssi']);
            var itemHtml = `
            <div class="wifi-component list-wifi-item" id="${iid}" data-ssid="${item['ssid']}">
            <div class="wifi-icon">
                <span class="base-icon qi-ico-wifiscanbars"></span>
                <span class="top-icon qi-ico-wifiscan${signalStrength}"></span>
            </div>
            <span class="text">${item['ssid']}</span>
            </div>`

            iid ++;
            innerHtml += itemHtml;
        });

        $('#dlgWifiScanBody').html(innerHtml);

        // WIFI 列表点击事件
        $('.wifi-component').click(function () {
            // $(this).attr('id);
            var ssid = $(this).data("ssid");
            console.log('Clicked on:', ssid);
            $("#wifi-sta-ssid").val(ssid);
            $("#wifi-sta-passwd").val('');
            $('#dlgWifiScan').modal("hide");
        });

        $("#dlgWifiScan").modal({backdrop: 'static', keyboard: false});
        $('#dlgWifiScan').modal("show");

        $('#dlgWifiScan').on('hidden.bs.modal', function () {

        });
    });
}

//----------------------------------------------------------------
// 获取配置信息
var _settings;
function getSettings()
{
    jRequest("/settings", "GET", "{msg:'hi'}", function(response) {
        _settings = response;
        
        $("#wifi-sta-ssid").val(_settings['ssid']);
        $("#wifi-sta-passwd").val(_settings['passwd']);

        $("#weather-key").val(_settings['we_key']);
        $("#weather-city").val(_settings['we_city']);

        refreshDefaultPage(_settings['page_nbr'], _settings['page_list']);
        showSuccess('刷新成功！', '');
    });
}

//----------------------------------------------------------------
// 保存配置
function saveSettings()
{
    var ssid = $('#wifi-sta-ssid').val();
    var passwd =$('#wifi-sta-passwd').val();

    var we_key = $('#weather-key').val();
    var we_city =$('#weather-city').val();
    var page_nbr = getDefaultPage();

    var jsonData = { ssid, passwd, we_key, we_city, page_nbr };
    var jsonString = JSON.stringify(jsonData);

    jRequest("/settings", "POST", jsonString, function(response) {
        
        if (response["msg"] == "done")
            showSuccess('保存成功！', '');
        else
            showFailed("", response["msg"]);
    });
}

//----------------------------------------------------------------
// 获取设备信息
function getDeviceInfo() {
    jRequest("/dev/info", "GET", "{msg:'hi'}", function(response) {
        var innerHtml = '';
        for (var key in response) {
            var itemHtml = `
            <li class="list-group-item list-group-item-light">
              <span class="title">${key}:</span>
              <span class="info">${response[key]}</span>
            </li>`;
            innerHtml += itemHtml;
        };

        $('#devInfoList').html(innerHtml);
        showSuccess('刷新成功！', '');
    });
}

//----------------------------------------------------------------
// 初始化 Popover，显示 天气 api 的源信息
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
})

//----------------------------------------------------------------
// 获取默认页面
function getDefaultPage() {
    var pageId = $('#uipgList')
        .find('a.active')
        .first()
        .data('pid');

    if (pageId !== undefined) {
        console.log(pageId);
        return pageId;
    } else {
        console.log('No active items found.');
        return 0;
    }
}

function refreshDefaultPage(current, strPages) {
    var innerHtml="";
    var pages = JSON.parse(strPages);

    for (var page of pages) {
        var itemHtml = "";

        if (current == page['id']) {
            itemHtml = `<a href="#" class="list-group-item list-group-item-action active ${page['ico']}" data-pid="${page['id']}">&nbsp;${page['name']}</a>`;
        }
        else {
            itemHtml = `<a href="#" class="list-group-item list-group-item-action ${page['ico']}" data-pid="${page['id']}">&nbsp;${page['name']}</a>`;
        }
        
        innerHtml += itemHtml;
    };

    $('#uipgList').html(innerHtml);

    // 绑定单击事件
    $('.list-group-item').click(function() {

        $('#uipgList .list-group-item').each(function() {
            $(this).removeClass('active'); // 清楚选中
        });

        $(this).addClass('active'); // 添加选中
    });
}

//----------------------------------------------------------------
// 重启设备
function devReset()
{
    jRequest("/dev/reset", "POST", "{msg:'hi'}", function(response) {
        
        if (response["msg"] == "done")
            showSuccess('设备重启中，请稍后...', '');
        else
            showFailed("", response["msg"]);
    });
}

//----------------------------------------------------------------
// 城市查询，自动完成
function autocomplete(inp, arr_city) {
    /*自动填充函数有两个参数，input 输入框元素和自动填充的数组*/
    var currentFocus;

    /* 监听 input 输入框，当在 input 输入框元素中时执行以下函数*/
    inp.on("input", function (e) {
        
        $("#autocomplete-div").empty();

        if (!this.value) { return false; }
        currentFocus = -1;
        
        var searchKeyword = $(this).val().toLowerCase();
        var results = arr_city.filter(function(element) {
          return (
            element.code.toLowerCase().includes(searchKeyword) ||
            element.name_en.toLowerCase().includes(searchKeyword) ||
            element.name_cn.toLowerCase().includes(searchKeyword)
          );
        });

        results.forEach(function(result) {
            var strResult = result.prov + "_" + result.name_cn + "_" + result.code;
            var item = `<div data-code='${result.code}'>${strResult}</div>`;
            $("#autocomplete-div").append(item);
        });
    });
    
    $("#autocomplete-div").on("click", "div", function () {
        inp.val($(this).data('code'));
        $("#autocomplete-div").empty();
    });

    // 按下键盘上的一个键时执行函数
    inp.on("keydown", function (e) {
        var x = $("#autocomplete-div");
        if (x) x = x.find("div");
        if (e.keyCode == 40) {      // Down Arrow
            currentFocus++;
            addActive(x);
        } else if (e.keyCode == 38) { // UP arrow
            currentFocus--;
            addActive(x);
        } else if (e.keyCode == 13) { // Enter
            e.preventDefault();
            if (currentFocus > -1) {
                if (x) x[currentFocus].click();
            }
        }
    });

    // 设置选中的选项函数
    function addActive(x) {
        if (!x) return false;

        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }

    // 移除没有选中选项的 "autocomplete-active" 类
    function removeActive(x) {                
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    // 点击 HTML 文档任意位置关闭填充列表
    document.addEventListener("click", function (e) {
        $("#autocomplete-div").empty();
    });
}

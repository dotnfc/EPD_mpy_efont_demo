// SPDX-License-Identifier: MIT License
//

import 'dart:convert';

import 'package:eforecast/screens/search_city_screen.dart';
import 'package:eforecast/screens/wifi_list_screen.dart';
import 'package:eforecast/utils/ble_transmit.dart';
import 'package:eforecast/data/global_data.dart';
import 'package:eforecast/utils/qwicons.dart';
import 'package:eforecast/widgets/password_text_field.dart';
import 'package:flutter/material.dart';
import 'package:flutter_material_symbols/flutter_material_symbols.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../utils/snackbar.dart';

class DeviceConnectTile extends StatefulWidget {
  final BleTransmit bleTrx;
  const DeviceConnectTile({super.key, required this.bleTrx});

  @override
  State<DeviceConnectTile> createState() => _DeviceConnectTileState();
}

class _DeviceConnectTileState extends State<DeviceConnectTile> {
  bool _testing = false;
  late GlobalConfigProvider _prov;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {

    _prov = context.watch<GlobalConfigProvider>();

    // WiFi Connection
    TextEditingController ctrlTextSSID = TextEditingController(
      text: _prov.config.ssid,
    );
    TextEditingController ctrlTextPass = TextEditingController(
      text: _prov.config.passwd,
    );

    // Weather API
    TextEditingController ctrlTextQWKey = TextEditingController(
      text: _prov.config.weKey,
    );
    TextEditingController ctrlTextQWCity = TextEditingController(
      text: _prov.config.weCity,
    );

    return Consumer<GlobalConfigProvider>(builder: (context, value, child) { 
      return 
        Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(10),
            color: const Color.fromARGB(255, 242, 242, 242),
          ),
          
          child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(children: [
                TextField(
                  controller: ctrlTextSSID,
                  decoration: InputDecoration(
                    border: const UnderlineInputBorder(borderSide: BorderSide(width: 0.1)),
                    icon: const Icon(QWIcons.icoWifi3, color: Colors.green),
                    hintText: 'WiFi 热点',
                    labelText: '请输入热点名',
                    suffixIcon: IconButton(
                      icon: const Icon(Icons.chevron_right_outlined),
                      onPressed: () { devListWifi(context, widget.bleTrx); }
                    ),
                  ),
                  onChanged: (value) => { _prov.config.ssid = value }
                ),
                const SizedBox(height: 6),
                PasswordTextField(
                  controller: ctrlTextPass,
                  icon: const Icon(MaterialSymbols.lock, fill: 0, weight: 200, color: Colors.green),
                  hintText: 'WiFi 密码',
                  labelText: '热点访问密码',
                  onChanged: (value) => { _prov.config.passwd = value }
                ),
                const SizedBox(height: 6),
                TextField(
                  controller: ctrlTextQWKey,
                  decoration: InputDecoration(
                    border: const UnderlineInputBorder(borderSide: BorderSide(width: 0.1)),
                    icon: const Icon(QWIcons.icoLogoCarkey, color: Colors.orangeAccent),
                    hintText: 'API KEY',
                    labelText: '和风天气秘钥',
                    suffixIcon: IconButton(
                      icon: const Icon(QWIcons.icoInfocircle),
                      onPressed: () { qwApiKeyTip(context); }
                    ),
                  ),
                  onChanged: (value) => { _prov.config.weKey = value }
                ),
                const SizedBox(height: 6),
                TextField(
                  readOnly: true,
                  controller: ctrlTextQWCity,
                  decoration: InputDecoration(
                    border: const UnderlineInputBorder(borderSide: BorderSide(width: 0.1)),
                    icon: const Icon(QWIcons.icoGlobe2, color: Colors.orangeAccent),
                    hintText: '城市编码',
                    labelText: '指定城市',
                    suffixIcon: IconButton(
                      icon: const Icon(Icons.chevron_right_outlined),
                      onPressed: () { searchCity(context, ctrlTextQWCity.text); }
                    ),
                  ),
                  onChanged: (value) => { _prov.config.weCity = value }
                ),
                const SizedBox(height: 6),
                ListTile(
                  title: const Text("测试连接"),
                  contentPadding: const EdgeInsets.all(0),
                  visualDensity: const VisualDensity(vertical: -4),
                  leading: const Icon(Icons.checklist_outlined, color: Colors.blue),
                  trailing: PopupMenuButton<String>(
                    onSelected: (value) => debugPrint("selected $value"),
                    itemBuilder: (context) => <PopupMenuItem<String>>[
                      PopupMenuItem<String>(
                        value: "menuTestWiFi",
                        child: const Text("测试 WiFi 热点"),
                        onTap: () =>testWifiConnect(context),
                      ),
                      PopupMenuItem<String>(
                        value: "menuTestQW",
                        child: const Text("测试天气服务"),
                        onTap: () =>testQWService(context),
                      ),
                    ]
                  )
                ),
                _testing ? const LinearProgressIndicator(
                  valueColor: AlwaysStoppedAnimation<Color>(Colors.blue),
                ) : Container()
              ]
            )
          )
      );
    });
  }
  
  // 执行热点连接测试
  void testWifiConnect(BuildContext context) {
    if (mounted) {
      setState(() {
        _testing = true;
      });
    }

    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    var prov = _prov;
    if (prov.config.ssid.isEmpty || prov.config.passwd.isEmpty) {
      if (mounted) {
        ScaffoldMessenger.of(context).hideCurrentSnackBar();
        Snackbar.show(ABC.c, "请指定热点名和密码后再试", success: false);
        return;
      }
    }

    Map<String, dynamic> reqData = {
        'ssid': prov.config.ssid,
        'password': prov.config.passwd,
      };
      
    String jsString = jsonEncode(reqData);
    List<int> listData = utf8.encode(jsString);

    widget.bleTrx.transceive(0, BLE_CMD_DEV_TEST, BLE_CMD_DEV_TEST_WIFI, 0, listData).then((result) {
      if (widget.bleTrx.getRApduSW() == 0x9000) {
          showResultMessage(context, "热点连接成功", true);
      } else {
        String strSW = '0x${widget.bleTrx.getRApduSW().toRadixString(16).toUpperCase()}';
        showResultMessage(context, "热点连接失败 $strSW", false);
      }
    }).onError((error, stackTrace) {
      showResultMessage(context, "连接热点出现错误", false);
    }).timeout(const Duration(milliseconds: 10000), onTimeout: () {
      showResultMessage(context, "设备未响应", false);
    }).whenComplete(() {
      if (mounted) {
        setState(() {
          _testing = false;
        });
      }
    });
  }

  // 连接天气服务测试
  void testQWService(BuildContext context) {
    if (mounted) {
      setState(() {
        _testing = true;
      });
    }

    ScaffoldMessenger.of(context).hideCurrentSnackBar();

    var prov = _prov;
    if (prov.config.weKey.isEmpty || prov.config.weCity.isEmpty) {
      if (mounted) {
        ScaffoldMessenger.of(context).hideCurrentSnackBar();
        Snackbar.show(ABC.c, "请指定天气服务信息后再试", success: false);
        return;
      }
    }

    Map<String, dynamic> reqData = {
        'key': prov.config.weKey,
        'city': prov.config.weCity,
      };
      
    String jsString = jsonEncode(reqData);
    List<int> listData = utf8.encode(jsString);

    widget.bleTrx.transceive(0, BLE_CMD_DEV_TEST, BLE_CMD_DEV_TEST_QWSVC, 0, listData).then((result) {
      if (widget.bleTrx.getRApduSW() == 0x9000) {
          showResultMessage(context, "天气服务测试通过", true);
      } else {
        String strSW = '0x${widget.bleTrx.getRApduSW().toRadixString(16).toUpperCase()}';
        showResultMessage(context, "天气服务测试失败 $strSW", false);
      }
    }).onError((error, stackTrace) {
      showResultMessage(context, "出错了", false);
    }).timeout(const Duration(milliseconds: 5000), onTimeout: () {
      showResultMessage(context, "设备未响应", false);
    }).whenComplete(() {
      if (mounted) {
        setState(() {
          _testing = false;
        });
      }
    });
  }
  
  void showResultMessage(BuildContext context, String message, bool status) {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    Snackbar.show(ABC.c, message, success: status);
  }

  // get a list of local wifi hot-spots
  void devListWifi(BuildContext context, BleTransmit bleTrx) async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => WiFiListPage(bleTrx:bleTrx),
      ),
    );

    if (result != null) {
      _prov.config.ssid = result;
      _prov.notifyOnly();
    }
  }

  // search a city to request weather information
  void searchCity(BuildContext context, String currentCity) {
    MaterialPageRoute route = MaterialPageRoute(
        builder: (context) => SearchCityScreen(currentText:currentCity), 
        settings: RouteSettings(
                    name: '/SearchCity',
                    arguments: currentCity
        )
    );
    Navigator.of(context).push(route).then((value) {
      if (mounted) {
        setState(() {
          String strCurrent = (value != null) ? value : currentCity;
          List<String> parts = strCurrent.split(':');
          _prov.config.weCity = parts.first;
        });
      }
    });
  }

  // show popup message for qWeather Development Tip
  void qwApiKeyTip(BuildContext context) {
    if (mounted) {
      ScaffoldMessenger.of(context).hideCurrentSnackBar();
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: const Text("和风天气的秘钥可以从其官网免费获取"),
        action: SnackBarAction(
          label: "详情",
          onPressed: () {
            ScaffoldMessenger.of(context).hideCurrentSnackBar();
            final Uri url = Uri.parse('https://console.qweather.com/');
            launchInBrowser(url);
          },
        ),
      ));
    }
  }

  // launch url in default browser
  Future<void> launchInBrowser(Uri url) async {
    
    if (!await launchUrl(url, mode: LaunchMode.externalApplication)) {
      throw Exception('Could not launch $url');
    }
  }
}



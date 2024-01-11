
import 'dart:convert';
import 'dart:typed_data';

import 'package:archive/archive.dart';
import 'package:eforecast/utils/ble_transmit.dart';
import 'package:eforecast/utils/qwicons.dart';
import 'package:flutter/material.dart';

class WiFiListPage extends StatefulWidget {

  final BleTransmit bleTrx;

  const WiFiListPage({super.key, required this.bleTrx});
  
  @override
  State<WiFiListPage> createState() => _WiFiListPageState();
}

class _WiFiListPageState extends State<WiFiListPage> {
  // final List<String> hotspots = List.generate(20, (index) => 'Hotspot ${index + 1}');

  bool _isLoading = true;
  String _title = "可用 WiFi 热点";

  late List<dynamic> _listAPs;

  @override
  void initState () {
    super.initState();

    widget.bleTrx.transceive(0, BLE_CMD_LIST_WIFI, 0, 0, null).whenComplete(() {
      if (widget.bleTrx.getRApduSW() == 0x9000) {
        try {
          var listData = widget.bleTrx.getRApduData();
          Uint8List compressed = Uint8List.fromList(listData);
          final bytes = Inflate(compressed).getBytes();
          
          _isLoading = false;
          String jsonString  = utf8.decode(bytes);
          List<dynamic> listInfo = jsonDecode(jsonString);
          
          _listAPs = listInfo.where((item) => item['ssid'] != '').toList();
          _title = "可用 WiFi 热点";

          debugPrint("wifis: $jsonString");
          setState(() {
          });
        } catch (ex) {
          debugPrint("数据格式无效 ${ex.toString()}");
          _title = "[错误] 收到的数据格式无效";
          _listAPs = [];
          setState(() {
          });
        }
      } else {
        String strSW = '0x${widget.bleTrx.getRApduSW().toRadixString(16).toUpperCase()}';
        _title = "[错误] 获取列表失败: $strSW";
        _listAPs = [];
        setState(() {
          });
      }
    }).onError((error, stackTrace) {
      _title = "[错误] 获取列表失败";
      debugPrint(error.toString());
      _listAPs = [];
      setState(() {
          });
    }).timeout(const Duration(milliseconds: 5000), onTimeout: () {
      _title = "[错误] 设备未响应";
      _listAPs = [];
      setState(() {
      });
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_isLoading? "正在刷新列表" : _title),
      ),
      body: _isLoading? 
        const Center(child: CircularProgressIndicator()) :
        showWiFiLists(),
    );
  }
  
  IconData apTypeIcon(int type) {  
    if (type == 1) {
      return QWIcons.icoWifi5Limited;
    }
    else {
      return QWIcons.icoWifi3;
    }
  }

  String rssiToStrength(int rssi, int type) {  
    
    String strType =  (type == 1)? '加密网络': '开放网络';

    if (rssi <= -80) {  
      return "$strType，信号非常弱";
    } else if (rssi <= -70) {  
      return "$strType，信号弱";
    } else if (rssi <= -60) {  
      return "$strType，信号中等"; 
    } else {  
      return "$strType，信号强";
    }
  }

  Widget showWiFiLists() {
    return Card(
        margin: const EdgeInsets.all(10),
        child: ListView.separated(
          
          itemCount: _listAPs.length, // Double the itemCount to account for the separators
          itemBuilder: (context, index) {
            
            return ListTile(
              visualDensity: const VisualDensity(vertical: -3),
              title: Text(_listAPs[index]['ssid']),
              subtitle: Text(rssiToStrength(_listAPs[index]['rssi'], _listAPs[index]['type'])),
              leading: Icon(apTypeIcon(_listAPs[index]['type'])),
              onTap: () {
                Navigator.pop(context, _listAPs[index]['ssid']);
              },
            );
          },
          separatorBuilder: (BuildContext context, int index) => const Divider()
        ),
        
      );
  }
}


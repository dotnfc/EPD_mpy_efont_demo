// SPDX-License-Identifier: MIT License
//

import 'dart:convert';
import 'dart:typed_data';

import 'package:eforecast/utils/ble_transmit.dart';
import 'package:eforecast/utils/global_data.dart';
import 'package:eforecast/utils/qwicons.dart';
import 'package:eforecast/utils/snackbar.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class DeviceInfoTile extends StatefulWidget {

  final BleTransmit bleTrx;

  const DeviceInfoTile({super.key, required this.bleTrx});

  @override
  State<DeviceInfoTile> createState() => _DeviceInfoTileState();
}

class _DeviceInfoTileState extends State<DeviceInfoTile> {
  @override
  Widget build(BuildContext context) {

    return Consumer<GlobalConfigProvider>(builder: (context, value, child) {
      
      return Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(8),
          color: const Color.fromARGB(255, 242, 242, 242),
        ),
        child: ListTile(
          contentPadding: const EdgeInsets.only(left: 8, right: 8, top: 0, bottom: 0),
          visualDensity: const VisualDensity(vertical: -4),
          leading: const Icon(QWIcons.icoInfocircle),
          title: const Text('设备信息'),
          trailing: const MouseRegion(
            cursor: SystemMouseCursors.click,
            child: Icon(Icons.chevron_right_outlined)
          ),
          onTap: () => showDeviceInfo(context),
        )
      );
    });
  }

  void showDeviceInfo(BuildContext context) {
    widget.bleTrx.transceive(0, BLE_CMD_DEV_INFO, 0, 0, null)
      .whenComplete(() {
        if (widget.bleTrx.getRApduSW() == 0x9000) {

          try {
            var listData = widget.bleTrx.getRApduData();
            Uint8List bytes = Uint8List.fromList(listData);

            String jsonString = utf8.decode(bytes);
            Map<String, dynamic> devCfg = json.decode(jsonString);
            // GlobalConfig newConfig = GlobalConfig.fromJson(devCfg);


            
          } catch (ex) {
            debugPrint("数据格式无效 ${ex.toString()}");
            Snackbar.show(ABC.c, "设备配置无效", success: false);
          }
        }
        else {
          String strSW = '0x${widget.bleTrx.getRApduSW().toRadixString(16).toUpperCase()}';
          Snackbar.show(ABC.c, "获取配置失败: $strSW", success: false);
        }
      })
      .onError((error, stackTrace) {
        Snackbar.show(ABC.c, prettyException("获取配置失败:", error), success: false);
        debugPrint(error.toString());
      })
      .timeout(const Duration(milliseconds: 2000), onTimeout: (){
        Snackbar.show(ABC.c, "设备未响应", success: false);
        debugPrint("cfg timeout");
      });
  }
}
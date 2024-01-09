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
            trailing: const MouseRegion(cursor: SystemMouseCursors.click, child: Icon(Icons.chevron_right_outlined)),
            onTap: () => showDeviceInfo(context),
          ));
    });
  }

  void showDeviceInfo(BuildContext context) {
    widget.bleTrx.transceive(0, BLE_CMD_DEV_INFO, 0, 0, null).whenComplete(() {
      if (widget.bleTrx.getRApduSW() == 0x9000) {
        try {
          var listData = widget.bleTrx.getRApduData();
          Uint8List bytes = Uint8List.fromList(listData);

          String strDevInfo = utf8.decode(bytes);
          showDeviceInfoTable(strDevInfo);
        } catch (ex) {
          debugPrint("数据格式无效 ${ex.toString()}");
          Snackbar.show(ABC.c, "设备配置无效", success: false);
        }
      } else {
        String strSW = '0x${widget.bleTrx.getRApduSW().toRadixString(16).toUpperCase()}';
        Snackbar.show(ABC.c, "获取配置失败: $strSW", success: false);
      }
    }).onError((error, stackTrace) {
      Snackbar.show(ABC.c, prettyException("获取配置失败:", error), success: false);
      debugPrint(error.toString());
    }).timeout(const Duration(milliseconds: 2000), onTimeout: () {
      Snackbar.show(ABC.c, "设备未响应", success: false);
      debugPrint("cfg timeout");
    });
  }

  void showDeviceInfoTable(String strDevInfo) {
    showModalBottomSheet<void>(
      context: context,
      builder: (context) {
        return BottomSheetContent(strDevInfo);
      },
    );
  }
}

class BottomSheetContent extends StatelessWidget {
  final String strDevInfo;

  const BottomSheetContent(this.strDevInfo, {super.key});

  //
  @override
  Widget build(BuildContext context) {
    Map<String, dynamic> mapInfo = json.decode(strDevInfo);
    List<DataRow> rows = [];
    mapInfo.forEach((key, value) {
      rows.add(DataRow(
        cells: [
          DataCell(Text(key)),
          DataCell(Text(value.toString())),
        ],
      ));
    });

    return SizedBox(
      height: 300,
      child: Column(
        children: [
          SizedBox(
            height: 50,
            child: Stack(children: [
              const Center(
                child: Text("设备信息",
                    textAlign: TextAlign.center, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16.0)
                ),
              ),
              IconButton(
                icon: const Icon(Icons.close),
                onPressed: () {
                  Navigator.of(context).pop();
                }
              ),
            ]
          )
          ),
          // const Divider(thickness: 1),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: DataTable(
              headingRowHeight: 0,
              columns: const [
                DataColumn(label: Text("dummy")),
                DataColumn(label: Text('值')),
              ],
              rows: rows,
            ),
          )
        ],
      ),
    );
  }
}

// SPDX-License-Identifier: MIT License
//

import 'package:eforecast/utils/qwicons.dart';
import 'package:flutter/material.dart';

class DeviceInfoTile extends StatefulWidget {
  const DeviceInfoTile({super.key});

  @override
  State<DeviceInfoTile> createState() => _DeviceInfoTileState();
}

class _DeviceInfoTileState extends State<DeviceInfoTile> {
  @override
  Widget build(BuildContext context) {
    return Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(8),
          color: const Color.fromARGB(255, 242, 242, 242),
        ),
        child: const ListTile(
          contentPadding: EdgeInsets.only(left: 8, right: 8, top: 0, bottom: 0),
          visualDensity: VisualDensity(vertical: -4),
          leading: Icon(QWIcons.icoInfocircle),
          title: Text('设备信息'),
          trailing: Icon(Icons.chevron_right_outlined),
        )
    );
  }
}
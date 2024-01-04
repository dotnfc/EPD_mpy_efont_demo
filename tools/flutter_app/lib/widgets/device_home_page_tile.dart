// SPDX-License-Identifier: MIT License
//

import 'package:eforecast/utils/qwicons.dart';
import 'package:flutter/material.dart';

class HomePageTile extends StatefulWidget {
  const HomePageTile({super.key});

  @override
  State<HomePageTile> createState() => _HomePageTileState();
}

class _HomePageTileState extends State<HomePageTile> {
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
          leading: Icon(QWIcons.icoHome),
          title: Text('月历'),
          trailing: Icon(Icons.chevron_right_outlined),
        )
    );
  }
}

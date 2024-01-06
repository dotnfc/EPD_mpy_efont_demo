// SPDX-License-Identifier: MIT License
//

import 'package:eforecast/utils/global_data.dart';
import 'package:eforecast/utils/qwicons.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class HomePageTile extends StatefulWidget {
  const HomePageTile({super.key});

  @override
  State<HomePageTile> createState() => _HomePageTileState();
}

class _HomePageTileState extends State<HomePageTile> {
  @override
  void initState() {
    super.initState();

    GlobalConfigProvider configProvider = Provider.of<GlobalConfigProvider>(context, listen: false);
    
    configProvider.addListener(() => mounted ? setState(() {}) : null);
  }

  @override
  void dispose() {
    GlobalConfigProvider configProvider = Provider.of<GlobalConfigProvider>(context, listen: false);
    configProvider.removeListener(() {});
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    var pages = Provider.of<GlobalConfigProvider>(context, listen: true).config.pageList;
    var current = Provider.of<GlobalConfigProvider>(context, listen: true).config.pageNbr;
    var currentPageName = '未指定';

    pages.forEach((item) {
      if (item.id == current) {
        currentPageName = item.name;
      }
    });

    return Consumer<GlobalConfigProvider>(builder: (context, value, child) {
      return Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(8),
            color: const Color.fromARGB(255, 242, 242, 242),
          ),
          child: ListTile(
            contentPadding: const EdgeInsets.only(left: 8, right: 8, top: 0, bottom: 0),
            visualDensity: const VisualDensity(vertical: -4),
            leading: const Icon(QWIcons.icoHome),
            title: Text(currentPageName),
            trailing: const MouseRegion(
              cursor: SystemMouseCursors.click,
              child: Icon(Icons.chevron_right_outlined)
            ),
            onTap: () => changeHomePage(context),
          )
      );
    });
  }

  void changeHomePage(BuildContext context) {
    showModalBottomSheet<void>(
      context: context,
      builder: (context) {
        return const BottomSheetContent();
      },
    );
  }
}

//----------------------------------------------------------------
// A popup window to show HomePage Selection
class BottomSheetContent extends StatefulWidget {

  const BottomSheetContent({super.key});

  @override
  State<BottomSheetContent> createState() => _BottomSheetContent();
}

class _BottomSheetContent extends State<BottomSheetContent> {
  late int _current;

  @override
  void initState() {
    super.initState();
    
    _current = 0;
  }

  @override
  Widget build(BuildContext context) {
    _current = Provider.of<GlobalConfigProvider>(context, listen: true).config.pageNbr;
    var pages = Provider.of<GlobalConfigProvider>(context, listen: true).config.pageList;

    return SizedBox(
      height: 240,
      child: Column(
        children: [
          SizedBox(
            height: 40,
            child: Stack(
              children: [
                const Center(
                  child: Text(
                    '指定开机默认页面',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16.0)
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
          const Divider(thickness: 1),
          Expanded(
            child: ListView.separated(
              separatorBuilder: (context, index) {
                return const Divider(height: 1, color: Colors.grey);
              },
              itemCount: pages.length,
              itemBuilder: (context, index) {
                return InkWell(
                  onTap: () {
                    Provider.of<GlobalConfigProvider>(context, listen: false).config.pageNbr = pages[index].id;
                    _current = pages[index].id;
                    setState(() { });

                    Provider.of<GlobalConfigProvider>(context, listen: false).notifyOnly();
                  },
                  highlightColor: Colors.blueGrey,
                  child: ListTile(
                      visualDensity: const VisualDensity(vertical: -4),
                      title: Text(pages[index].name),
                      trailing: (pages[index].id == _current) ? const Icon(Icons.done) : null),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

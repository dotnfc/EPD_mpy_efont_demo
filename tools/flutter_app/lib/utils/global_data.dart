import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';

class PageItem {
  String name;
  String ico;
  int id;

  PageItem({
    required this.name,
    required this.ico,
    required this.id,
  });

  factory PageItem.fromJson(Map<String, dynamic> json) {
    return PageItem(
      name: json['name'],
      ico: json['ico'],
      id: json['id'],
    );
  }
}

class GlobalConfig {
  String weCity;
  String passwd;
  String ssid;
  int pageNbr;
  List<PageItem> pageList;
  String weKey;

  GlobalConfig({
    required this.weCity,
    required this.passwd,
    required this.ssid,
    required this.pageNbr,
    required this.pageList,
    required this.weKey,
  });

  factory GlobalConfig.fromJson(Map<String, dynamic> json) {
    var pageListJson = json['page_list'];
    List<dynamic> pageListDecoded = jsonDecode(pageListJson);
    
    List<PageItem> pages = pageListDecoded.map((page) => PageItem.fromJson(page)).toList();

    return GlobalConfig(
      weCity: json['we_city'],
      passwd: json['passwd'],
      ssid: json['ssid'],
      pageNbr: json['page_nbr'],
      //pageList: List<PageItem>.from(
      //  json['page_list'].map((pageItem) => PageItem.fromJson(pageItem)),
      //),
      pageList: pages,
      weKey: json['we_key'],
    );
  }

  // 默认构造函数，所有数据为空或0
  GlobalConfig.empty()
      : weCity = '',
        passwd = '',
        ssid = '',
        pageNbr = 0,
        pageList = [],
        weKey = '';
}

class GlobalConfigProvider with ChangeNotifier {
  GlobalConfig _config;

  GlobalConfigProvider() : _config = GlobalConfig.empty();

  GlobalConfig get config => _config;

  set config(GlobalConfig newConfig) {
    _config = newConfig;
    // 通知监听器配置已更改
    notifyListeners();
  }

  void notifyOnly() {
    notifyListeners();
  }
  void updateConfig(GlobalConfig newConfig) {
    config = newConfig;
  }
}

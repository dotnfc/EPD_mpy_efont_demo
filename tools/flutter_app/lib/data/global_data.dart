import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';

/* represents data
 {
    "we_city": "101010100", 
    "passwd": "20241212", 
    "ssid": "DOTNFC-HOS", 
    "page_nbr": 1, 
    "page_list": [
      {"name": "设置", "ico": "qi-ico-home", "id": 1}, 
      {"name": "月历", "ico": "qi-ico-calendarmonth", "id": 2}, 
      {"name": "天气", "ico": "qi-sunny", "id": 3}
    ], 
    "we_key": "6d76a5bd96da4eada10fbf19c7077fbb"
  }
*/
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

  Map<String, dynamic> toJson() {
    return {
      'we_city': weCity,
      'passwd': passwd,
      'ssid': ssid,
      'page_nbr': pageNbr,
      'we_key': weKey,
    };
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
    notifyListeners();
  }

  void notifyOnly() {
    notifyListeners();
  }

  void reset() {
    _config = GlobalConfig.empty();
  }

  void updateConfig(GlobalConfig newConfig) {
    config = newConfig;
  }
}

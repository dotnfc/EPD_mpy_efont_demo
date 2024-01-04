import 'package:eforecast/screens/search_city_screen.dart';
import 'package:eforecast/utils/qwicons.dart';
import 'package:eforecast/widgets/password_text_field.dart';
import 'package:flutter/material.dart';
import 'package:flutter_material_symbols/flutter_material_symbols.dart';
import 'package:url_launcher/url_launcher.dart';

class DeviceConnectTile extends StatefulWidget {
  const DeviceConnectTile({super.key});

  @override
  State<DeviceConnectTile> createState() => _DeviceConnectTileState();
}

class _DeviceConnectTileState extends State<DeviceConnectTile> {
  // final icoLock = const Icon(MaterialSymbols.lock, fill: 0, weight: 200);
  // final icoLock = const Icon(Icons.lock_outline, weight: 200, color: Colors.green);

  // WiFi Connection
  late TextEditingController _ctrlTextSSID;
  late TextEditingController _ctrlTextPass;

  // Weather API
  late TextEditingController _ctrlTextQWKey;
  late TextEditingController _ctrlTextQWCity;

  @override
  void initState() {
    super.initState();

    _ctrlTextSSID = TextEditingController(text: '7Days');
    _ctrlTextPass = TextEditingController(text: '12345678');

    _ctrlTextQWKey= TextEditingController(text: 'QWeather API Key');
    _ctrlTextQWCity= TextEditingController(text: '1000100');
  }

  @override
  Widget build(BuildContext context) {
    return Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(10),
          color: const Color.fromARGB(255, 242, 242, 242),
        ),
        child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(children: [
              TextField(
                controller: _ctrlTextSSID,
                decoration: InputDecoration(
                  icon: const Icon(QWIcons.icoWifi3, color: Colors.green),
                  hintText: 'WiFi 热点',
                  labelText: '请输入热点名',
                  suffixIcon: IconButton(
                    icon: const Icon(Icons.chevron_right_outlined),
                    onPressed: () { devListWifi(); }
                  ),
                ),
              ),
              const SizedBox(height: 6),
              PasswordTextField(
                controller: _ctrlTextPass,
                icon: const Icon(MaterialSymbols.lock, fill: 0, weight: 200, color: Colors.green),
                hintText: 'WiFi 密码',
                labelText: '热点访问密码',
              ),
              const SizedBox(height: 10),
              TextField(
                controller: _ctrlTextQWKey,
                decoration: InputDecoration(
                  icon: const Icon(QWIcons.icoLogoCarkey, color: Colors.orangeAccent),
                  hintText: 'API KEY',
                  labelText: '和风天气秘钥',
                  suffixIcon: IconButton(
                    icon: const Icon(QWIcons.icoInfocircle),
                    onPressed: () { qwApiKeyTip(context); }
                  ),
                ),
              ),
              const SizedBox(height: 6),
              TextField(
                readOnly: true,
                controller: _ctrlTextQWCity,
                decoration: InputDecoration(
                  icon: const Icon(QWIcons.icoGlobe2, color: Colors.orangeAccent),
                  hintText: '城市编码',
                  labelText: '指定城市',
                  suffixIcon: IconButton(
                    icon: const Icon(Icons.chevron_right_outlined),
                    onPressed: () { searchCity(context, _ctrlTextQWCity.text); }
                  ),
                ),
              ),
              const SizedBox(height: 6),
            ]
          )
        )
    );
  }
  
  // get a list of local wifi hot-spots
  void devListWifi() {
    setState(() {
    });
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
          
          _ctrlTextQWCity.text = parts.first;
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
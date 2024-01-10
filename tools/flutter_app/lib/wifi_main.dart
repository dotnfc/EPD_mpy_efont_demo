import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String selectedHotspot = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('WiFi Hotspots'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () async {
                final result = await Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => HotspotListPage(),
                  ),
                );

                if (result != null) {
                  setState(() {
                    selectedHotspot = result;
                  });
                }
              },
              child: Text('Show WiFi Hotspots'),
            ),
            SizedBox(height: 20),
            Text(
              'Selected Hotspot: $selectedHotspot',
              style: TextStyle(fontSize: 18),
            ),
          ],
        ),
      ),
    );
  }
}

class HotspotListPage extends StatelessWidget {
  final List<String> hotspots = List.generate(20, (index) => 'Hotspot ${index + 1}');

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('WiFi Hotspots List'),
      ),
      body: Card(
        child: ListView.builder(
          
          itemCount: hotspots.length * 2 - 1, // Double the itemCount to account for the separators
          itemBuilder: (context, index) {
            if (index.isOdd) {
              return Divider(height: 0.1, color: Colors.grey); // Custom separator using DecoratedBox
            }

            final hotspotIndex = index ~/ 2;
            return ListTile(
              visualDensity: VisualDensity(vertical: -3),
              title: Text(hotspots[hotspotIndex]),
              subtitle: Text('Encryption: WPA2, Signal Strength: Strong'),
              leading: Icon(Icons.wifi),
              onTap: () {
                Navigator.pop(context, hotspots[hotspotIndex]);
              },
            );
          },
        ),
      ),
    );
  }
}


// class MyHomePage extends StatelessWidget {
//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(
//         title: Text('WiFi热点列表'),
//       ),
//       body: Center(
//         child: ElevatedButton(
//           onPressed: () {
//             _showWifiListDialog(context);
//           },
//           child: Text('显示WiFi热点列表'),
//         ),
//       ),
//     );
//   }

//  void _showWifiListDialog(BuildContext context) {
//     showDialog(
//       context: context,
//       builder: (BuildContext context) {
//         return Dialog(
//           insetPadding: EdgeInsets.all(0),
//           child: Container(
//             width: double.maxFinite,
//             height: double.maxFinite,
//             child: ListView.builder(
//               shrinkWrap: true,
//               itemCount: 20,
//               itemBuilder: (BuildContext context, int index) {
//                 // 模拟测试数据
//                 String ssid = 'WiFi热点 $index';
//                 bool isEncrypted = index % 2 == 0; // 每隔一个加密
//                 int signalStrength = (index % 4) + 1; // 信号强度 1-4

//                 return Card(
//                   child: ListTile(
//                     title: Text(ssid),
//                     subtitle: Text('加密: ${isEncrypted ? '是' : '否'}'),
//                     trailing: _buildSignalStrengthIcon(signalStrength),
//                   ),
//                 );
//               },
//             ),
//           ),
          
//         );
//       },
//     );
//   }

//   // 根据信号强度返回相应的图标
//   Widget _buildSignalStrengthIcon(int strength) {
//     IconData iconData;
//     Color iconColor;

//     switch (strength) {
//       case 1:
//         iconData = Icons.network_wifi_1_bar;
//         iconColor = Colors.red;
//         break;
//       case 2:
//         iconData = Icons.network_wifi_2_bar;
//         iconColor = Colors.orange;
//         break;
//       case 3:
//         iconData = Icons.network_wifi_3_bar;
//         iconColor = Colors.yellow;
//         break;
//       case 4:
//         iconData = Icons.signal_wifi_4_bar;
//         iconColor = Colors.green;
//         break;
//       default:
//         iconData = Icons.signal_wifi_off;
//         iconColor = Colors.grey;
//         break;
//     }

//     return Icon(
//       iconData,
//       color: iconColor,
//     );
//   }

//   // 新增的方法，用于显示WiFi热点列表的对话框
//   void _showWiFiListDialog1(BuildContext context) {
//     showDialog(
//       context: context,
//       builder: (BuildContext context) {
//         return GestureDetector(
//           onTap: () {
//             Navigator.of(context).pop();
//           },
//           child: AlertDialog(
//             title: Text('WiFi热点列表'),
//             content: Container(
//               width: double.maxFinite,
//               height: 300,
//               child: SingleChildScrollView(
//                 child: Column(
//                   children: [
//                     // 使用ListView.builder创建一个滚动的WiFi热点列表
//                     ListView.builder(
//                       shrinkWrap: true,
//                       physics: NeverScrollableScrollPhysics(),
//                       itemCount: 10, // 增加到10个WiFi热点
//                       itemBuilder: (BuildContext context, int index) {
//                         // 替换以下内容为真实的WiFi热点信息
//                         String ssid = 'WiFi热点 $index';
//                         bool isEncrypted = index % 2 == 0; // 偶数为加密
//                         int signalStrength = (index * 20) % 100;

//                         return Card(
//                           child: ListTile(
//                             title: Text(ssid),
//                             subtitle: Text('加密: ${isEncrypted ? '是' : '否'}'),
//                             trailing: Icon(Icons.signal_wifi_4_bar), // 替换为实际的信号强度图标
//                           ),
//                         );
//                       },
//                     ),
//                   ],
//                 ),
//               ),
//             ),
//             actions: [
//               TextButton(
//                 onPressed: () {
//                   Navigator.of(context).pop();
//                 },
//                 child: Text('关闭'),
//               ),
//             ],
//           ),
//         );
//       },
//     );
//   }
// }
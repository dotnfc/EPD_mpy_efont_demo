import 'dart:async';

import 'package:eforecast/utils/qwicons.dart';
import 'package:eforecast/widgets/password_text_field.dart';
import 'package:flutter/material.dart';
import 'package:flutter_blue_plus_windows/flutter_blue_plus_windows.dart';

import '../utils/snackbar.dart';
import '../utils/extra.dart';
import '../utils/constants.dart';
import '../utils/utils.dart';

class DeviceScreen extends StatefulWidget {
  final BluetoothDevice device;

  const DeviceScreen({Key? key, required this.device}) : super(key: key);

  @override
  State<DeviceScreen> createState() => _DeviceScreenState();
}

class _DeviceScreenState extends State<DeviceScreen> {
  int? _rssi;
  int? _mtuSize;
  BluetoothConnectionState _connectionState = BluetoothConnectionState.disconnected;
  List<BluetoothService> _services = [];
  bool _isDiscoveringServices = false;
  bool _isConnecting = false;
  bool _isDisconnecting = false;

  late StreamSubscription<BluetoothConnectionState> _connectionStateSubscription;
  late StreamSubscription<bool> _isConnectingSubscription;
  late StreamSubscription<bool> _isDisconnectingSubscription;
  late StreamSubscription<int> _mtuSubscription;

  final List<int> _responseValue = [];
  int _responseLength = 0;

  BluetoothCharacteristic? _nusDeviceCharRx;

  late TextEditingController _ctrlTextAssets;
  late TextEditingController _ctrlTextConsume;

  @override
  void initState() {
    super.initState();

    _ctrlTextAssets = TextEditingController(text: '9999.99');
    _ctrlTextConsume = TextEditingController(text: '100.00');

    _connectionStateSubscription = widget.device.connectionState.listen((state) async {
      _connectionState = state;
      debugPrint("new state: $_connectionState");
      if (state == BluetoothConnectionState.connected) {
        _services = []; // must rediscover services
      }
      if (state == BluetoothConnectionState.connected && _rssi == null) {
        try {
          _rssi = await widget.device.readRssi();
        } catch (e) {
          Snackbar.show(ABC.c, prettyException("readRssi Error:", e), success: false);
        }
      }
      if (mounted) {
        setState(() {});
      }
    });

    _mtuSubscription = widget.device.mtu.listen((value) {
      _mtuSize = value;
      if (mounted) {
        setState(() {});
      }
    });

    _isConnectingSubscription = widget.device.isConnecting.listen((value) {
      _isConnecting = value;
      if (mounted) {
        setState(() {});
      }
    });

    _isDisconnectingSubscription = widget.device.isDisconnecting.listen((value) {
      _isDisconnecting = value;
      if (mounted) {
        setState(() {});
      }
    });

    onDiscoverServicesPressed();
  }

  @override
  void dispose() {
    _connectionStateSubscription.cancel();
    _mtuSubscription.cancel();
    _isConnectingSubscription.cancel();
    _isDisconnectingSubscription.cancel();
    //_lastValueSubscription.cancel();
    super.dispose();
  }

  void onConsume() async {
    String strTotal = _ctrlTextAssets.text;
    String strConsume = _ctrlTextConsume.text;

    List<int> total = convertIntToHexList(strTotal);
    List<int> consume = convertIntToHexList(strConsume);
    List<int> data = total + consume;

    await devTransmit(0x00, 0xf2, 0x00, 0x03, data);
  }

  void onGetDevID() async {

    await devTransmit(0x00, 0x02, 0x01, 0x00, []);
  }

  bool get isConnected {
    return _connectionState == BluetoothConnectionState.connected;
  }

  Future onConnectPressed() async {
    try {
      await widget.device.connectAndUpdateStream();
      Snackbar.show(ABC.c, "Connect: Success", success: true);
    } catch (e) {
      if (e is FlutterBluePlusException && e.code == FbpErrorCode.connectionCanceled.index) {
        // ignore connections canceled by the user
      } else {
        Snackbar.show(ABC.c, prettyException("Connect Error:", e), success: false);
      }
    }
  }

  Future onCancelPressed() async {
    try {
      await widget.device.disconnectAndUpdateStream(queue: false);
      Snackbar.show(ABC.c, "Cancel: Success", success: true);
    } catch (e) {
      Snackbar.show(ABC.c, prettyException("Cancel Error:", e), success: false);
    }
  }

  Future onDisconnectPressed() async {
    try {
      await widget.device.disconnectAndUpdateStream();
      Snackbar.show(ABC.c, "Disconnect: Success", success: true);
    } catch (e) {
      Snackbar.show(ABC.c, prettyException("Disconnect Error:", e), success: false);
    }
  }

  Future onDiscoverServicesPressed() async {
    if (mounted) {
      setState(() {
        _isDiscoveringServices = true;
      });
    }
    try {
      _services = await widget.device.discoverServices(subscribeToServicesChanged: false);
      //showVendorInfo(_services);
      //showBatteryInfo(_services);

      final nusServiceUUID = _services.singleWhere((item) => item.serviceUuid == Guid(NUS_SERVICE_UUID));

      final nusTxCharacterUUID = nusServiceUUID.characteristics
          .singleWhere((item) => item.characteristicUuid == Guid(NUS_TX_CHARACTERISTIC_UUID));

      await nusTxCharacterUUID.setNotifyValue(true);
      //StreamSubscription<List<int>> _lastValueSubscription =
      nusTxCharacterUUID.lastValueStream.listen((value) {
        if (value.isEmpty) {
          return;
        }
        if (_responseValue.isEmpty) {
          // first frame
          if ((value[0] == FRAME_PING) || (value[0] == FRAME_KEEP_ALIVE) || (value[0] == FRAME_ERROR)) {
            return; // drop this invalid state frame
          }
          if (value[0] == FRAME_MSG) {
            _responseValue.addAll(value.sublist(3));
            _responseLength = (value[1] << 8) + value[2];
          }
        } else {
          _responseValue.addAll(value.sublist(1)); // exluding seq
        }

        if (_responseLength <= _responseValue.length) {
          // String strResponse = _responseValue.map((int value) => value.toRadixString(16).padLeft(2, '0')).join();
          
        }
      });

      _nusDeviceCharRx = nusServiceUUID.characteristics
          .singleWhere((item) => item.characteristicUuid == Guid(NUS_RX_CHARACTERISTIC_UUID));

      Snackbar.show(ABC.c, "Discover Services: Success", success: true);
    } catch (e) {
      Snackbar.show(ABC.c, prettyException("Discover Services Error:", e), success: false);
    }
    if (mounted) {
      setState(() {
        _isDiscoveringServices = false;
      });
    }
  }

  Widget buildSpinner(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.all(14.0),
      child: AspectRatio(
        aspectRatio: 1.0,
        child: CircularProgressIndicator(
          backgroundColor: Colors.black12,
          color: Colors.black26,
        ),
      ),
    );
  }

  Widget buildGetServices(BuildContext context) {
    return IndexedStack(
      index: (_isDiscoveringServices) ? 1 : 0,
      children: <Widget>[
        ElevatedButton(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.blue,
            foregroundColor: Colors.white,
            //shadowColor: Colors.blueAccent,
            //elevation: 10,
          ),
          onPressed: onDiscoverServicesPressed,
          child: const Text("取服务列表"),
        ),
        const IconButton(
          icon: SizedBox(
            width: 18.0,
            height: 18.0,
            child: CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation(Colors.grey),
            ),
          ),
          onPressed: null,
        )
      ],
    );
  }

  Widget buildDividerTile(BuildContext context) {
    return const SizedBox(height: 10);
  }

  Widget buildConnectTile(BuildContext context) {
    return Container(
          decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(10),
          color: const Color.fromARGB(255, 242, 242, 242),
        ),
        child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(children: [
              const SizedBox(height: 6),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.blue,
                      foregroundColor: Colors.white,
                      shadowColor: Colors.blueAccent,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(5.0),
                      ),
                    ),
                    onPressed: () {},
                    child: const Text("WiFi 热点列表")),
              ),
              const SizedBox(height: 6),
              TextField(
                controller: _ctrlTextConsume,
                decoration: const InputDecoration(
                  icon: Icon(QWIcons.icoWifi3, color: Colors.green),
                  hintText: 'WiFi 热点',
                  labelText: '请输入热点名',
                ),
              ),
              const SizedBox(height: 6),
              PasswordTextField(
                controller: _ctrlTextConsume,
                icon: const Icon(Icons.lock, color: Colors.green),
                hintText: 'WiFi 密码',
                labelText: '热点访问密码',
              ),
              const SizedBox(height: 10),
              TextField(
                controller: _ctrlTextConsume,
                decoration: const InputDecoration(
                  icon: Icon(QWIcons.icoLogoCarkey, color: Colors.orangeAccent),
                  hintText: 'API KEY',
                  labelText: '和风天气秘钥',
                ),
              ),
              const SizedBox(height: 6),
              TextField(
                controller: _ctrlTextConsume,
                decoration: const InputDecoration(
                  icon: Icon(QWIcons.icoGlobe2, color: Colors.orangeAccent),
                  hintText: '城市编码',
                  labelText: '请求指定城市',
                ),
              ),
              const SizedBox(height: 6),
            ])));
  }

  Widget getItem(int index) {
    return ListTile(
      leading: Icon(QWIcons.icoWechat),

      title: Text("item name"),
      // trailing: Icon(Icons.keyboard_arrow_right_outlined),
      onTap: () {
        // print('index');
      },
      onLongPress: () {
        // print('${item.desc}');
      },
    );
  }

  Widget buildHomeTile(BuildContext context) {
    return Expanded(
        child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(10),
          color: const Color.fromARGB(255, 242, 242, 242),
        ),
        child: ListView.builder(
          itemCount: 3,
          itemBuilder: (context, index) {
            return getItem(index);
          },
        ) 
      )
    );
  }

  Widget buildInfoTile(BuildContext context) {
    return Expanded(
        child: Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(10),
        color: const Color.fromARGB(255, 242, 242, 242),
      ),
    ));
  }

  Widget buildConnectButton(BuildContext context) {
    return Row(children: [
      if (_isConnecting || _isDisconnecting) buildSpinner(context),
      TextButton(
          onPressed: _isConnecting ? onCancelPressed : (isConnected ? onDisconnectPressed : onConnectPressed),
          child: Text(
            _isConnecting ? "取消" : (isConnected ? "断开连接" : "连接"),
            style: Theme.of(context).primaryTextTheme.labelLarge?.copyWith(color: Colors.white),
          ))
    ]);
  }

  Widget showDeviceState(BuildContext context) {
    return ListTile(
      title: Text('设备已${getBleState()}')
    );
  }

  String getBleState() {
    return _connectionState == BluetoothConnectionState.connected ? "连接" : "断开";
  }

  @override
  Widget build(BuildContext context) {
    return ScaffoldMessenger(
      key: Snackbar.snackBarKeyC,
      child: Scaffold(
          resizeToAvoidBottomInset: false, // fix 'Bottom overflowed by xxx pixels'
          appBar: AppBar(
            title: Text(widget.device.platformName),
            actions: [buildConnectButton(context)],
            backgroundColor: Colors.lightBlue,
            foregroundColor: Colors.white,
          ),
          body: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: <Widget>[
                isConnected ? Container() : showDeviceState(context),
                isConnected ? buildConnectTile(context) : Container(),
                isConnected ? buildDividerTile(context) : Container(),
                isConnected ? buildHomeTile(context) : Container(),
                isConnected ? buildDividerTile(context) : Container(),
                isConnected ? buildInfoTile(context) : Container(),
              ],
            ),
          )),
    );
  }

  Future<void> devTransmit(int cla, int ins, int p1, int p2, List<int> data) async {
    _responseValue.clear();
    _responseLength = 0;

    if (!isConnected) {
      return;
    }

    int seq = -1;
    List<int> frame = [0x00, 0x00];
    List<int> apdu = [cla, ins, p1, p2, data.isEmpty ? 0 : data.length];

    int tlen = 5 + data.length;
    frame[0] = (tlen & 0xff00) >> 8;
    frame[1] = (tlen & 0xff);
    frame.addAll(apdu);
    if (data.isNotEmpty) {
      frame.addAll(data);
    }

    final chunkSize = _mtuSize! - 3;
    final blockSize = chunkSize - 1;
    for (var i = 0; i < frame.length; i += blockSize) {
      final chunk = frame.sublist(i, i + blockSize > frame.length ? frame.length : i + blockSize);
      List<int> chunkBuf = [];
      if (seq < 0) {
        chunkBuf.add(FRAME_MSG);
        chunkBuf.addAll(chunk);
        seq = 0;
      } else {
        chunkBuf.add(seq);
        chunkBuf.addAll(chunk);
        seq = seq + 1;
        if (seq >= 0x80) {
          seq = 0;
        }
      }

      try {
        await _nusDeviceCharRx?.write(chunkBuf, timeout: 1);
      } catch (e) {
        debugPrint('发送失败 $e.message');
      }
    }
  }
}

// SPDX-License-Identifier: MIT License
//
// main page for devcie operations
//

import 'dart:async';

import 'package:eforecast/utils/ble_transmit.dart';
import 'package:eforecast/utils/qwicons.dart';
import 'package:eforecast/widgets/device_connect_tile.dart';
import 'package:eforecast/widgets/device_home_page_tile.dart';
import 'package:eforecast/widgets/device_info_tile.dart';
import 'package:flutter/material.dart';
import 'package:flutter_blue_plus_windows/flutter_blue_plus_windows.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
// import 'package:eforecast/l10n/l10n.dart';

import '../utils/snackbar.dart';
import '../utils/extra.dart';
import '../utils/constants.dart';

class DeviceScreen extends StatefulWidget {
  final BluetoothDevice device;

  const DeviceScreen({super.key, required this.device});

  @override
  State<DeviceScreen> createState() => _DeviceScreenState();
}

class _DeviceScreenState extends State<DeviceScreen> {
  int? _rssi;
  late BleTransmit bleTrx;

  BluetoothConnectionState _connectionState = BluetoothConnectionState.disconnected;
  List<BluetoothService> _services = [];
  bool _isDiscoveringServices = false;
  bool _isConnecting = false;
  bool _isDisconnecting = false;

  late StreamSubscription<BluetoothConnectionState> _connectionStateSubscription;
  late StreamSubscription<bool> _isConnectingSubscription;
  late StreamSubscription<bool> _isDisconnectingSubscription;
  late StreamSubscription<int> _mtuSubscription;

  @override
  void initState() {
    super.initState();
    bleTrx = BleTransmit();
    bleTrx.init(context);

    _connectionStateSubscription = widget.device.connectionState.listen((state) async {
      _connectionState = state;
      debugPrint("new state: $_connectionState");
      if (state == BluetoothConnectionState.connected) {
        _services = []; // must rediscover services

        // 当设备连接后，延迟 0.2 s 去发现服务
        Future.delayed(const Duration(milliseconds: 200), () {
          discoverDeviceServices(); //
        });
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
      bleTrx.setMtu(value);
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

  bool get isConnected {
    return _connectionState == BluetoothConnectionState.connected;
  }

  String getBleStateString() {
    return isConnected ? "连接" : "断开";
  }

  Future onConnectPressed() async {
    try {
      await widget.device.connectAndUpdateStream();
      //Snackbar.show(ABC.c, "Connect: Success", success: true);
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

  Future discoverDeviceServices() async {
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
        bleTrx.recvBlock(value);
      });

      BluetoothCharacteristic nusDeviceCharRx = nusServiceUUID.characteristics
          .singleWhere((item) => item.characteristicUuid == Guid(NUS_RX_CHARACTERISTIC_UUID));
      bleTrx.setRxChar(nusDeviceCharRx);
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

  Widget buildDividerTile(BuildContext context) {
    return const SizedBox(height: 10);
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
      title: Text('设备已${getBleStateString()}')
    );
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
                isConnected ? const DeviceConnectTile() : Container(),
                isConnected ? buildDividerTile(context) : Container(),
                isConnected ? const HomePageTile() : Container(),
                isConnected ? buildDividerTile(context) : Container(),
                isConnected ? const DeviceInfoTile() : Container(),
              ],
            ),
          ),
          floatingActionButton: bottomButtons()
        ),
    );
  }

  Widget bottomButtons() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.end,
      children: [
                                  // 获取设备当前配置
        FloatingActionButton.extended(
          onPressed: () => devInfoReload(),
          heroTag: 'devload',
          backgroundColor: Colors.blue,
          foregroundColor: Colors.white,
          icon: const Icon(QWIcons.icoRefresh),
          label: const Text("载入"),
          extendedPadding: const EdgeInsetsDirectional.all(10)
        ),
        
        const SizedBox(width: 12), // 保存/更新配置
        FloatingActionButton.extended(
          onPressed: () => devInfoUpdate(),
          heroTag: 'devsave',
          backgroundColor: Colors.blue,
          foregroundColor: Colors.white,
          icon: const Icon(QWIcons.icoSave),
          label: const Text("保存"),
          extendedPadding: const EdgeInsetsDirectional.all(10)
        ),
        
        const SizedBox(width: 12), // 重启设备
        FloatingActionButton.extended(
          onPressed: () {
            bleTrx.cmdReset();
          },
          heroTag: 'devreset',
          backgroundColor: Colors.red[600],
          icon: const Icon(QWIcons.icoRestart),
          label: const Text("重启"),
          extendedPadding: const EdgeInsetsDirectional.all(8)
        ),
      ],
    );
  }

  void devInfoReload() {

  }

  void devInfoUpdate() {
    
  }
}


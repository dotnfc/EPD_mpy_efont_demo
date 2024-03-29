// SPDX-License-Identifier: MIT License
//
// scan BLE devices nearby
//

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_blue_plus_windows/flutter_blue_plus_windows.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'device_screen.dart';
import '../utils/snackbar.dart';
import '../widgets/system_device_tile.dart';
import '../widgets/scan_result_tile.dart';
import '../utils/extra.dart';
import 'package:package_info_plus/package_info_plus.dart';

class ScanScreen extends StatefulWidget {
  const ScanScreen({super.key});

  @override
  State<ScanScreen> createState() => _ScanScreenState();
}

class _ScanScreenState extends State<ScanScreen> {
  List<BluetoothDevice> _systemDevices = [];
  final List<ScanResult> _scanResults = [];
  bool _isScanning = false;
  late StreamSubscription<List<ScanResult>> _scanResultsSubscription;
  late StreamSubscription<bool> _isScanningSubscription;
  String _version = 'Unknown';

  @override
  void initState() {
    super.initState();
    getAppVersion();

    _scanResultsSubscription = FlutterBluePlus.scanResults.listen((results) {

      // filtering devices
      if (results.isNotEmpty) {
        for (ScanResult result in results) {
          String deviceName = result.device.platformName;
          if (deviceName.startsWith('eFore-') && (!_scanResults.contains(result)) ){
            _scanResults.add(result);
          }
        }
      }
      // _scanResults = results;

      if (mounted) {
        setState(() {});
      }
    }, onError: (e) {
      Snackbar.show(ABC.b, prettyException("Scan Error:", e), success: false);
    });

    _isScanningSubscription = FlutterBluePlus.isScanning.listen((state) {
      _isScanning = state;
      if (mounted) {
        setState(() {});
      }
    });
  }

  @override
  void dispose() {
    _scanResultsSubscription.cancel();
    _isScanningSubscription.cancel();
    super.dispose();
  }

  Future<void> getAppVersion() async {
    final PackageInfo packageInfo = await PackageInfo.fromPlatform();
    // String appName = packageInfo.appName;
    // String packageName = packageInfo.packageName;
    // String version = packageInfo.version;
    // String buildNumber = packageInfo.buildNumber;
    setState(() {
      _version = packageInfo.version;
    });
  }


  Future onScanPressed() async {
    _scanResults.clear();
    if (mounted) {
      setState(() {});
    }

    try {
      _systemDevices = await FlutterBluePlus.systemDevices;
    } catch (e) {
      Snackbar.show(ABC.b, prettyException("System Devices Error:", e), success: false);
    }
    try {
      // android is slow when asking for all advertisments,
      // so instead we only ask for 1/8 of them
      // int divisor = Platform.isAndroid ? 8 : 1;
      await FlutterBluePlus.startScan(
          // timeout: const Duration(seconds: 15), continuousUpdates: true, continuousDivisor: divisor);
          timeout: const Duration(seconds: 15));
    } catch (e) {
      Snackbar.show(ABC.b, prettyException("Start Scan Error:", e), success: false);
    }
    if (mounted) {
      setState(() {});
    }
  }

  Future onStopPressed() async {
    try {
      FlutterBluePlus.stopScan();
    } catch (e) {
      Snackbar.show(ABC.b, prettyException("Stop Scan Error:", e), success: false);
    }
  }

  void onConnectPressed(BluetoothDevice device) {
    device.connectAndUpdateStream().catchError((e) {
      Snackbar.show(ABC.c, prettyException("Connect Error:", e), success: false);
    });

    // before we go, stop scan
    onStopPressed();
    
    MaterialPageRoute route = MaterialPageRoute(
        builder: (context) => DeviceScreen(device: device), 
        settings: const RouteSettings(name: '/DeviceScreen'));
    Navigator.of(context).push(route);
  }

  Future onRefresh() {
    if (_isScanning == false) {
      FlutterBluePlus.startScan(timeout: const Duration(seconds: 5));
    }
    if (mounted) {
      setState(() {});
    }
    return Future.delayed(const Duration(milliseconds: 500));
  }

  Widget buildScanButton(BuildContext context) {
    if (FlutterBluePlus.isScanningNow) {
      return FloatingActionButton(
        onPressed: onStopPressed,
        backgroundColor: Colors.red,
        foregroundColor: Colors.white,
        child: const Icon(Icons.stop),
      );
    } else {
      return FloatingActionButton(
        onPressed: onScanPressed, 
        backgroundColor: Colors.lightBlue,
        foregroundColor: Colors.white,
        child: Text(AppLocalizations.of(context)!.scan));
    }
  }

  List<Widget> _buildSystemDeviceTiles(BuildContext context) {
    return _systemDevices
        .map(
          (d) => ScannedDeviceTile(
            device: d,
            onOpen: () => Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => DeviceScreen(device: d),
                settings: const RouteSettings(name: '/DeviceScreen'),
              ),
            ),
            onConnect: () => onConnectPressed(d),
          ),
        )
        .toList();
  }

  List<Widget> _buildScanResultTiles(BuildContext context) {
    return _scanResults
        .map(
          (r) => ScanResultTile(
            result: r,
            onTap: () => onConnectPressed(r.device),
          ),
        )
        .toList();
  }

  Widget buildSpinner(BuildContext context) {
    if (_isScanning) {
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
    else {
      return Container();
    }
  }

  Widget showVersion(BuildContext context) {
    return Positioned(
      left: 16.0,
      bottom: 16.0,
      child: Text(
        '版本 V$_version',
        style: const TextStyle(
          fontSize: 11.0,
          color: Colors.grey, 
        ),
      ),
    );      
  }

  Widget buildResult(BuildContext context) {
    return RefreshIndicator(
          onRefresh: onRefresh,
          child: ListView(
            children: <Widget>[
              ..._buildSystemDeviceTiles(context),
              ..._buildScanResultTiles(context),
            ],
          ),
        );
  }

  @override
  Widget build(BuildContext context) {
    return ScaffoldMessenger(
      key: Snackbar.snackBarKeyB,
      child: Scaffold(
        appBar: AppBar(
          leading: const Icon(Icons.bluetooth),
          title: Text(AppLocalizations.of(context)!.searcheForecastDevice),
          actions: [buildSpinner(context)],
          backgroundColor: Colors.lightBlue,
          foregroundColor: Colors.white,
        ),
        body: Stack(
          children: [
            buildResult(context),
            showVersion(context),
          ]
        ),
        floatingActionButton: buildScanButton(context),
      ),
    );
  }
}

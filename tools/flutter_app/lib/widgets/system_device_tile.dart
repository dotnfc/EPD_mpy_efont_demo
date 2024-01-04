import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_blue_plus_windows/flutter_blue_plus_windows.dart';

class ScannedDeviceTile extends StatefulWidget {
  final BluetoothDevice device;
  final VoidCallback onOpen;
  final VoidCallback onConnect;

  const ScannedDeviceTile({
    required this.device,
    required this.onOpen,
    required this.onConnect,
    super.key,
  });

  @override
  State<ScannedDeviceTile> createState() => _ScannedDeviceTileState();
}

class _ScannedDeviceTileState extends State<ScannedDeviceTile> {
  BluetoothConnectionState _connectionState = BluetoothConnectionState.disconnected;

  late StreamSubscription<BluetoothConnectionState> _connectionStateSubscription;

  @override
  void initState() {
    super.initState();

    _connectionStateSubscription = widget.device.connectionState.listen((state) {
      _connectionState = state;
      if (mounted) {
        setState(() {});
      }
    });
  }

  @override
  void dispose() {
    _connectionStateSubscription.cancel();
    super.dispose();
  }

  bool get isConnected {
    return _connectionState == BluetoothConnectionState.connected;
  }

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(widget.device.platformName),
      subtitle: Text(widget.device.remoteId.toString()),
      trailing: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.blue,
          foregroundColor: Colors.white,
          shadowColor: Colors.blueAccent,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(5.0),
          ),
        ),
        onPressed: isConnected ? widget.onOpen : widget.onConnect,
        child: isConnected ? const Text('打开') : const Text('连接'),
      ),
    );
  }
}

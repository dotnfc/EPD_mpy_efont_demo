// SPDX-License-Identifier: MIT License
//

import 'dart:async';

import 'package:eforecast/utils/constants.dart';
import 'package:eforecast/utils/snackbar.dart';
import 'package:flutter/material.dart';
import 'package:flutter_blue_plus_windows/flutter_blue_plus_windows.dart';

const int BLE_CMD_RESET = 0x10;     // 复位设备
const int BLE_CMD_LIST_WIFI = 0x11; // 列举 WIFI 热点
const int BLE_CMD_CONFIG = 0x12;    // 获取/设置 配置
const int BLE_CMD_DEV_INFO = 0x15;  // 获取设备信息
const int BLE_CMD_DEV_TEST = 0x16;  // 测试连接功能

const int BLE_CMD_DEV_TEST_WIFI = 1;  // {"ssid": "xxx", "password": "zzz"}
const int BLE_CMD_DEV_TEST_QWSVC = 2; // {"key": "xxx", "city": "zzz"}

class BleTransmit {
  int? _mtuSize;
  
  late List<int> _responseValue;
  late int _responseLength;
  late int _responseSeq;
  late Completer<void>? _completer;
  late BluetoothCharacteristic? _nusDeviceCharRx;
  late int _defaultTimeoutMs;

  void init(BuildContext context) {
    _completer = null;
    _nusDeviceCharRx = null;
    _mtuSize = 23;
    _defaultTimeoutMs = 2000;

    _responseSeq = 0;
    _responseLength = 0;
    _responseValue = [];
  }

  void reset() {
    _responseSeq = 0;
    _responseLength = 0;
    _responseValue = [];
  }

  void setRxChar(BluetoothCharacteristic characteristic) {
    _nusDeviceCharRx = characteristic;
  }

  void setMtu(int mtu) {
    if (mtu > 0) {
      _mtuSize = mtu;
    }
  }

  void setTimeout(int timeout) {
    _defaultTimeoutMs = timeout;
  }

  // send command apdu to the device
  Future<bool> send(List<int> apduHead, List<int>? apduData) async {
    int seq = -1;
    List<int> frame = [0x00, 0x00];
    reset();

    _completer = Completer<void>();
    _responseValue.clear();
    _responseLength = 0;

    int tlen = 5 + (apduData?.length ?? 0);
    frame[0] = (tlen & 0xff00) >> 8;
    frame[1] = (tlen & 0xff);
    frame.addAll(apduHead);
    if (apduData != null) {
      frame.addAll(apduData);
    }

    final chunkSize = _mtuSize! - 3;
    final blockSize = chunkSize - 1;
    for (var i = 0; i < frame.length; i += blockSize) {
      final chunk = frame.sublist(i, (i + blockSize > frame.length) ? frame.length : i + blockSize);
      List<int> chunkBuf = [];
      if (seq < 0) {
        chunkBuf.add(FRAME_MSG);
        chunkBuf.addAll(chunk);
        seq = 0;
      } else {
        chunkBuf.add(seq);
        chunkBuf.addAll(chunk);
        seq = seq + 1;
        if (seq > 0x80) {
          seq = 0;
        }
        // make esp32-ble to take a breath
        await Future.delayed(const Duration(milliseconds: 100));
      }

      try {
        debugPrint("-> $chunkBuf");
        await _nusDeviceCharRx?.write(chunkBuf, timeout: 1);
      } catch (e) {
        debugPrint('ble send failed: $e.message');
        return false;
      }
    }
    return true;
  }

  // get notified message from device
  void recvBlock(List<int> data) {
    if (data.isEmpty) {
      return;
    }
    if (_responseValue.isEmpty) {
      // first frame
      if ((data[0] == FRAME_PING) || (data[0] == FRAME_KEEP_ALIVE) || (data[0] == FRAME_ERROR)) {
        return; // drop this invalid state frame
      }
      if (_responseLength == 0) {
        if(data[0] == FRAME_MSG) {
          debugPrint('<- $data');
          _responseSeq = 0;
          _responseValue.addAll(data.sublist(3));
          _responseLength = (data[1] << 8) + data[2];
        }
        else {
          return; // drop invalid frame
        }
      }
    } else {
      if (data[0] != _responseSeq) {
        // seq is invalid, drop this frame
        return;
      }
      debugPrint('<- $data');
      _responseValue.addAll(data.sublist(1)); // exluding seq
      _responseSeq ++;
    }

    if (_responseLength <= _responseValue.length) {
      // String strResponse = _responseValue.map((int value) => value.toRadixString(16).padLeft(2, '0')).join();
      if (_completer != null && !_completer!.isCompleted) {
        _completer!.complete();
      } 
    }
  }

  Future<void> transceive(int cla, int ins, int p1, int p2, List<int>? apduData) async {

    List<int> apduHead = [cla, ins, p1, p2, apduData?.length ?? 0];

    send(apduHead, apduData);

    return _completer?.future;
  }

  int getRApduSW() {
    if (_responseLength >= 2) {
      int offset = _responseValue.length - 2;
      return (_responseValue[offset + 0] << 8) + _responseValue[offset + 1];
    }
    else {
      return 0x6F00;
    }
  }

  List<int> getRApduData() {
    if (_responseLength >= 2) {
      return _responseValue.sublist(0, _responseValue.length - 2);
    }
    else {
      return [];
    }
  }

  void cmdReset() {
    transceive(0, BLE_CMD_RESET, 0, 0, null)
      .whenComplete(() {
        if (getRApduSW() == 0x9000) {
          Snackbar.show(ABC.c, "设备已重启", success: true);
        }
        else {
          String strSW = '0x${getRApduSW().toRadixString(16).toUpperCase()}';
          Snackbar.show(ABC.c, "设备重启失败: $strSW", success: false);
        }
      })
      .onError((error, stackTrace) {
        Snackbar.show(ABC.c, prettyException("设备重启失败:", error), success: false);
        debugPrint(error.toString());
      })
      .timeout(Duration(milliseconds: _defaultTimeoutMs), onTimeout: (){
        Snackbar.show(ABC.c, "设备未响应", success: false);
        debugPrint("reset timeout");
      });
  }
}

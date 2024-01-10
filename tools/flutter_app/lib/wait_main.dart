import 'dart:async';
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  bool _isLoading = false;

  // 模拟耗时操作
  Future<void> _performTimeConsumingOperation() async {
    await Future.delayed(Duration(seconds: 5)); // 模拟耗时操作，5秒钟
  }

  // 显示加载动画并执行耗时操作
  void _handleButtonPress() {
    setState(() {
      _isLoading = true;
    });

    Future<void> future = _performTimeConsumingOperation();

    future.timeout(Duration(seconds: 3), onTimeout: () {
      // 超时处理
      setState(() {
        _isLoading = false;
      });

      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: Text("超时"),
          content: Text("设备未响应，请检查网络连接。"),
          actions: <Widget>[
            ElevatedButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: Text("确定"),
            ),
          ],
        ),
      );
    }).whenComplete(() {
      // 完成后关闭加载动画
      setState(() {
        _isLoading = false;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Flutter 等待动画"),
      ),
      body: Center(
        child: _isLoading
            ? CircularProgressIndicator()
            : ElevatedButton(
                onPressed: _handleButtonPress,
                child: Text("执行操作"),
              ),
      ),
    );
  }
}
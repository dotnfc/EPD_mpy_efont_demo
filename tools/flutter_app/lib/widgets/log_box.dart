import 'package:flutter/material.dart';

class LogDisplayWidget extends StatefulWidget {
  const LogDisplayWidget({Key? key}) : super(key: key);

  @override
  State<LogDisplayWidget> createState() => _LogDisplayWidgetState();
}

class _LogDisplayWidgetState extends State<LogDisplayWidget> {
  // 用于存储日志的列表
  List<String> logList = [];

  // 控制文本框滚动
  final ScrollController _scrollController = ScrollController();

  // 添加日志的方法
  void _addLog(String log) {
    setState(() {
      logList.add(log);
    });

    // 滚动到最底部
    _scrollController.animateTo(
      _scrollController.position.maxScrollExtent,
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeOut,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // 主要内容
        Expanded(
          child: ListView.builder(
            controller: _scrollController,
            itemCount: logList.length,
            itemBuilder: (context, index) {
              return ListTile(
                title: Text(logList[index]),
              );
            },
          ),
        ),

        // 输入框和按钮
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            children: [
              Expanded(
                child: TextField(
                  onChanged: (text) {
                    // 这里可以添加一些逻辑处理
                  },
                  decoration: const InputDecoration(
                    hintText: '输入日志',
                  ),
                ),
              ),
              const SizedBox(width: 8.0),
              ElevatedButton(
                onPressed: () {
                  // 添加日志
                  _addLog("用户输入: ${logList.length + 1}");
                },
                child: const Text('添加日志'),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

import 'package:flutter/material.dart';

/// PageView 页面
class PageViewDevice extends StatefulWidget {
  const PageViewDevice({Key? key}) : super(key: key);

  @override
  State<PageViewDevice> createState() => _PageViewDeviceState();
}

class _PageViewDeviceState extends State<PageViewDevice> {
  int currentIndex = 0;

  late List<Widget> children;

  late PageController _pageController;

  @override
  void initState() {
    super.initState();
    children = [
      const PageDeviceConnect(),
      const PageDeviceHome(),
      const PageDeviceInfo(),
      const PageAboutApp(),
    ];

    _pageController = PageController(initialPage: 0);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Test'),
      ),
      
      body: GestureDetector(
        onHorizontalDragEnd: (DragEndDetails details) {
          if (details.primaryVelocity! > 0) {
            // Swiped to the right
            if (_pageController.page! > 0) {
              _pageController.previousPage(
                duration: const Duration(milliseconds: 300),
                curve: Curves.easeInOut,
              );
            }
          } else if (details.primaryVelocity! < 0) {
            // Swiped to the left
            if (_pageController.page! < 2) {
              _pageController.nextPage(
                duration: const Duration(milliseconds: 300),
                curve: Curves.easeInOut,
              );
            }
          }
        },
        child: PageView(
          scrollDirection: Axis.horizontal,
          controller: _pageController,
          onPageChanged: onPageChanged,
          children: children,
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: currentIndex,
        items: List.generate(
          children.length,
          (index) => BottomNavigationBarItem(
              icon: children[index].icon,
              label: children[index].label,
          ),
        ),
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: '首页',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.message_rounded),
            label: '消息',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.people),
            label: '我的',
          ),
        ],
        onTap: (value) {
          currentIndex = value;
          setState(() {});
          _pageController.animateToPage(
            currentIndex,
            duration: const Duration(milliseconds: 300),
            curve: Curves.easeIn,
          );
        },
      ),
    );
  }

  void onPageChanged(int value) {
    currentIndex = value;
    setState(() {});
  }
}

# eForecast

A Flutter project for the eForecast to config the
hardware via BLE.

## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.

## Development Resource
 - [Material, Symbols Icons](https://fonts.google.com/icons)
 - [Material Colors](https://api.flutter.dev/flutter/material/Colors-class.html)
 - [BLE: Nordic Uart Service](https://developer.nordicsemi.com/nRF_Connect_SDK/doc/latest/nrf/libraries/bluetooth_services/services/nus.html)
 - [Flutter Widgets Gallery](https://gallery.flutter.cn/)
 - [Flutter: search_autocomplete](https://pub.dev/packages/search_autocomplete)

## Build Tips
- [编译环境搭建](https://flutter.cn/docs/get-started/install)

  建议将下面两个变量作为环境变量
  ```shell
  set FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
  set PUB_HOSTED_URL=https://pub.flutter-io.cn
  ```
- 解决安卓编译 Gradle 构建的问题

  Exception in thread "main" java.net.ConnectException: Connection timed out: connect'


```shell
#
# %USER_HOME%\.gradle\gradle.properties
#

# HTTP代理配置
systemProp.http.proxyHost=127.0.0.1
systemProp.http.proxyPort=58309
systemProp.http.nonProxyHosts=localhost|127.*.*

# HTTPS代理配置
systemProp.https.proxyHost=127.0.0.1
systemProp.https.proxyPort=58309
systemProp.https.nonProxyHosts=localhost|127.*.*

# SOCKS代理配置（如果需要）
#systemProp.socks.proxyHost=socks-proxy.example.com
#systemProp.socks.proxyPort=1080

# 配置阿里云Maven中心仓库
systemProp.maven.repo.url=https://maven.aliyun.com/repository/public

# 如果要替换Google Maven仓库，可以添加如下配置：
systemProp.maven.google.repo=https://maven.aliyun.com/repository/google

# 对于Gradle插件仓库（如果需要）
systemProp.gradle.plugin.repo=https://maven.aliyun.com/repository/gradle-plugin


```

<hr>

*.NFC 2024/01/01*

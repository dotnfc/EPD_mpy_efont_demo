// https://github.com/BytesZero/flutter_widgets/blob/master/lib/extension/image_extension.dart
//

// 扩展 String 类型
extension ImageLoad on String {
  /// 获取图片全路径
  String get img => 'assets/images/$this';

  /// 获取 icon 全路径
  String get icon => 'assets/icons/$this';
}

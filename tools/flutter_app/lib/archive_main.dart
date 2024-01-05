import 'dart:io';
import 'dart:typed_data';
import 'package:archive/archive.dart';
import 'package:flutter/material.dart';

void testGZip(InputStream input) {
  
  final compressed = GZipEncoder().encode(input);
  
  debugPrint("compressed $compressed\n");

  final decompressed = GZipDecoder().decodeBytes(compressed!, verify: true);
  debugPrint("decompressed $decompressed\n");
}

// void testZLib(InputStream input) {
  
//   final compressed = ZLibEncoder().encode(input);
  
//   debugPrint("compressed $compressed\n");

//   final decompressed = ZLibDecoder().decodeBytes(compressed!, verify: true);
//   debugPrint("decompressed $decompressed\n");
// }

void testRaw(List<int> data) {
    // compress
    List<int> inflatedDataString = Deflate(data, level: Deflate.BEST_COMPRESSION).getBytes();
    debugPrint("compress $inflatedDataString\n");

    // decompressed
    List<int> inflatedDataBytes = Inflate(inflatedDataString).getBytes();
    debugPrint("decompressed $inflatedDataBytes\n");

    // decompressed2
    inflatedDataString = [203, 72, 205, 201, 201, 87, 40, 207, 47, 202, 73, 81, 64, 102, 3, 0]; // inflatedDataString.sublist(0, inflatedDataString.length - 2);
    
    List<int> inflatedDataBytes2 = Inflate(inflatedDataString).getBytes();
    debugPrint("decompressed $inflatedDataBytes2\n");

    Uint8List bytes = Uint8List.fromList(inflatedDataBytes2);
    String string = String.fromCharCodes(bytes);
    debugPrint(string);
}

void main() {
  String inputString = "hello world hello world ";

  Uint8List uint8List = Uint8List.fromList(inputString.codeUnits);

  final InputStream input = InputStream(uint8List);
  // testZLib(input);
  // testGZip(input);
  testRaw(inputString.codeUnits);
}

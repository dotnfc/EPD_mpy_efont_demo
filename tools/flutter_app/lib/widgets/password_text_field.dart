// SPDX-License-Identifier: MIT License
//

import 'package:flutter/material.dart';

class PasswordTextField extends StatefulWidget {
  final String labelText;
  final String hintText;
  final Icon icon;
  final TextEditingController controller;

  const PasswordTextField({
    super.key,
    required this.controller,
    required this.icon, 
    required this.hintText, 
    required this.labelText
  });

  @override
  State<PasswordTextField> createState() => _PasswordTextFieldState();
}

class _PasswordTextFieldState extends State<PasswordTextField> {
  bool _obscureText = true;

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: widget.controller,
      obscureText: _obscureText, // 密码风格
      decoration: InputDecoration(
        hintText: widget.hintText,
        labelText: widget.labelText,
        icon: widget.icon,
        suffixIcon: IconButton(
          icon: Icon(
            _obscureText ? Icons.visibility : Icons.visibility_off,
          ),
          onPressed: () {
            setState(() {
              _obscureText = !_obscureText; // 切换明文和密文
            });
          },
        ),
      ),
    );
  }
}


# EFont Demo

## 目录

- [EFont Demo](#efont-demo)
  - [目录](#目录)
  - [关于此工程](#关于此工程)
  - [快速使用](#快速使用)
  - [VSCode 中编辑代码](#vscode-中编辑代码)
  - [页面展示](#页面展示)
  - [参考](#参考)
  

## 关于此工程
此工程包含的是 EPD_mpy_efont 的几个有用的实例。可以在 micropython 的模拟器以及 ESP32-S3 的硬件上测试使用。

[参考](#参考) 中给出了此工程所参考的相关资源。

## 快速使用
在 tools/win-cygwin 中提供了一个 micropython.exe 供 Windows 用户在 Windows 平台上快速预览 Demo。对于 unix，可以直接编译 [EPD_mpy_efont](https://github.com/dotnfc/EPD_mpy_efont/blob/main/docs/build_CN.md) 的 Unix Port。

比如修改了 10.2 寸三色屏的 Demo，开一个控制台 CTRL+` 在命令行中执行如下命令即可立即预览修改结果: 
> tools\win-cygwin\efore-demo.cmd

如需放到 ESP32-S3 开发板上去运行，那就可以
- 使用 [thonny](https://thonny.org/)
- 将 code 打包为 vfs，然后使用工具下载到目标板上
  
打包 vfs，可以[参考这个方法](https://github.com/dotnfc/EPD_mpy_efont/blob/main/README_CN.md#4-%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F)。下载的方法比较多，这里有一个 mpy_efont_tool (位于 .\tools\esp32_tool\mpy_efont_tool.py)，运行时需要脱离 mpy stubs 的 venv，并在 python 中安装其依赖包:
> EPD_mpy_efont_demo\tools\esp32_tool> pip install -r requirements txt 

<img src="image/efont-tool.jpg" />

## VSCode 中编辑代码
首先需要安装 python 相关扩展，以及 'MicroPython stubs'，并建立 venv，请参考 [Using the MicroPython stubs](https://micropython-stubs.readthedocs.io/en/main/20_using.html).

仓库中已经携带了 mpy stubs 的配置，见 .vscode/settings.json

对于 efont 的特定 stub，存放于 .efont 目录中。

## 页面展示

<img src="image/ex10d2.jpg" />

## 参考

 - [weather-icons](https://erikflowers.github.io/weather-icons/)
 - [esp32-weather-epd](https://github.com/lmarzen/esp32-weather-epd/tree/main)
 - [icomoon](https://icomoon.io/app/)
 - [MicroPython Online DOC](https://docs.micropython.org/en/latest/index.html)
 - [micropython-lib](https://github.com/micropython/micropython-lib)
 - [pycopy-lib](https://github.com/pfalcon/pycopy-lib)
 - [Chinese zodiac sign icons] By StevyG


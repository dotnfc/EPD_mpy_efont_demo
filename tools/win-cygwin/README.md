## Micropython TTF JPG PNG 扩展库

这个 efont 扩展，仓库在 https://github.com/dotnfc/EPD_mpy_efont，此压缩包是使用 cygwin 环境编译的 unix port，演示了

- efont-demo-2c.cmd
黑白 4.2 寸的联网显示天气的功能

- efont-demo-3c.cmd 
黑白红 10.2 寸的中英文显示，ttf 图标 显示的功能

- efont-demo-day.cmd 
黑白红 10.2 寸的中英文显示农历、阳历的信息，以及一条文心一言

上述批处理，双击运行即可，里面已经配置了路径、环境及执行特定脚本。

## 调用流程描述

> main_demo.py > display.py > panel/*.py


> main_demo_3c.py > display3c.py > panel/*.py


其中 display*.py 配置了要使用的 panel 目录下的 epd/sdl 驱动脚本，且为便于脚本编写，封装了图片显示，多字体管理使用。

对于 esp32 平台，spi, gpio 的配置，则位于 lib/board.py

挺简单的演示，欢迎交流。

<hr />
*.nfc 2023/09/28*
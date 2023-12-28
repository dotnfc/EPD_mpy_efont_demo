@echo off
REM
REM https://github.com/labplus-cn/mkfatfs/releases/download/v2.0.1/mkfatfs.rar
REM

mkfatfs -c ../../code -t fatfs -s 4194304 efont_demo_esp32s3_vfs.bin 

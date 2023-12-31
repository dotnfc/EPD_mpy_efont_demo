#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
将原始网页数据，转为固件所用的文件，主要是 gz 方式压缩，节省空间
by .NFC 2023/07/24
'''

import os
import shutil
import gzip
from htmlmin import minify


#----------------------------------------------------------------
# 设置当前目录为脚本文件所在目录
def setCWD():
  # 获取脚本所在目录的绝对路径
  script_path = os.path.abspath(__file__)
  script_directory = os.path.dirname(script_path)

  # 切换当前工作目录
  os.chdir(script_directory)

#----------------------------------------------------------------
# 压缩后，递归复制 js, css 文件
def compress_js_css_recursive(source_dir, destination_dir):
  # 获取源目录下的所有子文件和目录
  entries = os.listdir(source_dir)

  # 创建目标目录（如果不存在）
  if not os.path.exists(destination_dir):
      os.makedirs(destination_dir)

  for entry in entries:
      source_path = os.path.join(source_dir, entry)
      dest_path = os.path.join(destination_dir, entry)

      if os.path.isdir(source_path):
          # 如果是目录，则递归处理子目录
          compress_js_css_recursive(source_path, dest_path)
      elif entry.endswith('.js') or entry.endswith('.css') or entry.endswith('.woff2'):
          # 如果是 .js 或 .css 文件，则进行压缩处理
          with open(source_path, 'rb') as f_in:
              with gzip.open(dest_path + '.gz', 'wb') as f_out:
                  shutil.copyfileobj(f_in, f_out)

#----------------------------------------------------------------
# 压缩并复制 index.html
def copy_index_html_file(source_dir, destination_dir):
  input_file = source_dir + os.sep + "index.html"
  output_file = destination_dir + os.sep + "index.html"

  # print(r"Copying index.html {} to {}".format(input_file, output_file))
  try:
      with open(input_file, 'r', encoding='utf-8') as file:
          html_content = file.read()

      # 使用 htmlmin 库进行压缩
      compressed_html = minify(html_content, remove_empty_space=True)

      # 将压缩后的内容写入输出文件
      with open(output_file, 'w', encoding='utf-8') as file:
          file.write(compressed_html)

      print(" - HTML 文件压缩成功！")
  except Exception as e:
      print("压缩失败：", str(e))

#----------------------------------------------------------------
# 复制常规文件
def copy_file(file_name, source_dir, destination_dir):
    source_file = source_dir + os.sep + file_name
    destination_file = destination_dir + os.sep + file_name
    
    try:
        # 使用 shutil 的 copy2 函数复制文件
        shutil.copy2(source_file, destination_file)
        print(f" - 文件复制成功！从 {source_file} 到 {destination_file}")
    except FileNotFoundError:
        print(" [err] 找不到指定的源文件。")
    except shutil.SameFileError:
        print(" [err] 源文件和目标文件路径相同，无需复制。")
    except Exception as e:
        print(" [err] 复制文件时出现错误：", str(e))
        
if __name__ == "__main__":
  setCWD()
  source_dir = "code"  # 指定 原始目录 目录
  destination_dir = "littlefs"  # 指定 目标 目录

  if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)
    
  compress_js_css_recursive(source_dir, destination_dir)
  print(" - 资源文件压缩复制完成")
  
  copy_index_html_file(source_dir, destination_dir)

  copy_file("config.json", source_dir, destination_dir)
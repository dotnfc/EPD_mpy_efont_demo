#-*- coding:utf-8 -*-
#----------------------------------------------------------------
#
# logger for epd driver
#
# by dotnfc, 2023/09/22
#

def dprint(*args, **kwargs):
    should_print = False

    if should_print:
        print(*args, **kwargs)

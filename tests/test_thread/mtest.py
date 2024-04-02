#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：myThread 
@File    ：test.py
@IDE     ：PyCharm 
@Author  ：大雄
@Date    ：2023/11/11 13:19 
"""
import time

from src.utils.ThreadUtils import SuperThread


def test():
    for i in range(20):
        time.sleep(0.1)
        print("test", i)


def test2():
    for i in range(20):
        time.sleep(0.1)
        print("test2", i)


def callf():
    print("回调了")


if __name__ == '__main__':
    t = SuperThread(target=test, callback_func=callf)
    t.start()
    time.sleep(1)

    t.cease()
    # input()

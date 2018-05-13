# -*- coding: utf-8 -*-

import datetime
import sys
import time
import random
from threading import Thread

from AndroidBase import AndroidBase
from DouYinBase import DouYinBase, DouYinU2

# 打印日志


def LogPrint(text):
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
    mystr = otherStyleTime + "  " + text
    print(mystr)


class Main_Test():
    def __init__(self):
        # self.myAndroid = AndroidBase()
        self.myDouyin = DouYinU2()
        self.myDouyin.ip = "192.168.1.120"

    def Run(self):
        self.myDouyin.android.LoadParameters("configure.ini")
        self.myDouyin.ConnectPhone()
        self.myDouyin.StartDouyin(10)
        # self.myDouyin.client.click(400, 300)

        while(True):
            # 暂时视频播放
            LogPrint(u"暂时视频")
            self.myDouyin.client.click(500, 500)
            # 点赞
            LogPrint(u"点赞")
            self.myDouyin.AwesomeMe()
            # 加好友
            LogPrint(u"加好友")
            self.myDouyin.AddFriend()
            # 发消息
            # LogPrint(u"发消息")
            # self.myDouyin.SendMsgXY(u"互粉，谢谢^_^")
            # 暂时视频播放
            #self.myDouyin.client.click(500, 500)
            # LogPrint(u"评论")
            # self.myDouyin.Comment("666")
            # 下一个
            LogPrint(u"下一个")
            self.myDouyin.client.swipe(0.5, 0.8, 0.5, 0.2, 0.1)
            LogPrint(u"看几秒视频")
            time.sleep(random.randint(10, 20))


if __name__ == '__main__':
    test = Main_Test()
    test.Run()

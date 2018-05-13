# -*- coding: utf-8 -*-

import time
import random
import string
from AndroidCtrl import AndroidCtrl
from DouYinCtrl import DouYinCtrl


#client = AndroidCtrl()
douyin = DouYinCtrl()

#print (client.RandomStr(4))

douyin.android.ui2_ConnectDevice()
douyin.SomeAdv()

def Test():
    client.ui2_ConnectDevice()
    #client.ui2_ConnectDeviceWiFi("192.168.1.118")

    #print (client.client.info)

    client.client.app_stop(client.APP_DOUYIN)
    client.client.app_start(client.APP_DOUYIN)

    time.sleep(10)

    if client.client(text="我").exists:
        print("我")

    if client.client(text="消息").exists:
        print("消息")

    if client.client(text="广告").exists:
        print("广告")

    if client.client(text="立即下载").exists:
        print("立即下载")

    if client.client(text="抖音号").exists:
        print("抖音号")

    if client.client(text="作品").exists:
        print("作品")

    if client.client(text="喜欢").exists:
        print("喜欢")

    if client.client(text="已关注").exists:
        print("已关注")
    elif client.client(text="关注").exists:
        print("未关注")

    # client.adb_PullScreenShot()
    # print (client.adb_CompareOne("yiguan.png"))
    # print (client.adb_CompareOne("jia.png"))
    # print (client.adb_CompareTwo("guan.png", "jia.png"))

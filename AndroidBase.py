# -*- coding: utf-8 -*-
"""@package AndroidBase
Basic Class for Android Controlling
"""
import datetime
import sys
import os
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
import subprocess
import pymysql
import configparser
import codecs
import uiautomator2 as u2

class AndroidBase():
    """
    AndroidBase基础库
    """
    # 初始化
    def __init__(self):
        pass

        # 读取参数
        self.LoadParameters("configure.ini")
        # 连接设备
        if self.ConnectPhone():
            # 获取当前屏蔽分辨率
            self.res = self.GetWindowSize()
        else:
            self.res = "800x600"

    # 读取参数
    def LoadParameters(self, file):

        # 参数文件读取
        self.cfg = configparser.ConfigParser()
        self.cfg.read(file, encoding="utf-8")

        # 序列号
        self.license = self.cfg.get("parameters", "license")

        # 自动操作内容
        self.auto_addfriend = self.cfg.get("parameters", "auto_addfriend")
        self.auto_awesome = self.cfg.get("parameters", "auto_awesome")
        self.auto_comment = self.cfg.get("parameters", "auto_comment")
        self.auto_message = self.cfg.get("parameters", "auto_message")
        # 自动停止次数
        self.awesome_stop = self.cfg.get("parameters", "awesome_stop")
        self.addfiend_stop = self.cfg.get("parameters", "addfiend_stop")
        self.comment_stop = self.cfg.get("parameters", "comment_stop")
        self.message_stop = self.cfg.get("parameters", "message_stop")
        # 自动评论
        self.comment = self.cfg.get("parameters", "comment")
        # 自动私信
        self.message = self.cfg.get("parameters", "message")
        # 休息时间
        self.ralex_time = self.cfg.get("parameters", "ralex_time")
        # 循环次数
        self.loop = self.cfg.get("parameters", "loop")

    # 初始化设备
    def Init_Device(self):
        cmd = "python -m uiautomator2 init"
        result = self.SendCommand(cmd)
        # TODO check result

    # 连接手机
    def ConnectPhone(self):
        try:
            self.client = u2.connect_usb("127.0.0.1:62001")
            # set delay 1.5s after each UI click and click
            self.client.click_post_delay = 1.0
            # set default element wait timeout (seconds)
            self.client.wait_timeout = 5.0
            return True
        except:
            self.LogPrint(u"手机无法连接，请检查是否未初始化过")
            return False

    # 安装APP
    def InstallAPP(self, appURL):
        self.client.app_install(appURL)

    # 下载抖音
    def DownloadDouyin(self):
        self.OpenURL("http://s.toutiao.com/UsMYE/")

    # 启动APP
    def StartAPP(self, appName):
        self.client.app_start(appName)

    # 关闭APP
    def StopAPP(self, appName):
        self.client.app_stop(appName)

    # 获取当前屏幕分辨率
    def GetWindowSize(self):
        x, y = self.client.window_size()
        if (x == 1080 | y == 1080):
            res = "1920x1080"
        elif (x == 720 | y == 720):
            res = "1280x720"
        elif (x == 600 | y == 600):
            res = "800x600"
        else:
            res = "800x600"
        return res

    # 打开连接并转到抖音
    def OpenDouyinURL(self, url, delaytime):
        self.OpenURL(url)
        self.client(description=u"打开看看").click()
        time.sleep(delaytime)

    # 打印日志
    def LogPrint(self, text):
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
        mystr = otherStyleTime + "  " + text
        print(mystr)

    # 重新定向adb命令
    def SendCommand(self, command):
        result = subprocess.call(command, shell=True)
        return result

    # 延时，时间单位为秒
    def Sleep(self, t):
        time.sleep(t)

    # 上滑屏幕
    def RollingUpScreen(self):
        self.myDouyin.client.swipe(0.5, 0.8, 0.5, 0.2, 0.1)

    # 下滑屏幕
    def RollingDownScreen(self, step):
        self.myDouyin.client.swipe(0.5, 0.2, 0.5, 0.8, 0.1)

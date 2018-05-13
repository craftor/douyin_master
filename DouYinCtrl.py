# -*- coding: utf-8 -*-
import time, urllib
import webbrowser
from AndroidCtrl import AndroidCtrl

class DouYinCtrl():

    # 初始化
    def __init__(self):
        self.android = AndroidCtrl()
        self.res = "800x600"

    # 下载抖音
    def DownloadDouyin(self):
        url = "http://s.toutiao.com/UsMYE/"
        webbrowser.open(url, new=0, autoraise=True)

    # 来点广告
    def SomeAdv(self):
        self.android.adb_OpenURL("http://craftor.org")

    # 安装抖音
    def InstallDouyin(self):
        pass

    def adb_AwesomeMe(self):
        self.android.adb_SingleClick(568, 482)

    # 点赞
    def ui2_AwesomeMe(self):
        self.android.client.click(568, 482)

    def adb_AddFriend(self):
        self.android.adb_SingleClick(568, 422)

    # 加关注
    def ui2_AddFriend(self):
        self.android.client.click(568, 422)

    # 批量保存视频
    def adb_DownVideo(self):
        # 点分享键
        self.android.adb_SingleClick(568, 614)
        time.sleep(1)
        # 保存本地
        self.android.adb_SingleClick(116, 680)
        time.sleep(3)

    def adb_Comment(self, text):
        # 点 评论
        self.android.adb_SingleClick(568, 548)
        # 点 聊天框
        self.android.adb_SingleClick(296, 780)
        # 输入内容
        self.android.client.send_keys(text)
        # 发送
        self.android.adb_SingleClick(581, 714)
        # 返回
        self.android.client.press("back")


    # 评论
    def ui2_Comment(self, text):
        # 点 评论
        self.android.adb_SingleClick(568, 548)
        time.sleep(1)
        # 点 聊天框
        self.android.adb_SingleClick(296, 780)
        # 输入内容
        self.android.client.send_keys(text)
        time.sleep(1)
        # 发送
        self.android.adb_SingleClick(581, 714)
        time.sleep(1)
        # 返回
        self.android.adb_SingleClick(300, 200)
        time.sleep(1)
        self.android.adb_SingleClick(300, 200)


    # 发消息
    def SendMsg(self, text):
        # 先点头像
        self.android.client.click(568, 394)
        time.sleep(1)
        # 点 发消息
        self.android.client.click(477, 110)
        time.sleep(1)
        # 点两下，以防上一步没有加关注
        self.android.client.click(477, 110)
        time.sleep(1)
        # 点 聊天框
        self.android.client.click(300, 777)
        time.sleep(1)
        # 输入内容
        self.android.client.send_keys(text)
        time.sleep(1)
        # 发送
        self.android.client.click(581, 714)
        time.sleep(2)
        # 返回3次
        self.android.client.click(19, 46)
        time.sleep(1)
        self.android.client.click(19, 46)
        time.sleep(1)

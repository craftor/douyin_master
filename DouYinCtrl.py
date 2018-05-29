# -*- coding: utf-8 -*-
import time
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

    def adb_AwesomeMe(self, device):
        self.android.adb_SingleClick(568, 482, device)

    def adb_AddFriend(self, device):
        self.android.adb_SingleClick(568, 422, device)

    # 批量保存视频
    def adb_DownVideo(self, device):
        self.android.adb_SingleClick(568, 614, device)  # 点分享键
        self.android.adb_SingleClick(116, 680, device)  # 保存本地
        time.sleep(3)

    # 发私信
    def adb_Message(self, text, device):
        self.android.adb_SingleClick(460, 119, device)  # 点 发消息
        self.android.adb_SingleClick(296, 780, device)  # 点 聊天框
        self.android.client.send_keys(text)             # 输入内容
        self.android.adb_SingleClick(581, 736, device)  # 发送
        self.android.client.click(19, 46, device)       # 返回
        time.sleep(1)

    # 发评论
    def adb_Comment(self, text, device):
        self.android.adb_SingleClick(570, 545, device)  # 点评论按钮
        self.android.adb_SingleClick(290, 777, device)  # 点评论框
        self.android.client.send_keys(text)             # 输入内容
        self.android.adb_SingleClick(581, 736, device)  # 点发送
        self.android.adb_SingleClick(280, 150, device)  # 空白处点一下，关闭评论框

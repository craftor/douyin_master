# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore

from Ui_main import Ui_Dialog
import sys
import datetime
import time
from threading import Thread
import random
import webbrowser
import urllib.request
import markdown

from DouYinCtrl import DouYinCtrl


class Dialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None):

        super(Dialog, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowMinimizeButtonHint)
        self.setupUi(self)

        #qss_file = open('psblack.css').read()
        #self.setStyleSheet(qss_file)

        # 在线检测
        self.ServerIP = "http://yinliu.craftor.org:5000"
        self.Online = False

        # 获取新闻
        # self.GetNews()

        # license有效标识
        self.LicenseAvaliabie = False
        # 线程
        self.tRun = False
        # 例化实例
        self.douyin = DouYinCtrl()
        # 参数初始化
        self.DefaultSetting()
        # 检查序列号
        self.CheckKey()
        # 计数器
        self.cnt = 0
        self.total = 0
        # 刷新设备列表
        self.RefreshDevcies()

        # self.pushButton_BuyKeys.setDisabled(True)

        # 定时检测服务器是否在线
        # self.timer = QTimer(self)  # 初始化一个定时器
        # self.timer.timeout.connect(self.CheckOnline)  # 计时结束调用operate()方法
        # self.timer.start(180000)  # 设置计时间隔并启动

        # 随便显示个在线人数
        # self.people = random.randint(10000, 20000)
        # self.label_OnlinePeople.setText(str(self.people))

        # For Test
        self.Test()

    def RefreshDevcies(self):
        devices = self.douyin.android.GetDeviceList()
        if devices is None:
            self.LogPrint("没有发现模拟器")
        else:
            self.LogPrint("【发现" + str(len(devices)) + "个模拟器】")
            # print(len(devices))
            if (len(devices) > 1):
                self.checkBox_EnableMultiDevices.setDisabled(False)
            else:
                self.checkBox_EnableMultiDevices.setDisabled(True)

            for i in range(len(devices)):
                # print(devices)
                self.comboBox_DeviceList.addItem(str(devices[i]))

    def Test(self):
        # cmd = "adb shell dumpsys package com.ss.android.ugc.aweme"
        # # result = self.douyin.android.SendCommand(cmd)
        # result = os.system(cmd)
        # #print (result)
        # print ((result).find('versionName'))
        self.douyin.android.GetDeviceList()

    def GetNews(self):
        url = "http://app.craftor.org/douyin.txt"
        # url = "https://douyin.craftor.org/2018/05/22/Latest_Version/"
        req = urllib.request.urlopen(url)
        res = req.read()
        news = str(res, encoding="utf8")
        # self.textEdit_News.setHtml(news)
        # input_file = codecs.open(res, mode="r", encoding="utf-8")
        # text = input_file.read()
        html = markdown.markdown(news)
        self.textEdit_News.setHtml(html)

    def CheckOnline(self):
        macaddr = self.douyin.android.GetMac()
        url = self.ServerIP + "/online/" + self.douyin.android.license + "/" + \
            macaddr + "/" + self.douyin.android.phone
        try:
            req = urllib.request.urlopen(url)
            res = req.read()
            if res == b"OK":
                print("【服务器在线】")
                self.Online = True
            else:
                self.Online = False
                print("序列号异常！")
            # print (str(res))
            # TODO, 显示在线人数
            # cnt = random.randint(-20, 20)
            # self.people = self.people + cnt
            # self.label_OnlinePeople.setText(str(self.people))
        except Exception:
            self.Online = False
            self.LogPrint(u"服务器无法连接！")
            # self.label_Oneline.setText("无法连接服务器！")

    # 初始化
    def DefaultSetting(self):
        self.LogPrint(u"参数初始化")
        self.comboBox_WatchTime.setCurrentIndex(1)
        self.checkBox_RestartDouyin.setChecked(True)
        self.checkBox_AutoAddFriend.setChecked(False)
        self.checkBox_AutoAwesome.setChecked(False)
        self.checkBox_AutoComment.setChecked(False)
        self.checkBox_DownVideo.setChecked(False)
        self.checkBox_Cnt.setChecked(False)
        # self.textEdit_Comment.setText("666")
        # self.textEdit_Message.setText("互粉，谢谢^_^")
        self.lineEdit_License.setText(self.douyin.android.license)
        self.lineEdit_PhoneNumber.setText(self.douyin.android.phone)
        self.LogPrint(u"初始化完成")

    # 激活Key
    def ActKey(self, license, phone):
        if len(phone) != 11:
            self.LogPrint(u"手机号不正确！激活后手机号不可修改！")
            return
        url = self.ServerIP + "/activate/" + license + "/" + phone
        # print(url)
        try:
            req = urllib.request.urlopen(url)
            res = req.read()
        except Exception:
            self.LicenseAvaliabie = False
            self.LogPrint(u"服务器无法连接！")
            return
        # print (res)
        msg = ''
        if res == b'1':
            msg = u"已激活！"
        elif res == b'-1':
            msg = u"已激活，不要重复点击"
        elif msg == b'0':
            msg = u"激活失败！"
        self.LogPrint(msg)

    # 检查Key有效时间
    def CheckKey(self):
        # 请求服务器
        url = self.ServerIP + "/check/" + self.douyin.android.license
        try:
            req = urllib.request.urlopen(url)
            res = req.read()
            lessTime = int(res)
        except Exception:
            self.LicenseAvaliabie = False
            self.LogPrint(u"服务器无法连接！")
            return

        if (lessTime is not None):
            if lessTime < 0:
                msg = u"未激活，请先激活！"
            elif lessTime == 0:
                msg = u"序列号无效！"
            else:
                msg = u"剩余" + str(lessTime) + u"天"
                self.LicenseAvaliabie = True
            self.label_LicenseAvaliable.setText(msg)
            self.LogPrint(msg)
        else:
            msg = u"无效的序列号！"
            self.label_LicenseAvaliable.setText(msg)
            self.LogPrint(msg)
            self.LicenseAvaliabie = False

    # 点赞
    def AwsomeMe(self, douyin, device):
        if (self.checkBox_AutoAwesome.isChecked()):
            print(str(device) + u"点个赞")
            douyin.adb_AwesomeMe(device)

    # 点击+号，加好友
    def AddFriend(self, douyin, device):
        if self.checkBox_AutoAddFriend.isChecked():
            print(str(device) + u"加关注")
            douyin.android.adb_SingleClick(569, 428, device)

    # 发私信
    def Message(self, douyin, device):
        if self.checkBox_AutoMessage.isChecked():
            strLen = self.comboBox_RandomStrLenMessage.currentIndex() + 4
            str_msg = self.textEdit_Message.toPlainText()
            if self.comboBox_CommentType.currentIndex() == 0:  # 随机评论
                msg = str_msg.split()
                msg_RndCnt = random.randint(0, len(msg) - 1)
                str_msg_single = msg[msg_RndCnt]
            else:
                pass
            if self.checkBox_InsertStrAfterMessage.isChecked():
                str_msg_single += douyin.android.RandomStr(strLen)
            print(str(device) + u"屏幕左滑")
            douyin.android.adb_RollingLeftScreen(device)
            douyin.android.adb_SingleClick(512, 118, device)
            douyin.android.adb_SingleClick(512, 118, device)
            douyin.adb_Message(str_msg_single, device)
            print(str(device) + u"屏幕右滑")
            douyin.android.adb_RollingRightScreen(device)

    # 下载视频
    def DownVideo(self, douyin, device):
        if (self.checkBox_DownVideo.isChecked()):
            print(str(device) + u"保存视频")
            douyin.adb_DownVideo(device)

    # 评论
    def Comment(self, douyin, device):
        if (self.checkBox_AutoComment.isChecked()):
            print(str(device) + u"评论开始")
            # 评论中插入随机字符
            strLen = self.comboBox_RandomStrLenComment.currentIndex() + 4
            str_comment = self.textEdit_Comment.toPlainText()
            if self.comboBox_CommentType.currentIndex() == 0:  # 随机评论
                str_cmt = str_comment.split()
                cmt_RndCnt = random.randint(0, len(str_cmt) - 1)
                str_cmt_single = str_cmt[cmt_RndCnt]
            else:
                pass
            # print (msg_single)
            if self.checkBox_InsertStrAfterComment.isChecked():
                str_cmt_single += douyin.android.RandomStr(strLen)
            douyin.adb_Comment(str_cmt_single, device)
            print(str(device) + u"评论结束")

    # 计数
    def Count(self, device):
        self.cnt = self.cnt + 1
        self.total = self.total + 1
        msg = str(device) + u"【已看：" + str(self.cnt) + "个，累计：" + str(self.total) + "个】"
        # self.label_Counter.setText(msg)
        if (self.checkBox_Cnt.isChecked()):
            self.LogPrint(msg)

    # 随机时间
    def RandomSleep(self, device):
        # 看一会儿视频
        if self.comboBox_WatchTime.currentIndex() == 0:
            cnt = random.randint(0, 5)
        elif self.comboBox_WatchTime.currentIndex() == 1:
            cnt = random.randint(5, 10)
        elif self.comboBox_WatchTime.currentIndex() == 2:
            cnt = random.randint(10, 15)
        else:
            cnt = random.randint(5, 10)
        print(str(device) + u"再看" + str(cnt) + u"秒")
        time.sleep(cnt)

    # 重启抖音
    def RestartDouyin(self, douyin, device):
        # 重新启动抖音
        if (self.checkBox_RestartDouyin.isChecked()):
            print(str(device) + u"正在重新启动抖音")
            try:
                douyin.android.client.app_stop(douyin.android.APP_DOUYIN)
            except Exception:
                print(str(device) + u"关闭抖音失败，请尝试重新【初始化模拟器】")
                return
            time.sleep(2)
            try:
                douyin.android.client.app_start(douyin.android.APP_DOUYIN)
            except Exception:
                print(str(device) + u"关闭抖音失败，请尝试重新【初始化模拟器】")
                return
            time.sleep(10)
            print(str(device) + u"启动完成")

    # 多开使用的线程
    def MultiThread(self, device):

        douyin = DouYinCtrl()  # 实例初始化
        douyin.android.ui2_ConnectDeviceUSB(device)  # 连接设备
        self.RestartDouyin(douyin, device)

        # 工作模式
        if self.comboBox_WorkMode.currentIndex() == 0:
            pass
        elif self.comboBox_WorkMode.currentIndex() == 1:  # 只刷关注用户
            self.LogPrint(u"只刷关注用户模式")
            douyin.android.adb_SingleClick(175, 777, device)
            time.sleep(2)
            douyin.android.adb_SingleClick(140, 366, device)
        elif self.comboBox_WorkMode.currentIndex() == 2:  # 只刷附近人
            self.LogPrint(u"只刷附近用户模式")
            douyin.android.adb_SingleClick(52, 777, device)
            time.sleep(2)
            douyin.android.adb_SingleClick(327, 60, device)
            time.sleep(2)
            douyin.android.adb_SingleClick(136, 237, device)

        while(self.tRun and self.LicenseAvaliabie):

            # 判断是否在抖音界面
            if (douyin.android.client(text="关注").exists):
                pass
            else:
                print(str(device) + "好像不在抖音界面")
                self.RestartDouyin(device)

            # 看5秒钟视频，判断是否为广告
            print(str(device) + "先观察5秒，判断是否为广告")
            time.sleep(5)
            if (douyin.android.client(text="立即下载").exists):
                print(str(device) + u"==========刷到广告了==========")
                time.sleep(1)
            elif (douyin.android.client(text="查看详情").exists):
                print(str(device) + u"==========刷到广告了==========")
                time.sleep(1)
            else:
                self.RandomSleep(device)
                self.AwsomeMe(douyin, device)
                self.AddFriend(douyin, device)
                self.Message(douyin, device)
                self.DownVideo(douyin, device)
                self.Comment(douyin, device)
                self.Count(device)

            # 下一个
            print(str(device) + u"下一个抖音")
            douyin.android.adb_RollingUpScreen(500, device)

    # 打印日志
    def LogPrint(self, text):
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%H:%M:%S")
        mystr = otherStyleTime + "  " + text
        self.textEdit_Print.append(mystr)

    @pyqtSlot()
    def on_pushButton_Run_clicked(self):

        if (self.tRun):

            # self.LogPrint("线程已经开始，不要重复点击")
            # self.pushButton_Run.setText(u"停止中。。。")
            self.tRun = False
            # self.myThread.join()
            self.LogPrint(u"*线程已经停止，等待本次循环结束")
            self.pushButton_Run.setText(u"开始")
            self.comboBox_WorkMode.setDisabled(False)

        else:

            # 检查是否需要自动初始化
            if self.checkBox_AutoInitial.isChecked():
                self.douyin.android.ui2_InitDevice()

            # 选检查Key是否有效
            if self.LicenseAvaliabie is False:
                self.LogPrint(u"序列号无效！")
                return
            else:
                self.LogPrint(u"序列号有效，准备开始")

            self.tRun = True
            self.cnt = 0

            device = self.douyin.android.devices
            for x in range(0, len(device)):
                myThread = "myTh" + str(x)
                myThread = Thread(target=self.MultiThread, args=[device[x]])
                myThread.start()
                self.LogPrint(str(device[x]) + u"线程已经启动")
            self.pushButton_Run.setText(u"停止")

    @pyqtSlot()
    def on_pushButton_InitDevice_clicked(self):
        cmd = "tools init"
        self.douyin.android.SendCommand(cmd)

    @pyqtSlot()
    def on_pushButton_SaveLog_clicked(self):
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y-%m-%d-%H-%M-%S")
        filename = otherStyleTime + ".txt"
        with open(filename, "w") as f:
            f.write(self.textEdit_Print.toPlainText())
        self.LogPrint(u"日志已保存")

    @pyqtSlot()
    def on_pushButton_ClearLog_clicked(self):
        self.textEdit_Print.setText("")

    @pyqtSlot()
    def on_pushButton_StartEmulator_clicked(self):
        self.douyin.android.StartEmulator()

    @pyqtSlot()
    def on_pushButton_EmulatorLocation_clicked(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                         "选取文件",
                                                         "C:/",
                                                         "Exe Files (nox.exe)")
        self.douyin.android.location = fileName
        self.douyin.android.SaveParameters("configure.ini")

    @pyqtSlot()
    def on_pushButton_LicenseCheck_clicked(self):
        self.CheckKey()

    @pyqtSlot()
    def on_textEdit_Comment_textChanged(self):
        self.comment = self.textEdit_Comment.toPlainText()

    @pyqtSlot(str)
    def on_lineEdit_License_textChanged(self, p0):
        self.douyin.android.license = p0

    @pyqtSlot(str)
    def on_lineEdit_PhoneNumber_textChanged(self, p0):
        self.douyin.android.phone = p0

    @pyqtSlot()
    def on_pushButton_BuyKeys_clicked(self):
        # url = "http://www.mhsc1688.com/list/2ypUu"
        url = "http://keys.craftor.org"
        webbrowser.open(url, new=0, autoraise=True)

    @pyqtSlot()
    def on_pushButton_DownloadEmulator_clicked(self):
        url = "https://www.yeshen.com/cn/download/fullPackage"
        webbrowser.open(url, new=0, autoraise=True)

    @pyqtSlot(bool)
    def on_checkBox_DownVideo_clicked(self, checked):
        if checked:
            self.LogPrint(u"【注意下载多了之后要及时清理】")

    @pyqtSlot(bool)
    def on_checkBox_RestartDouyin_clicked(self, checked):
        if checked is False:
            self.LogPrint(u"【请确认抖音已经启动，并在视频播放状态】")

    @pyqtSlot(bool)
    def on_checkBox_AutoAddFriend_clicked(self, checked):
        if checked is False:
            self.checkBox_AutoMessage.setDisabled(True)
            self.checkBox_AutoMessage.setChecked(False)
        else:
            self.checkBox_AutoMessage.setDisabled(False)

    @pyqtSlot()
    def on_pushButton_DownloadDouyin_clicked(self):
        url = "http://s.toutiao.com/UsMYE/"
        webbrowser.open(url, new=0, autoraise=True)
        # self.douyin.android.adb_OpenURL(url)

    @pyqtSlot(int)
    def on_comboBox_WorkMode_currentIndexChanged(self, index):
        if index == 0:
            self.LogPrint(u"【默认模式】")
            self.pushButton_Run.setDisabled(False)
            self.checkBox_AutoAddFriend.setChecked(True)
            self.checkBox_AutoAddFriend.setDisabled(False)
            self.checkBox_RestartDouyin.setChecked(True)
            self.checkBox_RestartDouyin.setDisabled(False)
        elif index == 1:
            self.LogPrint(u"【只刷关注用户模式】-暂时关闭")
            self.pushButton_Run.setDisabled(True)
            self.checkBox_AutoAddFriend.setChecked(False)
            self.checkBox_AutoAddFriend.setDisabled(True)
            self.checkBox_RestartDouyin.setChecked(True)
            self.checkBox_RestartDouyin.setDisabled(True)
        elif index == 2:
            self.LogPrint(u"【只刷附近用户模式】")
            self.pushButton_Run.setDisabled(False)
            self.checkBox_RestartDouyin.setChecked(True)
            self.checkBox_RestartDouyin.setDisabled(True)
        else:
            pass

    @pyqtSlot()
    def on_pushButton_ActKey_clicked(self):
        self.douyin.android.license = self.lineEdit_License.text()
        self.douyin.android.phone = self.lineEdit_PhoneNumber.text()
        self.ActKey(self.douyin.android.license, self.douyin.android.phone)
        # self.CheckKey()
        self.douyin.android.SaveParameters("configure.ini")

    @pyqtSlot()
    def on_pushButton_VisitHome_clicked(self):
        url = "http://douyin.craftor.org"
        webbrowser.open(url, new=0, autoraise=True)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())

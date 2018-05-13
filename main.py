# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui

from Ui_main import Ui_Dialog
import sys
import datetime
import time
from threading import Thread
import random
import webbrowser
import qrcode
import urllib.request
from multiprocessing import Process

from DouYinCtrl import DouYinCtrl

class Dialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None):

        super(Dialog, self).__init__(parent)
        self.setupUi(self)

        # license有效标识
        self.LicenseAvaliabie = False
        # 线程
        self.tRun = False
        # 例化实例
        self.douyin = DouYinCtrl()
        # 参数初始化
        self.LoadSetting()
        # 检查序列号
        self.CheckKey()
        # 计数器
        self.cnt = 0
        self.total = 0

        # For Test
        # self.Test()

    def Test(self):
        # qr = qrcode.QRCode(
        #     version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=4)
        # qr.add_data("http://www.cnblogs.com/sfnz/")
        # qr.make(fit=True)
        # img = qr.make_image()
        img = qrcode.make('http://craftor.org')
        img.save('test.png')
        #img = img.convert("RGBA")
        self.label_5.setPixmap(QtGui.QPixmap('test.png'))

    # 初始化
    def LoadSetting(self):
        self.LogPrint(u"参数初始化")
        self.comboBox_WatchTime.setCurrentIndex(1)
        self.checkBox_RestartDouyin.setChecked(True)
        self.checkBox_AutoAddFriend.setChecked(True)
        self.checkBox_AutoAwesome.setChecked(True)
        self.checkBox_AutoComment.setChecked(False)
        self.checkBox_DownVideo.setChecked(False)
        self.checkBox_Cnt.setChecked(True)
        self.textEdit_Comment.setText("666")
        self.lineEdit_License.setText(self.douyin.android.license)
        self.LogPrint(u"初始化完成")

    # 激活Key
    def ActKey(self):
        url = "http://yinliu.craftor.org:5000/activate/" + self.douyin.android.license
        try:
            req = urllib.request.urlopen(url)
            res = req.read()
        except:
            self.LicenseAvaliabie = False
            self.LogPrint(u"服务器无法连接！")
            return
        #print (res)
        if res == b'1':
            msg = u"已激活！"
        else:
            msg = u"激活失败！"
        self.label_LicenseAvaliable.setText(msg)
        self.LogPrint(msg)

    # 检查Key有效时间
    def CheckKey(self):
        # 请求服务器
        url = "http://yinliu.craftor.org:5000/check/" + self.douyin.android.license
        try:
            req = urllib.request.urlopen(url)
            res = req.read()
            lessTime = int(res)
        except:
            self.LicenseAvaliabie = False
            self.LogPrint(u"服务器无法连接！")
            return

        if (lessTime is not None):
            if lessTime < 0:
                msg = u"未激活，请先激活！"
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

    # 线程
    def douyinThread(self):
        while(self.tRun):

            # 看一会儿视频
            if self.comboBox_WatchTime.currentIndex() == 0:
                cnt = random.randint(5, 10)
            elif self.comboBox_WatchTime.currentIndex() == 1:
                cnt = random.randint(10, 15)
            elif self.comboBox_WatchTime.currentIndex() == 2:
                cnt = random.randint(15, 20)
            else:
                cnt = random.randint(10, 15)
            self.LogPrint(u"看" + str(cnt) + u"秒视频")
            time.sleep(cnt)

            # 点赞
            if (self.checkBox_AutoAwesome.isChecked()):
                self.LogPrint(u"点个赞")
                self.douyin.adb_AwesomeMe()

            # 加好友
            if (self.checkBox_AutoAddFriend.isChecked()):

                self.LogPrint(u"屏幕左滑")
                self.douyin.android.adb_RollingLeftScreen()

                if self.douyin.android.client(text="已关注").exists:
                    self.LogPrint(u"已关注，忽略")
                elif self.douyin.android.client(text="关注").exists:
                    self.LogPrint(u"未关注，关注一下")
                    self.douyin.android.adb_SingleClick(460, 119)
                
                self.LogPrint(u"屏幕右滑")
                self.douyin.android.adb_RollingRightScreen()

            # 下载视频
            if (self.checkBox_DownVideo.isChecked()):
                self.LogPrint(u"保存视频")
                self.douyin.adb_DownVideo()

            # 评论
            if (self.checkBox_AutoComment.isChecked()) :
                self.LogPrint(u"评论开始")
                # 评论中插入随机字符
                len = self.comboBox_RandomStrLen.currentIndex() + 4
                msg = self.textEdit_Comment.toPlainText() + self.douyin.android.RandomStr(len)
                self.douyin.adb_Comment(msg)
                self.LogPrint(u"评论结束")

            # 下一个
            self.LogPrint(u"下一个抖音")
            self.douyin.android.adb_RollingUpScreen(500)

            # 计数
            self.cnt = self.cnt + 1
            self.total = self.total + 1
            if (self.checkBox_Cnt.isChecked()):
                self.LogPrint(u"【已观看：" + str(self.cnt) + "个，累计观看：" + str(self.total) + "个】")

    # 打印日志
    def LogPrint(self, text):
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%H:%M:%S")
        mystr = otherStyleTime + "  " + text
        self.textEdit_Print.append(mystr)

    @pyqtSlot()
    def on_pushButton_Run_clicked(self):

        self.CheckKey()

        if (self.tRun):
            #self.pushButton_Run.setText(u"停止中。。。")
            self.tRun = False
            #self.myThread.join()
            self.LogPrint(u"线程已经停止，等待本次循环结束")
            self.pushButton_Run.setText(u"开始")
        else:

            self.douyin.android.ui2_ConnectDevice()

            # 选检查Key是否有效
            if self.LicenseAvaliabie is False:
                self.LogPrint(u"序列号无效！")
                return 0
            else:
                self.LogPrint(u"序列号有效，准备开始")

            # 来点广告
            #self.douyin.SomeAdv()
            
            # 重新启动抖音
            if (self.checkBox_RestartDouyin.isChecked()):
                self.LogPrint(u"正在重新启动抖音")
                self.douyin.android.client.app_stop(self.douyin.android.APP_DOUYIN)
                self.douyin.android.client.app_start(self.douyin.android.APP_DOUYIN)
                time.sleep(10)
                self.LogPrint(u"启动完成")

            self.tRun = True
            self.cnt = 0
            self.myThread = Thread(target=self.douyinThread)
            self.myThread.start()
            self.LogPrint(u"线程已经启动")
            self.pushButton_Run.setText(u"停止")

    @pyqtSlot()
    def on_pushButton_InitDevice_clicked(self):
        cmd = "python -m uiautomator2 init"
        self.douyin.android.SendCommand(cmd)

    @pyqtSlot()
    def on_pushButton_ConnectDevice_clicked(self):
        self.douyin.android.ui2_ConnectDevice()

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

    @pyqtSlot()
    def on_textEdit_Message_textChanged(self):
        self.message = self.textEdit_Message.toPlainText()

    @pyqtSlot()
    def on_pushButton_BuyKeys_clicked(self):
        fileName = "pay.png"
        self.LogPrint(u"请扫描二维码完成支付")
        self.label_QRCode.setPixmap(QtGui.QPixmap(fileName))

    @pyqtSlot()
    def on_pushButton_DownloadEmulator_clicked(self):
        url = "https://www.yeshen.com/cn/download/fullPackage"
        webbrowser.open(url, new=0, autoraise=True)

    @pyqtSlot(bool)
    def on_checkBox_DownVideo_clicked(self, checked):
        if checked:
            self.label_DownVideo.setText(u"【注意下载多了之后要及时清理】")
        else:
            self.label_DownVideo.setText("")

    @pyqtSlot(bool)
    def on_checkBox_RestartDouyin_clicked(self, checked):
        if checked is False:
            self.label_ResartDouyin.setText(u"【请确认抖音已经启动，并在视频播放状态】")
        else:
            self.label_ResartDouyin.setText("")
    
    @pyqtSlot()
    def on_pushButton_DownloadDouyin_clicked(self):
        url = "http://s.toutiao.com/UsMYE/"
        webbrowser.open(url, new=0, autoraise=True)
        #self.douyin.android.adb_OpenURL(url)

    @pyqtSlot()
    def on_pushButton_ActKey_clicked(self):
        self.ActKey()

if __name__ == '__main__':

    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())

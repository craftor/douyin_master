# -*- coding: utf-8 -*-
import datetime
import time
import cv2
import numpy as np
import configparser
import uiautomator2 as u2
import win32api
import random
import uuid
import os


class AndroidCtrl():

    def __init__(self):
        # 截图文件名
        self.ScreenShotFileName = "Tmp01.png"
        self.ScreenShotDetected = "Tmp02.png"
        # 屏幕尺寸
        self.width = 600
        self.height = 800
        # 根目录
        self.dir_root = "pic"
        # 图像比对默认阈值
        self.threshold = 0.7
        # APP Name
        self.APP_DOUYIN = "com.ss.android.ugc.aweme"
        # client for UI2
        self.client = None
        # 读取参数文件
        self.LoadParameters("configure.ini")
        # 设备列表
        self.devices = []

    # 获取设备列表
    def GetDeviceList(self):
        cmd = "adb devices"
        result = self.SendCommand(cmd)
        if (len(result) <= 1):
            # print("没有找到设备")
            pass
        else:
            # print(len(result))
            for i in range(1, len(result) - 1):
                tmp = result[i].split()
                # print(tmp[0])
                if (tmp is not None):
                    self.devices.append(tmp[0])
        return self.devices

    # 重新定向命令
    def SendCommand(self, command):
        # result = subprocess.Popen(command, shell=True)
        result = os.popen(command).readlines()
        # print(result)
        return result

    # 打印日志
    def LogPrint(self, text):
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
        mystr = otherStyleTime + "  " + text
        print(mystr)

    # 生成随机字符串
    def RandomStr(self, len):
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
        sa = []
        for i in range(len):
            sa.append(random.choice(seed))
        salt = ''.join(sa)
        # print (salt)
        return salt

    # 获取Mac地址
    def GetMac(self):
        node = uuid.getnode()
        mac = uuid.UUID(int=node).hex[-12:]
        return mac

    # 载入参数
    def LoadParameters(self, file):
        try:
            output = open(file, 'r')
            output.close()
        except Exception:
            output = open(file, "w")
            output.write(
                "[parameters] \nlicense=0 \nphone=0 \nlocation = D:/Program Files/Nox/bin/Nox.exe")
            output.close()
            self.license = "0"
            self.phone = "0"
            self.location = "D:/Program Files/Nox/bin/Nox.exe"
            return
        # 参数文件读取
        self.cfg = configparser.ConfigParser()
        self.cfg.read(file, encoding="utf-8")
        # 序列号
        self.license = self.cfg.get("parameters", "license")
        # 手机号
        self.phone = self.cfg.get("parameters", "phone")
        # 模拟器安装路径
        self.location = self.cfg.get("parameters", "location")

    # 写入参数文件
    def SaveParameters(self, file):
        # 参数文件读取
        self.cfg = configparser.ConfigParser()
        self.cfg.read(file, encoding="utf-8")

        self.cfg.set("parameters", "license", self.license)
        self.cfg.set("parameters", "phone", self.phone)
        self.cfg.set("parameters", "location", self.location)

        with open(file, "w+") as f:
            self.cfg.write(f)

    # 启动夜神模拟器
    def StartEmulator(self):
        # args = '-resolution:800x600'
        args = ''
        win32api.ShellExecute(0, 'open', str(self.location), args, '', 0)

    # 使用ui2操作，第一次要初始化一下设备
    def ui2_InitDevice(self):
        cmd = "tools init"
        self.SendCommand(cmd)

    def ui2_ConnectDeviceWiFi(self, ipaddr):
        try:
            self.client = u2.connect_wifi(ipaddr)
            # set delay 1.5s after each UI click and click
            self.client.click_post_delay = 1.0
            # set default element wait timeout (seconds)
            self.client.wait_timeout = 5.0
            return True
        except Exception:
            self.LogPrint(u"手机无法连接，请检查是否未初始化过")
            return False

    def ui2_ConnectDeviceUSB(self, addr):
        try:
            self.client = u2.connect_usb(addr)
            # set delay 1.5s after each UI click and click
            self.client.click_post_delay = 1.0
            # set default element wait timeout (seconds)
            self.client.wait_timeout = 5.0
            return True
        except Exception:
            self.LogPrint(u"手机无法连接，请检查是否未初始化过")
            return False

    # 连接手机
    def ui2_ConnectDevice(self):
        try:
            self.client = u2.connect_usb("127.0.0.1:62001")
            # set delay 1.5s after each UI click and click
            self.client.click_post_delay = 1.0
            # set default element wait timeout (seconds)
            self.client.wait_timeout = 5.0
            return True
        except Exception:
            self.LogPrint(u"手机无法连接，请检查是否未初始化过")
            return False

    # 安装APP
    def ui2_InstallAPP(self, appURL):
        self.client.app_install(appURL)

    def adb_InstallAPP(self, appURL, device):
        cmd = 'adb -s ' + str(device) + ' install ' + appURL
        self.SendCommand(cmd)

    # 启动APP
    def ui2_StartAPP(self, appName):
        try:
            self.client.app_start(appName)
            return True
        except Exception:
            self.LogPrint(u"启动APP失败")
            return False

    # 关闭APP
    def ui2_StopAPP(self, appName):
        try:
            self.client.app_stop(appName)
            return True
        except Exception:
            self.LogPrint(u"关闭APP失败")
            return False

    # 获取当前屏幕分辨率
    def ui2_GetScreenSize(self):
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
    def ui2_OpenDouyinURL(self, url, delaytime):
        self.ui2_OpenURL(url)
        self.client(description=u"打开看看").click()
        time.sleep(delaytime)

    # 上滑屏幕
    def ui2_RollingUpScreen(self):
        self.client.swipe(0.5, 0.8, 0.5, 0.2, 0.1)

    # 下滑屏幕
    def ui2_RollingDownScreen(self, step):
        self.client.swipe(0.5, 0.2, 0.5, 0.8, 0.1)

    def ui2_RollingLeftScreen(self):
        # self.client.swipe(0.9, 0.4, 0.1, 0.4, 0.2)
        pass

    def ui2_RollingRightScreen(self):
        # self.client.swipe(0.1, 0.4, 0.9, 0.4, 0.2)
        pass

    def adb_OpenURL(self, url, device):
        cmd = 'adb -s ' + str(device) + ' shell am start -a android.intent.action.VIEW -d ' + str(url)
        self.SendCommand(cmd)
        time.sleep(1)

    # 只能发英文和数字，不支持中文！
    def adb_SendText(self, text, device):
        cmd = 'adb -s ' + str(device) + ' shell input text ' + str(text)
        self.SendCommand(cmd)
        time.sleep(1)

    # 获取设备列表
    def adb_GetDevices(self):
        cmd = 'adb devices'
        result = self.SendCommand(cmd)
        print(result)

    # 单击操作
    def adb_SingleClick(self, x, y, device):
        cmd = 'adb -s ' + str(device) + ' shell input tap ' + str(x) + ' ' + str(y)
        self.SendCommand(cmd)
        time.sleep(1)

    # 返回按钮
    def adb_ClickReturn(self, device):
        cmd = 'adb -s ' + str(device) + ' shell input keyevent 4'
        self.SendCommand(cmd)
        time.sleep(1)

    # 滑动操作
    def adb_Rolling(self, x1, y1, x2, y2, device):
        cmd = 'adb -s ' + str(device) + ' shell input swipe ' + \
            str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2)
        self.SendCommand(cmd)
        time.sleep(1)

    # 上滑屏幕
    def adb_RollingUpScreen(self, step, device):
        self.adb_Rolling(int(self.width / 2), int(self.height / 2),
                         int(self.width / 2), int(self.height / 2) - step,
                         device)
        time.sleep(1)

    # 下滑屏幕
    def adb_RollingDownScreen(self, step, device):
        self.adb_Rolling(int(self.width / 2), int(self.height / 2),
                         int(self.width / 2), int(self.height / 2) + step,
                         device)
        time.sleep(1)

    # 左滑屏幕
    def adb_RollingLeftScreen(self, device):
        self.adb_Rolling(int(self.width - 20), int(self.height / 2),
                         int(20), int(self.height / 2),
                         device)
        time.sleep(1)

    # 右滑屏幕
    def adb_RollingRightScreen(self, device):
        self.adb_Rolling(int(20), int(self.height / 2),
                         int(self.width - 20), int(self.height / 2),
                         device)
        time.sleep(1)

    # 截屏
    def adb_PullScreenShot(self, device):
        cmd = 'adb -s ' + str(device) + ' shell screencap -p /sdcard/' + self.ScreenShotFileName
        self.SendCommand(cmd)
        cmd = 'adb -s ' + str(device) + ' pull /sdcard/' + self.ScreenShotFileName + ' .'
        self.SendCommand(cmd)

    # 获取屏幕尺寸，非常重要
    def adb_GetScreenSize(self):
        self.adb_PullScreenShot()
        img = cv2.imread(self.ScreenShotFileName, 3)
        self.height, self.width = img.shape[:2]

    # 1个条件比对
    def adb_CompareOne(self, cond1):
        # 比对条件
        yes1, max_loc1 = self.adb_MatchImg(cond1)
        # 检查
        if (yes1):
            return True
        else:
            return False

    # 2个条件比对
    def adb_CompareTwo(self, cond1, cond2):
        # 比对条件
        yes1, max_loc1 = self.adb_MatchImg(cond1)
        yes2, max_loc2 = self.adb_MatchImg(cond2)
        # 检查
        if (yes1 and yes2):
            return True
        else:
            return False

    # 3个条件比对
    def adb_CompareThree(self, cond1, cond2, cond3):
        # 比对条件
        yes1, max_loc1 = self.adb_MatchImg(cond1)
        yes2, max_loc2 = self.adb_MatchImg(cond2)
        yes3, max_loc3 = self.adb_MatchImg(cond3)
        # 检查
        if (yes1 and yes2 and yes3):
            return True
        else:
            return False

    # 找匹配图标
    def adb_MatchImg(self, Target):
        # 原始图片
        img_rgb = cv2.imread(self.ScreenShotFileName)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        # 比对模板图片
        temp_url = self.dir_root + "/" + Target
        # print(temp_url)
        template = cv2.imread(temp_url, 0)
        # 获取模板图片尺寸
        w, h = template.shape[::-1]
        # 比对操作
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        # 比对结果坐标
        loc = np.where(res >= self.threshold)
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 找到最大值和最小值
        # print(cv2.minMaxLoc(res))
        # print(loc)

        # 描绘出外框
        for pt in zip(*loc[::-1]):
            cv2.rectangle(
                img_rgb, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
        # 保存识别目标后的图
        cv2.imwrite(self.ScreenShotDetected, img_rgb)

        # 检查比对结果
        for pp in loc:
            # 如果不为空，说明有比对成果的内容
            if len(pp):
                # print ("Yes")
                # print(pp)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(
                    res)  # 找到最大值和最小值
                # print (max_loc)
                return True, max_loc
            else:
                # print ("Empty")
                return False, []

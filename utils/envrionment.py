# coding: utf-8

from appium import webdriver
from multiprocessing import Pool
from utils.appiumServer import AppiumServer
from utils.phoneInfo import *
import random
import os

def getDriver(device):
    # getRun = getYam(PATH("../yaml/run.yaml"))

    print(device)
    desired_caps = {}
    desired_caps['platformName'] = device["platformName"]
    desired_caps['platformVersion'] = device["platformVersion"]
    desired_caps['deviceName'] = device["deviceName"]
    desired_caps['appPackage'] = device["appPackage"]
    desired_caps['appActivity'] = device["appActivity"]
    desired_caps['udid'] = device["deviceName"]

    desired_caps["noReset"] = "True"
    desired_caps['noSign'] = "True"
    # desired_caps["unicodeKeyboard"] = "True"
    # desired_caps["resetKeyboard"] = "True"
    # desired_caps['app'] = devices["app"]

    remote = "http://127.0.0.1:" + str(device["port"]) + "/wd/hub"
    driver = webdriver.Remote(remote, desired_caps)

    return driver

def devicesPool():
    bridge = AndroidDebugBridge()
    devices = bridge.attached_devices()
    devices_Pool = []
    if len(devices) > 0:
        for device in devices:
            _initApp = {}
            _initApp["deviceName"] = device
            _initApp["platformVersion"] = getPhoneInfo(devices=_initApp["deviceName"])["release"]
            _initApp["platformName"] = "android"
            _initApp["appPackage"] = "com.ss.android.ugc.live"
            _initApp["appActivity"] = "com.ss.android.ugc.live.splash.LiveSplashActivity"
            _initApp["port"] = str(random.randint(4700, 4900))
            _initApp["bport"] = str(random.randint(4700, 4900))
            # _initApp["appPackage"] = apkInfo.getApkBaseInfo()[0]
            # _initApp["appActivity"] = apkInfo.getApkActivity()
            # _initApp["app"] = getDevices[i]["app"]
            devices_Pool.append(_initApp)
    else:
        print("没有可用的安卓设备")
    return devices_Pool


#!/usr/bin/env python
# coding: utf-8

import time

import allure
import pytest
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from log import Log as L
from utils.shell import Shell

#设备信息
desired_caps ={}
desired_caps['platformName'] = 'Android'
desired_caps['platforVersion'] = '6.0.1'
desired_caps['deviceName'] = 'huawei'
desired_caps['appPackage'] = 'com.ss.android.ugc.live'
desired_caps['appActivity'] = 'com.ss.android.ugc.live.splash.LiveSplashActivity'
desired_caps['newCommandTimeout'] = 20000
desired_caps['noReset'] = True
desired_caps['unicodeKeyboard'] = True
desired_caps['resetKeyboard'] = True

#访问本地server，通过server去访问真机
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

def isElement(driver, identifyBy, element):
    '''
    判断元素是否存在
    :param identifyBy:
    :param element:
    :return:
    '''
    time.sleep(1)

    flag = None
    try:
        if identifyBy == "id":
            driver.find_element_by_id(element)
        elif identifyBy == "xpath":
            driver.find_element_by_xpath(element)
        elif identifyBy == "class":
            driver.find_element_by_class_name(element)
        elif identifyBy == "link text":
            driver.find_element_by_link_text(element)
        elif identifyBy == "partial link text":
            driver.find_element_by_partial_link_text(element)
        elif identifyBy == "name":
            driver.find_element_by_name(element)
        elif identifyBy == "tag name":
            driver.find_element_by_tag_name(element)
        elif identifyBy == "css selector":
            driver.find_element_by_css_selector(element)
        flag = True
    except NoSuchElementException:
        flag = False
    finally:
        return flag


def getSize():
    '''
    获取屏幕长和宽
    :return: 手机屏幕长宽
    '''
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    #print x, y
    return (x, y)


def swipeUp(t, n):
    '''
    向上滑动
    :param t:滑动的时间
    :param n:滑动的次数
    :return:
    '''
    time.sleep(2)
    i = 0
    l = getSize()
    xStart = int(l[0] * 0.5)
    yStart = int(l[1] * 0.75)
    yEnd = int(l[1] * 0.25)
    while i < n:
        driver.swipe(0, yStart, 0, yEnd, t)
        i = i + 1


def swipeDown(t):
    '''
    屏幕向下滑动
    :param t: 滑动的时间
    :return:
    '''
    l = getSize()
    xStart = int(l[0] * 0.5)  #x坐标
    yStart = int(l[1] * 0.25)   #起始y坐标
    yEnd = int(l[1] * 0.75)   #终点y坐标
    driver.swipe(xStart, yStart, xStart, yEnd,t)


def swipLeft(t):
    '''
    屏幕向左滑动
    :param t: 滑动时间
    :return:
    '''
    l=getSize()
    xStart=int(l[0]*0.75)
    yEnd=int(l[1]*0.5)
    xEnd=int(l[0]*0.05)
    driver.swipe(xStart, yEnd, yEnd, yEnd, t)

def check_home_page(driver):
    '''
    返回首页
    :param driver:
    :return:
    '''
    if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "首页")]'):
        print "login testing pass."
    else:
        print "login testing fail."

@allure.step('some operation')
@allure.issue('http://jira.lan/browse/ISSUE-1')
def new_user_view_video():
    '''
    未登录状态下滑动刷新，进入视频详情页看视频
    :return:
    '''
    try:
        if isElement(driver, 'id', 'com.ss.android.ugc.live:id/zs'):
            print("new user view video testing now.")
            # 向上拉动刷新
            swipeUp(500, 3)
            time.sleep(1)
            # 点击打开第一个视频
            driver.find_element_by_id('com.ss.android.ugc.live:id/a6m').click()
            # 确定进入视频
            time.sleep(2)
            # 退回首页
            driver.find_element_by_id('com.ss.android.ugc.live:id/ef').click()
            if isElement(driver, 'id', 'com.ss.android.ugc.live:id/zs'):
                print "login testing pass."
            else:
                print "login testing fail."
    except Exception as e:
        print e

@allure.step(title="获取账号和密码")
@allure.issue('http://jira.lan/browse/ISSUE-1')
def test_new_user_view_live():
    '''
    未登录状态下滑动刷新，进入直播详情页看直播
    :return:
    '''
    try:
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "直播")]'):
            print("new user view live testing now.")
            time.sleep(2)
            # 点击进入直播feed
            driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "直播")]').click()
            # 向上拉动刷新
            swipeUp(500, 3)
            time.sleep(1)
            # 点击打开第一个直播
            driver.find_elements_by_class_name("android.widget.RelativeLayout")[0].click()
            time.sleep(2)
            # 退出直播（退出按钮是最后一个按钮）
            driver.find_elements_by_class_name("android.widget.ImageView")[-1].click()
            # 退回首页
            driver.find_element_by_id('com.ss.android.ugc.live:id/ef').click()
            if isElement(driver, 'id', 'com.ss.android.ugc.live:id/zs'):
                print "login testing pass."
            else:
                print "login testing fail."
    except Exception as e:
        print e




def login():
    '''
    成功登录
    :return:
    '''
    try:
        # if isElement(driver, 'id', 'com.ss.android.ugc.live:id/zs'):
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "注册/登录")]'):
            print("login testing now.")
            # 等待注册／登录按钮出现
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/zr")))
            # 点击注册／登录按钮
            driver.find_element_by_id("com.ss.android.ugc.live:id/zs").click()
            # 清空输入框后输入手机号
            # driver.find_element_by_id("com.ss.android.ugc.live:id/rq").clear()
            driver.find_element_by_id("com.ss.android.ugc.live:id/rq").send_keys("18611084547")
            # 等待下一步按钮出现并点击
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/ru")))
            driver.find_element_by_id("com.ss.android.ugc.live:id/ru").click()
            # 清空输入框并输入登录密码
            # driver.find_element_by_id("com.ss.android.ugc.live:id/acq").clear()
            driver.find_element_by_id("com.ss.android.ugc.live:id/acq").send_keys("12345678")
            # 等待登录按钮出现并点击
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/acz")))
            driver.find_element_by_id("com.ss.android.ugc.live:id/acz").click()
        time.sleep(1)
        # 确认成功登录，通过判断首页出现即成功
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/akq")))
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "首页")]'):
            print "login testing pass."
        else:
            print "login testing fail."
    except Exception as e:
        print e


def main():

    # new_user_view_video()
    #  login()
    test_new_user_view_live()
    # getSide()
    # swipeUp(500, 3)


if __name__ == '__main__':
     xml_report_path = "./allure-results"
     html_report_path = "./allure-results/html"
     # 开始测试
     args = ["test.py", '-s', '-q', '--alluredir', xml_report_path]
     pytest.main(args)
     args = ["test.py", '-s', '-q', '--alluredir', xml_report_path]
     pytest.main(args)
     # 生成html测试报告
     cmd1 = 'allure generate %s -o %s' % (xml_report_path, html_report_path)
     cmd2 = 'allure open ' + html_report_path
     try:
         Shell.invoke(cmd1)
         Shell.invoke(cmd2)
     except:
         L.e("Html测试报告生成失败,确保已经安装了Allure-Commandline")
     # try :
     #     Shell.invoke("allure serve --profile  ./")
     # except:
     #     L.e("Html测试报告生成失败,确保已经安装了Allure-Commandline")
     #


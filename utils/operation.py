# -*- coding: utf-8 -*-

import time
from selenium.common.exceptions import NoSuchElementException

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



def findElement(driver, info):
    if(info.startswith("//")):
        element = driver.find_element_by_xpath(info)
    elif(":id/" in info or ":string/" in info):
        element = driver.find_element_by_id(info)
    else:
        try:
            element = driver.find_element_by_name(info)
        except:
            element = driver.find_element_by_class_name(info)
    return element


def getSize(driver):
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


def swipLeft(driver, t):
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

def click(element):
    element.click()
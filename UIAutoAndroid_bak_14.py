#!/usr/bin/env python
# coding: utf-8

import time
import allure
import pytest
from allure.constants import AttachmentType

from appium import webdriver

from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

#设备信息Nexus 5
desired_caps ={}
desired_caps['platformName'] = 'Android'
desired_caps['platforVersion'] = '6.0'
#desired_caps['platforVersion'] = '6.0'
desired_caps['deviceName'] = 'huawei'
#desired_caps['deviceName'] = 'MI 5C'
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


def clear_hongbao():
    '''
    安装首次启动出现“拍视频领红包”，任意点击消息
    :return:
    '''
    if isElement(driver, 'xpath', '//android.widget.FrameLayout[@index="0"]/android.widget.FrameLayout[@index="0"]/'
                                  'android.widget.ImageView[@index="0"]'):
        driver.back()


def cancel_download():
    if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "快来下载啦")]'):
        driver.find_element_by_id('com.ss.android.ugc.live:id/later_btn').click()


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
    i = 0
    l = getSize()
    xStart = int(l[0] * 0) #x坐标
    yStart = int(l[1] * 0.75) #起始y坐标
    yEnd = int(l[1] * 0.25) #终点y坐标
    while i < n:
        driver.swipe(xStart, yStart, xStart, yEnd, t)
        i = i + 1


def swipeDown(t, n):
    '''
    屏幕向下滑动
    :param t: 滑动的时间
    :return:
    '''
    i = 0
    l = getSize()
    xStart = int(l[0] * 0)  #x坐标
    yStart = int(l[1] * 0.25)   #起始y坐标
    yEnd = int(l[1] * 0.75)   #终点y坐标
    #print xStart,yStart,yEnd
    while i < n:
        driver.swipe(xStart, yStart, xStart, yEnd, t)
        i = i + 1


def swipLeft(t, n):
    '''
    屏幕向左滑动
    :param t: 滑动时间
    :return:
    '''
    i = 0
    l=getSize()
    xStart=int(l[0]*0.75)
    yEnd=int(l[1]*0.9)
    xEnd=int(l[0]*0.25)
    driver.swipe(xStart, yEnd, xEnd, yEnd, t)
    while i < n:
        driver.swipe(xStart, yEnd, xStart, yEnd, t)
        i = i + 1

def seekBar(driver, id, ratio):
    '''
    :param driver: driver
    :param id: 元素的 id
    :param ratio: 宽度的比例位置
    :return:
    '''
    # 通过 id 找到 seek_bar
    seek_bar = driver.find_element_by_id(id)
    # 获取到 seek bar 的 X 轴位置
    print(seek_bar.location)
    start = seek_bar.location.get('x')
    # 获取到 seek bar 的宽度
    print(seek_bar.size)
    width = seek_bar.size.get('width')
    # 获取到 seek bar 的 Y 轴位置
    y = seek_bar.location.get('x')

    # 获取一个 Action
    action = TouchAction(driver)

    # 获取移动的目的位置
    moveTo = int(width * ratio)
    action.long_press(el=seek_bar, x=start, y=y).move_to(el=seek_bar, x=moveTo, y=y).release().perform()


def new_user_check_is_homepage(driver):
    '''
    返回首页
    :param driver:
    :return:
    '''
    if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "注册/登录")]'):
        print "login testing pass."
    else:
        print "login testing fail."


def login_check_is_homepage(driver):
    '''
    返回首页
    :param driver:
    :return:
    '''
    if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "首页")]'):
        print "login testing pass."
    else:
        print "login testing fail."
    time.sleep(2)


def new_user_view_video_up():
    '''
    未登录状态向上滑动刷新，进入视频详情页看视频
    :return:
    '''
    try:
        if isElement(driver, ):
            print("new user view video up testing now.")
            time.sleep(2)
            # 向上拉动刷新
            swipeUp(500, 3)
            time.sleep(1)
            # 点击打开第一个视频
            driver.find_elements_by_id('com.ss.android.ugc.live:id/video_cover')[0].click()
            # 确定进入视频
            time.sleep(2)
            # 退回首页
            driver.find_element_by_id('com.ss.android.ugc.live:id/close').click()
            new_user_check_is_homepage(driver)
    except Exception as e:
        print e


def new_user_view_video_down():
    '''
    未登录状态向下滑动刷新，进入视频详情页看视频
    :return:
    '''
    try:
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "注册/登录")]'):
            print("new user view video down testing now.")
            time.sleep(2)
            # 向下拉动刷新
            swipeDown(500, 1)
            time.sleep(1)
            # 点击打开第一个视频
            # driver.find_element_by_id('com.ss.android.ugc.live:id/a9_').click()
            driver.find_elements_by_id('com.ss.android.ugc.live:id/video_cover')[0].click()
            time.sleep(2)
            # 退回首页
            driver.find_element_by_id('com.ss.android.ugc.live:id/close').click()
            new_user_check_is_homepage(driver)
    except Exception as e:
        print e


def new_user_view_video_hit():
    '''
    未登录状态点击视频刷新，进入视频详情页看视频
    :return:
    '''
    try:
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "注册/登录")]'):
            print("new user view video down testing now.")
            time.sleep(2)
            # 点击tabs的视频
            driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "视频")]').click()
            # 点击打开第一个视频
            # driver.find_element_by_id('com.ss.android.ugc.live:id/a9_').click()
            driver.find_elements_by_id('com.ss.android.ugc.live:id/video_cover')[0].click()
            time.sleep(2)
            # 退回首页
            driver.find_element_by_id('com.ss.android.ugc.live:id/close').click()
            new_user_check_is_homepage(driver)
    except Exception as e:
        print e


def new_user_view_live_up():
    '''
    未登录状态上滑动刷新，进入直播详情页看直播
    :return:
    '''
    try:
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "注册/登录")]'):
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
            driver.find_element_by_id('com.ss.android.ugc.live:id/close').click()
            new_user_check_is_homepage(driver)
    except Exception as e:
        print e


def new_user_view_live_down():
    '''
    未登录状态下滑动刷新，进入直播详情页看直播
    :return:
    '''
    try:
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "注册/登录")]'):
            print("new user view live down testing now.")
            time.sleep(2)
            # 点击进入直播feed
            driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "直播")]').click()
            # 向上拉动刷新
            swipeDown(500, 1)
            time.sleep(1)
            # 点击打开第一个直播
            driver.find_elements_by_class_name("android.widget.RelativeLayout")[0].click()
            time.sleep(2)
            # 退出直播（退出按钮是最后一个按钮）
            driver.find_elements_by_class_name("android.widget.ImageView")[-1].click()
            # 退回首页
            driver.find_element_by_id('com.ss.android.ugc.live:id/close').click()
            new_user_check_is_homepage(driver)
    except Exception as e:
        print e


def new_user_view_live_hit():
    '''
    未登录状态点击直播刷新，进入直播详情页看直播
    :return:
    '''
    try:
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "注册/登录")]'):
            print("new user view live down testing now.")
            time.sleep(2)
            # 点击进入直播feed
            driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "直播")]').click()
            # 点击直播刷新feed
            driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "直播")]').click()
            # print('----------')
            time.sleep(1)
            # 点击打开第一个直播
            driver.find_elements_by_class_name("android.widget.RelativeLayout")[0].click()
            time.sleep(2)
            # 退出直播（退出按钮是最后一个按钮）
            driver.find_elements_by_class_name("android.widget.ImageView")[-1].click()
            # 退回首页
            driver.find_element_by_id('com.ss.android.ugc.live:id/close').click()
            new_user_check_is_homepage(driver)
    except Exception as e:
        print e



def login():
    '''
    成功登录
    :return:
    '''
    try:
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "注册/登录")]'):
            print("login testing now.")
            time.sleep(2)
            # 取消升级提醒
            clear_hongbao()
            # 等待注册／登录按钮出现
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/register")))
            # 点击注册／登录按钮
            driver.find_element_by_id("com.ss.android.ugc.live:id/register").click()
            # 清空输入框后输入手机号
            # driver.find_element_by_id("com.ss.android.ugc.live:id/rq").clear()
            driver.find_element_by_id("com.ss.android.ugc.live:id/mobile_input").send_keys("18611084547")
            # 等待下一步按钮出现并点击
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/next_step_btn")))
            driver.find_element_by_id("com.ss.android.ugc.live:id/next_step_btn").click()
            # 清空输入框并输入登录密码
            # driver.find_element_by_id("com.ss.android.ugc.live:id/acq").clear()
            driver.find_element_by_id("com.ss.android.ugc.live:id/password_input").send_keys("12345678")
            # 等待登录按钮出现并点击
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/login_btn")))
            driver.find_element_by_id("com.ss.android.ugc.live:id/login_btn").click()
            time.sleep(2)
        # 确认成功登录，通过判断首页出现即成功
        login_check_is_homepage(driver)
    except Exception as e:
        print e


def login_video_detail():
    '''
    登录进入视频详情页看视频、看评论、发评论、点赞、转发、关注(视频 feed)
    :return:
    '''
    try:
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "首页")]'):
            print('login video detail testing now')

            # 点击视频feed
            driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "视频")]').click()
            time.sleep(1)

            # 点击第一个视频，进入视频详情页
            driver.find_elements_by_id('com.ss.android.ugc.live:id/video_cover')[0].click()

            # 进入视频详情页后,首先判断蒙层
            if isElement(driver, 'id', 'com.ss.android.ugc.live:id/tips_image'):
                driver.find_elements_by_id('com.ss.android.ugc.live:id/tips_image').click()

            # 看评论
            driver.find_element_by_id('com.ss.android.ugc.live:id/comments_num').click()
            # 看评论，滑动看评论
            swipeUp(500, 2)
            # 退出评论
            driver.find_element_by_id('com.ss.android.ugc.live:id/close_comment').click()
            # 写评论
            driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "说点什么...")]').click()
            driver.find_element_by_id('com.ss.android.ugc.live:id/comment_editor').send_keys(u'利害了，A')
            driver.find_element_by_id('com.ss.android.ugc.live:id/comment_editor_send').click()
            time.sleep(2)

            # 点赞
            driver.find_elements_by_xpath('//android.widget.TextView[contains(@text, "说点什么...")]/../*')[2].click()

            # 转发
            driver.find_element_by_id('com.ss.android.ugc.live:id/turn_video').click()
            driver.find_elements_by_id('com.ss.android.ugc.live:id/share_third')[0].click()
            driver.back()
            time.sleep(1)
            driver.find_element_by_id('com.ss.android.ugc.live:id/close').click()
            # 退回首页
            login_check_is_homepage(driver)
    except Exception as e:
        print e


def notice():
    '''
    查看消息列表，滑动查看消息，点击消息查看具体消息内容。
    :return:
    '''
    try:
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "消息")]'):
            print('notice testing now.')
            time.sleep(1)
            # 点击消息，进入消息列表
            driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "消息")]').click()
            time.sleep(1)
            # 向上滑动，查看消息
            swipeUp(500, 1)
            # 点击第一个消息查看
            if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "评论了你")]'):
                #跳转被评论的视频
                driver.find_elements_by_xpath('//android.widget.TextView[contains(@text, "评论了你")]')[0].click()
                time.sleep(1)
                #退出评论
                driver.find_element_by_id("com.ss.android.ugc.live:id/close_comment").click()
                #退出视频
                driver.find_element_by_id("com.ss.android.ugc.live:id/close").click()
            elif isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "喜欢了你的评论")]'):
                #跳转被评论的视频
                driver.find_elements_by_xpath('//android.widget.TextView[contains(@text, "喜欢了你的评论")]')[0].click()
                time.sleep(1)
                # 退出评论
                driver.find_element_by_id("com.ss.android.ugc.live:id/close_comment").click()
                # 退出视频
                driver.find_element_by_id("com.ss.android.ugc.live:id/close").click()
            elif isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "回复了你")]'):
                # 跳转被评论的视频
                driver.find_elements_by_xpath('//android.widget.TextView[contains(@text, "回复了你")]')[0].click()
                time.sleep(1)
                # 退出评论
                driver.find_element_by_id("com.ss.android.ugc.live:id/close_more_comment").click()
                # 退出视频
                driver.find_element_by_id("com.ss.android.ugc.live:id/close").click()
            elif isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "喜欢了你的作品")]'):
                # 跳转被评论的视频
                driver.find_elements_by_xpath('//android.widget.TextView[contains(@text, "喜欢了你的作品")]')[0].click()
                time.sleep(1)
                # 退出视频
                driver.find_element_by_id("com.ss.android.ugc.live:id/close").click()
            elif isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "发视频提到了你")]'):
                # 跳转被评论的视频
                driver.find_elements_by_xpath('//android.widget.TextView[contains(@text, "发视频提到了你")]')[0].click()
                time.sleep(1)
                # 退出视频
                driver.find_element_by_id("com.ss.android.ugc.live:id/close").click()
            elif isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "关注了你")]'):
                # 跳转到个人页
                driver.find_elements_by_xpath('//android.widget.TextView[contains(@text, “关注了你”]')[0].click()
                time.sleep(1)
                # 退出个人页
                driver.find_element_by_id("com.ss.android.ugc.live:id/back_btn").click()
            else:
                driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "首页")]').click()
            # 退回首页
            driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "首页")]').click()
            login_check_is_homepage(driver)
    except Exception as e:
        print e


def gossip():
    '''
    查看八卦列表，滑动查看，点击一条八卦查看具体内容。
    :return:
    '''
    try:
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "消息")]'):
            print('gossip testing now.')
            time.sleep(1)
            # 点击消息，进入消息列表
            driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "消息")]').click()
            time.sleep(2)
            # 点击八卦，进入八卦列表
            driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "八卦")]').click()
            time.sleep(3)
            # 点击任意一个视频
            driver.find_elements_by_id('com.ss.android.ugc.live:id/image')[0].click()
            # 向上滑动
            swipeUp(500,2)
            time.sleep(2)
            # 向下滑动
            swipeDown(500, 3)
            # 退出视频
            driver.find_element_by_id("com.ss.android.ugc.live:id/close").click()
            # 返回首页
            driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "首页")]').click()
            login_check_is_homepage(driver)
    except Exception as e:
        print e


def shooting_from_gallery():
    '''
    登录，从相册裁剪自己喜欢的视频，直接发布。
    :return:
    '''
    if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "首页")]'):
        print('login shoot from photo album testing now.')

        # 点击‘‘+’’进行拍摄页面
        driver.find_element_by_id('com.ss.android.ugc.live:id/shot').click()
        time.sleep(2)
        # 点击“相册”
        driver.find_element_by_id('com.ss.android.ugc.live:id/tv_gallery').click()
        time.sleep(3)
        # 选择喜欢的视频
        driver.find_elements_by_id('com.ss.android.ugc.live:id/media_view')[0].click()
        time.sleep(3)
        # 裁剪视频
        swipLeft(500, 1)
        print('swipLeft')
        time.sleep(2)
        # 下一步
        driver.find_element_by_id('com.ss.android.ugc.live:id/next').click()
        # 等待合成,并到下一步页面
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/tv_next_step")))
        # 选音乐
        driver.find_element_by_id('com.ss.android.ugc.live:id/ll_cut_music').click()
        driver.find_elements_by_class_name("android.widget.LinearLayout")[0].click()
        time.sleep(3)
        driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "确定")]').click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/tv_cut_music_finish")))
        driver.find_element_by_id('com.ss.android.ugc.live:id/tv_cut_music_finish').click()
        # 音量选择
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/rl_change_volume")))
        driver.find_element_by_id('com.ss.android.ugc.live:id/rl_change_volume').click()
        seekBar(driver, 'com.ss.android.ugc.live:id/seek_bar_man_voice', 0.85)
        seekBar(driver, 'com.ss.android.ugc.live:id/seek_bar_music_voice', 0.85)
        driver.find_element_by_id('com.ss.android.ugc.live:id/iv_change_volume_next').click()
        time.sleep(3)
        # 滤镜选择
        driver.find_element_by_id('com.ss.android.ugc.live:id/ll_new_filter').click()
        swipLeft(500, 1)
        driver.find_elements_by_id('com.ss.android.ugc.live:id/iv_bg')[1].click()
        driver.find_element_by_id('com.ss.android.ugc.live:id/iv_filter_next').click()
        time.sleep(0.5)
        # 下一步
        driver.find_element_by_id('com.ss.android.ugc.live:id/tv_next_step').click()
        # 发布
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/tv_publish_video")))
        driver.find_element_by_id('com.ss.android.ugc.live:id/tv_publish_video').click()
        time.sleep(2)
        WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[contains(@text, "上传成功！分享给朋友")]')))
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "上传成功！分享给朋友")]'):
            print('publish video successed')
        else:
            print('publish video failed')
        # 返回首页
        driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "首页")]').click()
        login_check_is_homepage(driver)


def shooting_from_shoot_next():
    '''
    登录,从拍摄录制视频,发布视频,
    :return:
    '''
    try:
        if isElement(driver, 'id', 'com.ss.android.ugc.live:id/shot'):
            print('shooting by shoot testing now.')
            # 点击“+”进入拍摄页面
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/shot")))
            driver.find_element_by_id('com.ss.android.ugc.live:id/shot').click()
            time.sleep(2)
            # 选择贴纸
            driver.find_element_by_id('com.ss.android.ugc.live:id/iv_show_stickers').click()
            time.sleep(1)
            # 选择第11个贴纸
            driver.find_elements_by_id('com.ss.android.ugc.live:id/sticker_item_img')[10].click()
            # 选着贴纸瘦脸程度
            driver.find_element_by_id('com.ss.android.ugc.live:id/eyes_level5').click()
            # 退出贴纸
            driver.find_element_by_id('com.ss.android.ugc.live:id/view_blank').click()
            # 如果有上次保存的拍摄，直接下一步
            if not isElement(driver, 'id', 'com.ss.android.ugc.live:id/iv_deleteLast'):
                # 拍摄
                driver.find_element_by_id('com.ss.android.ugc.live:id/record').click()
                time.sleep(10)
                driver.find_element_by_id('com.ss.android.ugc.live:id/record').click()
            time.sleep(2)
            driver.find_element_by_id('com.ss.android.ugc.live:id/iv_next').click()

            time.sleep(2)
            # 点击下一步
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/tv_next_step")))
            driver.find_element_by_id('com.ss.android.ugc.live:id/tv_next_step').click()
            time.sleep(2)
            # 进入封面选择页面
            driver.find_element_by_id('com.ss.android.ugc.live:id/ll_edit_hint').click()
            time.sleep(2)
            # 选择封面
            driver.find_elements_by_class_name('android.widget.ImageView')[3].click()
            # 填写标题
            driver.find_element_by_id('com.ss.android.ugc.live:id/et_title').send_keys(u"测试测试")
            time.sleep(3)
            # 点击完成
            driver.find_element_by_id('com.ss.android.ugc.live:id/tv_select_cover_finish').click()
            time.sleep(5)
            # 编写视频内容
            driver.find_element_by_id('com.ss.android.ugc.live:id/et_description').send_keys(u"啦啦啦啦")
            # 添加@
            driver.find_element_by_id('com.ss.android.ugc.live:id/btn_at').click()
            time.sleep(2)
            driver.find_elements_by_id('com.ss.android.ugc.live:id/at_friend_avatar')[1].click()
            time.sleep(2)
            # 点击发布
            driver.find_element_by_id('com.ss.android.ugc.live:id/tv_publish_video').click()
            time.sleep(30)
            if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "上传成功！分享给朋友")]'):
                print('publish video successed')
            else:
                print('publish video fail')
            login_check_is_homepage(driver)
    except Exception as e:
        print e


def shooting_from_shoot_draft():
    '''
    从草稿箱发视频，途径:录制视频、存草稿、发布
    :return:
    '''
    if isElement(driver, 'id', 'com.ss.android.ugc.live:id/shot'):
        print('shooting by shoot testing now.')
        # 点击“+”进入拍摄页面
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/shot")))
        driver.find_element_by_id('com.ss.android.ugc.live:id/shot').click()
        time.sleep(2)
        # 选择贴纸
        driver.find_element_by_id('com.ss.android.ugc.live:id/iv_show_stickers').click()
        time.sleep(1)
        # 选择第11个贴纸
        driver.find_elements_by_id('com.ss.android.ugc.live:id/sticker_item_img')[10].click()
        # 选着贴纸瘦脸程度
        driver.find_element_by_id('com.ss.android.ugc.live:id/eyes_level5').click()
        # 退出贴纸
        # print("hahahahhah")
        driver.find_element_by_id('com.ss.android.ugc.live:id/view_blank').click()
        # 如果有上次保存的拍摄，直接下一步
        if not isElement(driver, 'id', 'com.ss.android.ugc.live:id/iv_deleteLast'):
            # 拍摄
            driver.find_element_by_id('com.ss.android.ugc.live:id/record').click()
            time.sleep(10)
            driver.find_element_by_id('com.ss.android.ugc.live:id/record').click()
        time.sleep(2)
        driver.find_element_by_id('com.ss.android.ugc.live:id/iv_next').click()
        # 存草稿
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "com.ss.android.ugc.live:id/tv_draft")))
        driver.find_element_by_id('com.ss.android.ugc.live:id/tv_draft').click()
        # 检测到待发布确保存草稿成功
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "待发布")]'):
            # 进入草稿
            driver.find_elements_by_id("com.ss.android.ugc.live:id/video_cover")[0].click()
            # 选择第一个草稿,点击发布
            driver.find_elements_by_id("com.ss.android.ugc.live:id/tv_publish")[0].click()
            # 进入视频编辑页
            driver.find_element_by_id('com.ss.android.ugc.live:id/ll_edit_hint').click()
            time.sleep(2)
            # 选择封面
            driver.find_elements_by_class_name('android.widget.ImageView')[3].click()
            # 填写标题
            driver.find_element_by_id('com.ss.android.ugc.live:id/et_title').send_keys(u"测试测试")
            time.sleep(3)
            # 点击完成
            driver.find_element_by_id('com.ss.android.ugc.live:id/tv_select_cover_finish').click()
            time.sleep(5)
            # 编写视频内容
            driver.find_element_by_id('com.ss.android.ugc.live:id/et_description').send_keys(u"啦啦啦啦")
            # 添加@
            driver.find_element_by_id('com.ss.android.ugc.live:id/btn_at').click()
            time.sleep(2)
            driver.find_elements_by_id('com.ss.android.ugc.live:id/at_friend_avatar')[1].click()
            time.sleep(2)
            # 点击发布
            driver.find_element_by_id('com.ss.android.ugc.live:id/tv_publish_video').click()
            time.sleep(20)
            if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "上传成功！分享给朋友")]'):
                print('publish video successed')
            else:
                print('publish video fail')
        # 返回首页
        driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "首页")]').click()
        login_check_is_homepage(driver)



def test_video_attention():
    '''
    视屏详情页点击关注，进入 profile 取消关注
    :return:
    '''
    try:
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "首页")]'):
            print('video\'s attention testing now.')
            # 视频 feed
            driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "视频")]').click()
            time.sleep(1)
            # 进入视频详情页
            driver.find_elements_by_id('com.ss.android.ugc.live:id/video_cover')[0].click()
            time.sleep(2)
            # 点击用户名右侧关注
            driver.find_element_by_id('com.ss.android.ugc.live:id/follow_prompt').click()
            # 点击用户头像,进入profile 页
            driver.find_element_by_id('com.ss.android.ugc.live:id/avatar').click()
            time.sleep(2)
            # 取消关注
            driver.find_element_by_id('com.ss.android.ugc.live:id/follow_header').click()
            time.sleep(1)
            driver.find_element_by_xpath('//android.widget.Button[contains(@text, "确定")]').click()
            time.sleep(1)
            # 退出 profile 页
            driver.find_element_by_id('com.ss.android.ugc.live:id/back_btn').click()
            # 退出视频
            driver.find_element_by_id('com.ss.android.ugc.live:id/close').click()
            time.sleep(2)
            login_check_is_homepage(driver)
    except Exception as e:
        print e


def search_tags():
    '''
    根据标签搜索
    :return:
    '''
    try:
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "视频")]'):
            print('search by tags testing now.')
            time.sleep(2)
            # 进入搜索页面
            driver.find_element_by_id('com.ss.android.ugc.live:id/search').click()
            time.sleep(2)
            # 通过标签搜索好友,选第一个
            driver.find_elements_by_id('com.ss.android.ugc.live:id/tv_label')[0].click()
            time.sleep(3)
            swipeUp(500, 3)
            time.sleep(2)
            # 点击取消，退出搜索
            driver.find_element_by_id('com.ss.android.ugc.live:id/cancel_btn').click()
            login_check_is_homepage(driver)
    except Exception as e:
        print e


def test_search_recommend():
    '''
    根据推荐搜索
    :return:
    '''
    try:
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "视频")]'):
            print('search by recommend testing now.')
            # 进入搜索页面
            driver.find_element_by_id('com.ss.android.ugc.live:id/search').click()
            time.sleep(2)
            # 滑动查看推荐用户
            swipeUp(500, 3)
            time.sleep(2)
            # 点击取消，退出搜索
            driver.find_element_by_id('com.ss.android.ugc.live:id/cancel_btn').click()
            login_check_is_homepage(driver)
    except Exception as e:
        print e

@allure.feature('搜索')
@allure.issue('https://jira.bytedance.com/browse/ZHIBO-6887?filter=14391')
def test_search_userid():
    '''
    根据用户 id 搜索
    :return:
    '''
    try:
        if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "视频")]'):
            print('search by user id testing now.')
            with pytest.allure.step('进入搜索页面'):
                # 进入搜索页面
                driver.find_element_by_id('com.ss.android.ugc.live:id/search').click()
                time.sleep(2)
            with pytest.allure.step('通过输入用户id查找好友'):
                # 通过输入用户id查找好友
                driver.find_element_by_id('com.ss.android.ugc.live:id/search_edit').send_keys('143274589')
                allure.attach('截图', driver.get_screenshot_as_png(), type=AttachmentType.PNG)
                time.sleep(3)
                swipeUp(500, 3)
                time.sleep(2)
            with pytest.allure.step('点击取消，退出搜索'):
                # 点击取消，退出搜索
                driver.find_element_by_id('com.ss.android.ugc.live:id/cancel_btn').click()
                login_check_is_homepage(driver)
    except Exception as e:
        print e

def test_save():
    if isElement(driver, 'xpath', '//android.widget.TextView[contains(@text, "我的")]'):
        element1 = driver.find_element_by_xpath('//android.widget.FrameLayout')
        element2 = driver.find_element_by_xpath('//android.widget.FrameLayout//android.widget.TabHost')
        element3 = driver.find_element_by_xpath('//android.widget.FrameLayout//android.widget.TabHost//android.widget.TabWidget')
        element4 = driver.find_element_by_xpath('//android.widget.FrameLayout//android.widget.TabHost//android.widget.TabWidget//android.widget.RelativeLayout[contains(@index,3)]')
        element = driver.find_element_by_xpath('//android.widget.FrameLayout//android.widget.TabHost//android.widget.TabWidget//android.widget.RelativeLayout[contains(@index,3)]')
        element.click()

        element5 = driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "我的")]/../..')
        element5.click()

        element6 = driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "我的")]/parent::*/parent::android.widget.RelativeLayout')
        element6.click()

        # 等待编辑按钮出现
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "编辑")))

if __name__ == '__main__':
    test_save()
# import sys
#
# if __name__ == '__main__':
#     xml_report_path = "./allure-results"
#     html_report_path = "./allure-results/html"
#     # 开始测试
#     args = ['-s', '-q', '--alluredir', xml_report_path]
#     pytest.main(args)
#     # 生成html测试报告
#     cmd1 = 'allure generate %s -o %s' % (xml_report_path, html_report_path)
#     cmd2 = 'allure open ' + html_report_path
#     try:
#         Shell.invoke(cmd1)
#         Shell.invoke(cmd2)
#     except:
#         L.e("Html测试报告生成失败,确保已经安装了Allure-Commandline")


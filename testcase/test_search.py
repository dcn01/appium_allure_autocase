# coding: utf-8

from utils.operation import *
import pytest
import allure
from allure.constants import AttachmentType


class SearchFriend:

    driver = None

    @pytest.fixture(scope='session')
    def setDriver(self):
        self.driver = driver


    def test_search_recommend(self):
        '''
        根据推荐搜索
        :return:
        '''
        try:
            if isElement(self.driver, 'xpath', '//android.widget.TextView[contains(@text, "视频")]'):
                print('search by recommend testing now.')
                # 进入搜索页面
                self.driver.find_element_by_id('com.ss.android.ugc.live:id/search').click()
                time.sleep(2)
                # 滑动查看推荐用户
                swipeUp(500, 3)
                time.sleep(2)
                # 点击取消，退出搜索
                self.driver.find_element_by_id('com.ss.android.ugc.live:id/cancel_btn').click()
        except Exception as e:
            print e

    @allure.feature('搜索')
    @allure.issue('https://jira.bytedance.com/browse/ZHIBO-6887?filter=14391')
    def test_search_userid(self):
        '''
        根据用户 id 搜索
        :return:
        '''
        try:
            if isElement(self.driver, 'xpath', '//android.widget.TextView[contains(@text, "视频")]'):
                print('search by user id testing now.')
                with pytest.allure.step('进入搜索页面'):
                    # 进入搜索页面
                    self.driver.find_element_by_id('com.ss.android.ugc.live:id/search').click()
                    time.sleep(2)
                with pytest.allure.step('通过输入用户id查找好友'):
                    # 通过输入用户id查找好友
                    self.driver.find_element_by_id('com.ss.android.ugc.live:id/search_edit').send_keys('143274589')
                    allure.attach('截图', self.driver.get_screenshot_as_png(), type=AttachmentType.PNG)
                    time.sleep(3)
                    swipeUp(500, 3)
                    time.sleep(2)
                with pytest.allure.step('点击取消，退出搜索'):
                    # 点击取消，退出搜索
                    self.driver.find_element_by_id('com.ss.android.ugc.live:id/cancel_btn').click()
        except Exception as e:
            print e

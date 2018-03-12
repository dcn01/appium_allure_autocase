# coding: utf-8

from utils.envrionment import *
from utils.operation import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest



class EditInfo:

    driver = None

    def __init__(self, driver):
        self.driver = driver


    def test_save(self, test_setup):
        if test_setup:
            element = findElement(self.driver, "保存")
            element.click()
            element1 = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "没有任何修改"))
            )
        else:
            print '初始化失败'

    def setDriver(self, driver):
        self.driver = driver

    @pytest.fixture(scope='function')
    def test_setup(self):
        if isElement(self.driver, 'xpath', '//android.widget.TextView[contains(@text, "我的")]'):
            element = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "我的")]')
            element.click()
            # 等待编辑按钮出现
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "编辑")))
            return True
        else:
            return False



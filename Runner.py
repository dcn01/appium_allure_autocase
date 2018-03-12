# coding: utf-8
from testcase.test_editInfo import EditInfo
from testcase.test_search import SearchFriend
from multiprocessing import Pool
from utils.envrionment import *
from utils.shell import *
import pytest

def test_run():
    pool = Pool(len(devicesPool()))
    pool.map(runner, devicesPool())
    pool.close()
    pool.join()

def runner(device):
    #开启一个AppiumServer服务
    appiumServer = AppiumServer(device)
    if not appiumServer.start_server():
        print "start appium failed!"
        exit(-1)

    #获得一个driver
    driver = getDriver(device)

    #执行测试用例
    runnerTestCase(driver)

    #关闭AppiumServer服务
    appiumServer.stop_server()

def runnerTestCase(driver):
    # testEditInfo = EditInfo(driver)
    # testEditInfo.test_save(testEditInfo.test_setup())

    testSearch = SearchFriend()
    testSearch.setDriver(driver)
    testSearch.test_search_recommend()
    testSearch.test_search_userid()

# def testReport(dir):
#     Shell.invoke('rm -rf ./allure-results/')
#     xml_report_path = "./allure-results"
#     html_report_path = "./allure-results/html"
#     # 开始测试
#     args = [dir, '-s', '-q', '--alluredir', xml_report_path]
#     pytest.main(args)
#     # 生成html测试报告
#     cmd1 = 'allure generate %s -o %s' % (xml_report_path, html_report_path)
#     cmd2 = 'allure open ' + html_report_path
#     try:
#         Shell.invoke(cmd1)
#         Shell.invoke(cmd2)
#     except:
#         print("Html测试报告生成失败,确保已经安装了Allure-Commandline")

if __name__ == '__main__':
    Shell.invoke('rm -rf ./allure-results/')
    xml_report_path = "./allure-results"
    html_report_path = "./allure-results/html"
    # 开始测试
    args = ['Runner.py', '-s', '-q', '--alluredir', xml_report_path]
    pytest.main(args)
    # 生成html测试报告
    cmd1 = 'allure generate %s -o %s' % (xml_report_path, html_report_path)
    cmd2 = 'allure open ' + html_report_path
    try:
        Shell.invoke(cmd1)
        Shell.invoke(cmd2)
    except:
        print("Html测试报告生成失败,确保已经安装了Allure-Commandline")
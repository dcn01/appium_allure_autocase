# -*- coding: utf-8 -*-


import subprocess
import os

def getPhoneInfo(devices):
    cmd = "adb -s " + devices +" shell cat /system/build.prop "
    print(cmd)
    # phone_info = os.popen(cmd).readlines()
    phone_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = {}
    release = "ro.build.version.release=" # 版本
    model = "ro.product.model=" #型号
    brand = "ro.product.brand=" # 品牌
    device = "ro.product.device=" # 设备名
    for line in phone_info.stdout.readlines():
         for i in line.split():
            temp = i.decode('utf-8')
            if temp.find(release) >= 0:
                result["release"] = temp[len(release):]
                break
            if temp.find(model) >= 0:
                result["model"] = temp[len(model):]
                break
            if temp.find(brand) >= 0:
                result["brand"] = temp[len(brand):]
                break
            if temp.find(device) >= 0:
                result["device"] = temp[len(device):]
                break
    print(result)
    return result

class AndroidDebugBridge(object):
    def call_adb(self, command):
        command_result = ''
        command_text = 'adb %s' % command
        print(command_text)
        results = os.popen(command_text, "r")
        while 1:
            line = results.readline()
            if not line: break
            command_result += line
        results.close()
        return command_result

    # 检查设备
    def attached_devices(self):
        result = self.call_adb("devices")
        devices = result.partition('\n')[2].replace('\n', '').split('\tdevice')
        # flag = [device for device in devices if len(device) > 2]
        # if flag:
        #     return True
        # else:
        #     return False

        return [device for device in devices if len(device) > 2]
# -*- coding:utf-8 -*-

import time
from multiprocessing import Process
from api import app
from setting import *
from generator import *
from tester import *

class Scheduler(object):
    @staticmethod
    def valid_cookies(cycle=CYCLE):
        while True:
            print('Cookies检测器开始运行！')
            try:
                for website, cls in TESTER_MAP.items():
                    tester = eval(cls + '(website="' + website + '")')
                    tester.run()
                    print('Cookies检测完成')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def generator_cookies(cycle=CYCLE):
        while True:
            print('Cookies生成器开始运行！')
            try:
                for website, cls in GENERATOR_MAP.items():
                    generator = eval(cls + '(website="' + website + '")')
                    generator.run()
                    print('Cookies生成完成')
                    generator.close()
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        print('API接口开始运行!')
        app.run(host=API_HOST, port=API_PORT)
    
    def run(self):
        if API_ENABLE:
            api_process = Process(target=Scheduler.api)
            api_process.start()

        if GENERATOR_ENABLE:
            generator_process = Process(target=Scheduler.generator_cookies)
            generator_process.start()

        if VALID_ENABLE:
            valid_process = Process(target=Scheduler.valid_cookies)
            valid_process.start()

if __name__ == '__main__':
    myscheduler = Scheduler()
    myscheduler.run()
# -*- coding:utf-8 -*-

from multiprocessing import Process
import time
from setting import *
from getter import Getter
from api import app
from tester import Tester

class Scheduler():
    def getter_scheduler(self, cycle = GETTER_CYCLE):
        """
        定时获取代理
        """
        print('获取器开始执行！')
        getter = Getter()
        while True:
            getter.run()
            print('休息', GETTER_CYCLE, '秒')
            time.sleep(GETTER_CYCLE)

    def tester_scheduler(self, cycle = TESTER_CYCLE):
        """
        定时测试代理
        """
        print('测试器开始执行！')
        tester = Tester()
        while True:
            tester.run()
            print('休息', TESTER_CYCLE, '秒')
            time.sleep(TESTER_CYCLE)

    def api_scheduler(self):
        """
        开启API
        """
        app.run(host=API_HOST, port=API_PORT)

    def run(self):
        print('代理池开始运行！')
        if GETTER_ENABLED:
            getter_process = Process(target=self.getter_scheduler)
            getter_process.start()

        if TESTER_ENABLED:
            tester_process = Process(target=self.tester_scheduler)
            tester_process.start()

        if API_ENABLED:
            api_process = Process(target=self.api_scheduler)
            api_process.start()

def main():
    myscheduler = Scheduler()
    myscheduler.run()

if __name__ == '__main__':
    main()
    
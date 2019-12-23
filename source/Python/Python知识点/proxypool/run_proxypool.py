# -*- coding:utf-8 -*-
from scheduler import Scheduler

def main():
    try:
        my_scheduler = Scheduler()
        my_scheduler.run()
    except:
        main()
        
if __name__ == '__main__':
    main()
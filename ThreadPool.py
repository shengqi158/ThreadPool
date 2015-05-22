#!/usr/bin/env python
#coding=utf-8
#author liaoxinxi@nsfocus.com

from Queue import Queue,Empty
from threading import Thread
import traceback
import sys

DEBUG = True
def my_print(*args):
    if DEBUG:
        print args

class Worker(Thread):
    """工作线程类,完成任务执行和结果获取"""
    def __init__(self, work_queue, result_queue, timeout):
        my_print('init')
        Thread.__init__(self);
        self.setDaemon(True)
        self.state = None
        self.work_que= work_queue
        self.result_queue = result_queue
        self.timeout = timeout
        self.start()

    def run(self):
        while(True):
            my_print('while', self.getName())
            if self.state == 'stop':
                break
            try:
                my_print('get')
                task = self.work_que.get(timeout=self.timeout)
                my_print(task)
                func, args, kwargs = task
#                (func, args, kwargs) = self.work_que.get(timeout=self.timeout)#block func
                print 'func,args,kwargs', func, args, kwargs
            except Empty:
                my_print('continue')
                continue
            try:
                my_print('start func')
                my_print(args)
                my_print(kwargs)
                res = func(*args, **kwargs)
                print 'res',res
                result = {args:res}
                print 'result', result
                self.result_queue.put(result)
                self.work_que.task_done()
            except Exception,e:
                traceback.print_exc()
                my_print(e)
                break
    def stop(self):
        self.state = 'stop'



class ThreadPool():
    """创建一个线程池"""
    def __init__(self, thread_num, timeout):
        self.work_queue = Queue()
        self.result_queue = Queue()
        self.thread_pool = []
        self.thread_num = thread_num
        self.timeout = timeout

        self.start_thread_pool()

    def start_thread_pool(self):
        for i in range(self.thread_num):
            worker = Worker(self.work_queue, self.result_queue, self.timeout)
            self.thread_pool.append(worker)


    def add_task(self, func, *args, **kwargs):
        if not self.work_queue.full():
            self.work_queue.put(func, args, kwargs)

    def get_result(self):
        if not self.result_queue.empty():
            return self.result_queue.get()
        else:
            return None

    def task_done(self):
        return self.work_queue.task_done()

    def task_join(self):
        self.work_queue.join()

    def stop_thread_pool(self):
        for i in range(self.thread_num):
            self.thread_pool[i].stop()

        del self.thread_pool[:]

def test(num1, num2):
    print "after plus:",num1+num2
    return num1+num2

if __name__ == "__main__":
    task = (test,(1,2),{})
    work_queue = Queue()
    result_queue = Queue()
    timeout = 0.5
    worker = Worker(work_queue,result_queue, timeout)
    for i in range(4):
        work_queue.put(task)
        print result_queue.get()
    print 'queue size', work_queue.qsize()
    print 'queue size', result_queue.qsize()
    work_queue.join()
    #result_queue.join()
    worker.stop()
    sys.exit()
    threadpool = ThreadPool(5, 0.5)
    for i in range(10):
        threadpool.add_task(test,1,2)
    print threadpool.get_result()
    threadpool.task_join()


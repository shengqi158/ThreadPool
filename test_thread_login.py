#!env python
#coding=utf-8
# 
# 
# Created Time: 2013年07月19日 星期五 10时05分49秒
# 
# FileName:     test_thread_login.py
# 
# Description:  
# 
# ChangeLog:
import login
from ThreadPool import Worker, ThreadPool
from Queue import Queue

_DEBUG = False

def test_login():
    if _DEBUG:
        import pdb
        pdb.set_trace()
    handle = login.login('ssh', 'root', 'n', '10.20.60.23')
    #handle.execute_cmd('uname -a')
    task = (handle.execute_cmd, ('uname -a',), {})
    work_queue = Queue()
    result_queue = Queue()
    timeout = 0.5
    worker = Worker(work_queue, result_queue, timeout)
    for i in range(3):
        work_queue.put(task)
        print result_queue.get()
    work_queue.join()
    worker.stop()

def test_thread_pool():
    pool = ThreadPool(2, 0.5)
    for i in range(2):
        handle = login.login('ssh', 'root', 'n', '10.20.60.23')
        task = (handle.execute_cmd, ('uname -a',), {})
        pool.add_task(task)
    print pool.get_result()
    pool.task_join()
        
if __name__ == "__main__":
    
#    test_login()
    test_thread_pool()

import threading
import time


def func(arg, slp_time):
    loop = 10
    while loop > 0:
        loop -= 1
        print('I am {} - {}'.format(arg, loop))
        time.sleep(slp_time)

a=('1', 1)
b=('2', 0.5)
c=('3', 0.33)
t1 = threading.Thread(target = func, name = 't1', args=a)
t2 = threading.Thread(target = func, name = 't2', args=b)
t3 = threading.Thread(target = func, name = 't3', args=c)
t1.start()
t2.start()
t3.start()

t3.join()
print('3 stopped')
t2.join()
print('2 stopped')
t1.join()
while threading.active_count() > 1:
    print('waiting')
    time.sleep(1)


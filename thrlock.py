import threading
import time
from random import randint



def func(id, lock_, var_):
    #time.sleep(randint(1,1000)/1000)
    print('thread {} started'.format(id))
    loop = 0
    while loop < 1000:
        lock_.acquire()
        var_[0] += 1
        lock_.release()
        loop += 1
        print('inst {0} loop {1} var {2}'.format(id, loop, var_[0]))
        #time.sleep(randint(1,1200)/1000)
    


if "__main__" == __name__:
    var = [1]
    lock = threading.Lock()
    t1 = threading.Thread(target = func, args=('1', lock, var))
    t2 = threading.Thread(target = func, args=('2', lock, var))
    t1.start()
    t2.start()


    t1.join()
    t2.join()
    print('var={}'.format(var))

from threading import Thread
from time import sleep


def async2(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@async2
def A():
    sleep(10)
    print("函数A睡了十秒钟。。。。。。")
    print("a function")

@async2
def A2():
    sleep(5)
    print("函数A睡了5秒钟。。。。。。")
    print("a2 function")

def B():
    print("b function")


A()
A2()
B()
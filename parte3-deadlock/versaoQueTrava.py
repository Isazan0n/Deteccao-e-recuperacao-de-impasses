import threading
import time

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()

def thread1():
    LOCK_A.acquire()
    print("T1 adquiriu LOCK_A")
    time.sleep(0.05)
    LOCK_B.acquire()
    print("T1 concluiu")
    LOCK_B.release()
    LOCK_A.release()

def thread2():
    LOCK_B.acquire()
    print("T2 adquiriu LOCK_B")
    time.sleep(0.05)
    LOCK_A.acquire()
    print("T2 concluiu")
    LOCK_A.release()
    LOCK_B.release()

t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)

t1.start()
t2.start()

t1.join()
t2.join()

print("Programa concluiu")
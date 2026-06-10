import threading
import time

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()

# sempre adquirir LOCK_A antes de LOCK_B em todas as threads
def thread1():
    LOCK_A.acquire()
    LOCK_B.acquire()
    print("T1 concluiu")
    LOCK_B.release()
    LOCK_A.release()

def thread2():
    LOCK_A.acquire()  
    LOCK_B.acquire()
    print("T2 concluiu")
    LOCK_B.release()
    LOCK_A.release()

t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)

t1.start()
t2.start()

t1.join()
t2.join()

print("Programa concluiu")
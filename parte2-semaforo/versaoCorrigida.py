import threading
import time

count = 0
# semaforo binario só 1 thread por vez
sem = threading.Semaphore(1)  
T = 8
M = 200000

def tarefa():
    global count
    for i in range(M):
        sem.acquire()
        try:
            count = count + 1
        finally:
            # libera mesmo se der erro
            sem.release()  

threads = []
inicio = time.time()

for _ in range(T):
    t = threading.Thread(target=tarefa)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

fim = time.time()
print(f"Esperado : {T * M}")
print(f"Obtido   : {count}")
print(f"Tempo    : {fim - inicio:.4f} segundos")
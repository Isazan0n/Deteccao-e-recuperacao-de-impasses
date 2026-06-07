import threading
import time

count = 0
T = 8
M = 200000

def tarefa():
    global count
    for i in range(M):
        count = count + 1

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
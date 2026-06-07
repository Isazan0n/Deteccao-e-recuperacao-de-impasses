import threading
import time
import random

N = 5
garfos = [threading.Semaphore(1) for _ in range(N)]
estado = ["pensando"] * N

def filosofo(p):
    while True:
        # Pensando
        estado[p] = "pensando"
        print(f"Filósofo {p} está PENSANDO")
        time.sleep(random.uniform(0.5, 1.5))

        # Com fome
        estado[p] = "com fome"
        print(f"Filósofo {p} está COM FOME")

        # Pega garfo esquerdo depois direito
        garfos[p].acquire()                    
        time.sleep(0.1)                        
        garfos[(p + 1) % N].acquire()          

        # Comendo
        estado[p] = "comendo"
        print(f"Filósofo {p} está COMENDO")
        time.sleep(random.uniform(0.5, 1.5))

        # Solta os garfos
        garfos[(p + 1) % N].release()
        garfos[p].release()

threads = []
for i in range(N):
    t = threading.Thread(target=filosofo, args=(i,))
    t.daemon = True
    threads.append(t)
    t.start()

time.sleep(15)
print("Tempo encerrado.")
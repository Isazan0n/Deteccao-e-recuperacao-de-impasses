import threading
import time
import random

N = 5
garfos = [threading.Semaphore(1) for _ in range(N)]
estado = ["pensando"] * N

def filosofo(p):
    garfo_esquerda = p
    garfo_direita  = (p + 1) % N

    left  = min(garfo_esquerda, garfo_direita)
    right = max(garfo_esquerda, garfo_direita)

    while True:
        estado[p] = "pensando"
        print(f"Filósofo {p} está PENSANDO")
        time.sleep(random.uniform(0.5, 1.5))

        estado[p] = "com fome"
        print(f"Filósofo {p} está COM FOME")

        # adquirir(left)
        garfos[left].acquire()
        print(f"Filósofo {p} pegou garfo {left}")

        # adquirir(right)
        garfos[right].acquire()
        print(f"Filósofo {p} pegou garfo {right}")

        estado[p] = "comendo"
        print(f"Filósofo {p} está COMENDO")

        # comer()
        time.sleep(random.uniform(0.5, 1.5))

        # liberar(right)
        garfos[right].release()

        # liberar(left)
        garfos[left].release()

        estado[p] = "pensando"
        print(f"Filósofo {p} soltou os garfos")

threads = []
for i in range(N):
    t = threading.Thread(target=filosofo, args=(i,))
    t.daemon = True
    threads.append(t)
    t.start()

time.sleep(15)
print("Tempo encerrado.")
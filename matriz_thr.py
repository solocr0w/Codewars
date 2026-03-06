import threading, random, time, sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
THREADS = 4
A = [[random.random() for _ in range(N)] for _ in range(N)]
B = [[random.random() for _ in range(N)] for _ in range(N)]
C = [[0]*N for _ in range(N)]
def calcular(ini, fim):
    for i in range(ini, fim):
        for j in range(N):
            for k in range(N): C[i][j] += A[i][k] * B[k][j]
inicio = time.time()
lista_threads = []
passo = N // THREADS
for t in range(THREADS):
    ini = t * passo
    fim = N if t == THREADS-1 else (t+1)*passo
    th = threading.Thread(target=calcular, args=(ini, fim))
    lista_threads.append(th); th.start()
for th in lista_threads: th.join()
print(f"Threads N={N}: {(time.time()-inicio)*1000:.2f} ms")
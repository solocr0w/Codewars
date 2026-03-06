from mpi4py import MPI
import random, time, sys

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300

if rank == 0:
    A = [[random.random() for _ in range(N)] for _ in range(N)]
    B = [[random.random() for _ in range(N)] for _ in range(N)]
    inicio = time.time()
else:
    A = B = None

# Envia as matrizes para todos os containers
A = comm.bcast(A, root=0)
B = comm.bcast(B, root=0)

# Divide as linhas entre os processos
fatia = N // size
ini = rank * fatia
fim = N if rank == size - 1 else (rank + 1) * fatia

minha_parte = []
for i in range(ini, fim):
    linha = [0]*N
    for j in range(N):
        for k in range(N): linha[j] += A[i][k] * B[k][j]
    minha_parte.append(linha)

# Junta tudo no Master
resultado = comm.gather(minha_parte, root=0)

if rank == 0:
    print(f"Distribuído N={N}: {(time.time()-inicio)*1000:.2f} ms")
from random import *
import logging
import threading
import time

def print_matriz(matriz): # printa a matriz
    logging.info("Main    : Matriz =")
    for linha in matriz:
        logging.info(f"Main    :     {linha}")
    print()

def random_matriz(linha, coluna): # cria uma matriz com valores aleatórios
    matriz = [[0 for j in range(coluna)] for i in range(linha)]
    for i in range(linha):
        for j in range(coluna):
            matriz[i][j] = randint(1,3)
    return matriz

def thread_function(id, A, B, C, start, end, n):
    logging.info("Thread %s: starting", id)
    for i in range(start, end):
        for j in range(len(B[0])):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
            logging.info(f"Thread {id}: Vetor C na linha: {i} coluna: {j} recebe valor: {C[i][j]}")
    time.sleep(2)
    logging.info("Thread %s: finishing", id)

if __name__ == "__main__":
    M = int(input("Informe o tamanho de M da sua matriz: "))
    N = int(input("Informe o tamanho de N da sua matriz: "))
    P = int(input("Informe o tamanho de P da sua matriz: "))
    thread = int(input("Quantos threads deseja criar? "))
    A = random_matriz(M, N)
    B = random_matriz(N, P)
    C = [[0 for j in range(P)] for i in range(M)]

    start = end = 0
    extra = len(C) % thread # o resto da divisão de P pelo numero de threads vai resultar no valor de segmentos extras
    threads = [] #armazena os descritores das threads

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    for id in range(0,thread):
        if(extra != 0 and id < extra):
            segmento = len(C) // thread + 1
        else:
            segmento = len(C) // thread
        end += segmento 
        t = threading.Thread(target=thread_function, args=(id, A, B, C, start, end, N, )) #inicializa a thread, informa o nome da função e os parâmetros
        logging.info("Main    : before running thread")
        t.start()
        threads.append(t)
        logging.info("Main    : wait for the thread to finish")
        start = end

    for t in threads:
        t.join()

    print_matriz(A)
    print_matriz(B)
    print_matriz(C)
    logging.info("Main    : all done")
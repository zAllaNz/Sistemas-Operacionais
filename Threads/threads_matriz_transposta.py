from random import *
import logging
import threading
import time

def print_matriz(matriz, bool): # imprimir a matriz de entrada e a matriz transposta
    if(bool):
        logging.info("Main    : Matriz =")
    else:
        logging.info("Main    : Matriz Transposta =")
    for linha in matriz:
        logging.info(f"Main    :     {linha}")
    print()

def random_matriz(linha, coluna): # cria as matrizes com valores aleatórios
    matriz = [[0 for j in range(coluna)] for i in range(linha)]
    for i in range(linha):
        for j in range(coluna):
            matriz[i][j] = randint(0,10)
    return matriz

def thread_function(id, A, B, start, end): # função que recebe duas matrizes e faz a transposição dos elementos de acordo com o segmento
    logging.info("Thread %s: starting", id)
    for i in range(start, end):
        for j in range(len(A[0])):
            B[j][i] = A[i][j]
            logging.info(f"Thread {id}: Vetor C na linha: {i} coluna: {j} recebe valor: {B[j][i]}")
    time.sleep(2)
    logging.info("Thread %s: finishing", id)

if __name__ == "__main__":
    N = int(input("Informe o tamanho de linhas da sua matriz: "))
    M = int(input("Informe o tamanho de colunas da sua matriz: "))
    thread = int(input("Quantos threads deseja criar? "))
    A = random_matriz(N, M)
    B = [[0 for j in range(N)] for i in range(M)]

    start = end = 0
    extra = N % thread # divide o número de linhas da matriz pela quantidade de threads, o resto se torna os segmentos extras
    threads = [] #armazena os descritores das threads

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    for id in range(0,thread):
        if(extra != 0 and id < extra): # divide os segmentos extras para as primeiras threads, caso tenha extras e o id seja menor que o número de extras
            segmento = N // thread + 1
        else: ## Caso ele não seja, o segmento vai ser a divisão por inteiro do tamanho do vetor pelo número de threads
            segmento = N // thread
        end += segmento # define até o intervalor que a thread irá executar
        t = threading.Thread(target=thread_function, args=(id, A, B, start, end, )) #inicializa a thread, informa o nome da função e os parâmetros
        logging.info("Main    : before running thread")
        t.start()
        threads.append(t)
        logging.info("Main    : wait for the thread to finish")
        start = end # Start vai receber o valor de end

    for t in threads:
        t.join()

    print_matriz(A, True)
    print_matriz(B, False)
    logging.info("Main    : all done")
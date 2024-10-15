from random import *
import logging
import threading
import time

def print_matriz(matriz): # printa as operações realizadas pela thread
    logging.info("Main    : Matriz =")
    for linha in matriz:
        logging.info(f"Main    :     {linha}")
    print()

def random_matriz(linha, coluna): # cria uma matriz e atribui valores aleatórios no intervalo de 0 até 9
    matriz = [[0 for j in range(coluna)] for i in range(linha)]
    for i in range(linha):
        for j in range(coluna):
            matriz[i][j] = randint(0,10)
    return matriz

def thread_function(id, A, B, C, start, end): # função para thread realizar as operações nos segmentos definidos
    logging.info("Thread %s: starting", id)
    for i in range(start, end):
        for j in range(len(A[0])):
            C[i][j] = A[i][j] + B[i][j]
            logging.info(f"Thread {id}: Vetor C na linha: {i} coluna: {j} recebe valor: {C[i][j]}")
    time.sleep(2)
    logging.info("Thread %s: finishing", id)

if __name__ == "__main__":
    N = int(input("Informe o tamanho de linhas da sua matriz: "))
    M = int(input("Informe o tamanho de colunas da sua matriz: "))
    thread = int(input("Quantos threads deseja criar? "))
    A = random_matriz(N, M)
    B = random_matriz(N, M)
    C = [[0 for j in range(M)] for i in range(N)]

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
        t = threading.Thread(target=thread_function, args=(id, A, B, C, start, end, )) #inicializa a thread, informa o nome da função e os parâmetros
        logging.info("Main    : before running thread")
        t.start()
        threads.append(t)
        logging.info("Main    : wait for the thread to finish")
        start = end # Start vai receber o valor de end

    for t in threads:
        t.join()

    print_matriz(A)
    print_matriz(B)
    print_matriz(C)
    logging.info("Main    : all done")
from random import *
import logging
import threading
import time

def random_vector(tamanho): # função que cria vetores com o tamanho N e atribui valores aleatórios de 0 até 9
    vetor = [0] * tamanho
    for i in range(0, tamanho):
        vetor[i] = randint(0,10)
    return vetor

def thread_function(id, A, B, C, start, end): # função que realiza a soma dos vetores e armazena em C
    logging.info("Thread %s: starting", id)
    for i in range(start, end):
        C[i] = A[i] + B[i]
        logging.info(f"Thread {id}: Vetor C na posicao: {i} recebe valor: {C[i]}")
    time.sleep(2)
    logging.info("Thread %s: finishing", id)

if __name__ == "__main__":
    N = int(input("Informe o tamanho do vetor: "))
    thread = int(input("Quantos threads deseja criar? "))
    A = random_vector(N) # Cria vetores com tamanho N e valores aleatórios
    B = random_vector(N)
    C = [0] * N # cria um vetor C com tamanho N com valores 0

    start = end = 0 
    extra = N % thread # o resto da divisão de N pelo numero de threads serão tratados como extras
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

    logging.info(f"Main    : Vetor A: {A}")
    logging.info(f"Main    : Vetor B: {B}")
    logging.info(f"Main    : Vetor C: {C}")
    logging.info("Main    : all done")
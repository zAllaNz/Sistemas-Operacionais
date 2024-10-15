#João Gabriel Freitas Acosta - 155487 e Allan Machado Gonçalves - 134496

import logging
import threading
import time
import random

def cadeira_barbeiro():
    while True:
        lock.acquire()
        if(len(threads_fila) == 0): # caso não tenha ninguem na barbearia, o barbeiro tira um cochilo
            logging.info("Barbearia vazia, Barbeiro está tirando um cochilo.")
            lock.release()
            time.sleep(1)
        else:
            cliente = threads_fila.pop(random.randint(0, len(threads_fila) - 1))
            logging.info("Thread %s sentou na cadeira do barbeiro.", cliente)
            logging.info("Barbeiro está cortando cabelo da Thread %s.", cliente)
            lock.release()
            time.sleep(10)
            logging.info("Barbeiro finalizou o corte da Thread %s.", cliente)


def cadeira_espera(id, n):
    logging.info("Thread %s está na frente da barbearia.", id)
    if(len(threads_fila) < n and S.acquire(blocking=False)):  # Tenta ocupar uma cadeira caso esteja disponível
        logging.info("Thread %s conseguiu uma cadeira está esperando para cortar o cabelo.", id)
        lock.acquire()  # O cliente adquire o lock para acessar a fila
        threads_fila.append(id)  # Adiciona o cliente na fila
        print(f"clientes esperando {threads_fila}.")
        lock.release()
        S.release()
    else: # Caso não tenha cadeira disponível, ele vai embora
        logging.info("Sem cadeira disponível, Thread %s vai embora.", id)
        time.sleep(10)

if __name__ == "__main__":

    threads = [] #armazena os descritores das threads
    n = 3
    id = 1
    threads_fila = []
    S = threading.Semaphore(n)
    lock = threading.Lock()
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    barbeiro = threading.Thread(target=cadeira_barbeiro)
    barbeiro.start()
    threads.append(barbeiro)
    while True:
        time.sleep(random.randint(1, 10)) 
        t = threading.Thread(target=cadeira_espera, args=(id, n)) #inicializa a thread, informa o nome da função e os parâmetros
        t.start()
        threads.append(t)
        id += 1

    for t in threads:
        t.join()

    logging.info("Main    : all done")
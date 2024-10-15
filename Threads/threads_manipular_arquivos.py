import os
import logging
import threading
import time
import collections

## Faça um programa que, dado um diretório com arquivos de texto no formato .txt, calcule as seguintes estatísticas para cada arquivo. 
## Número de palavras, número de vogais, número de consoantes, palavra que apareceu mais vezes no arquivo, vogal mais frequente, consoante 
## mais frequente. Além disso, para cada arquivo do diretório, o programa deverá gerar um novo arquivo, contendo o conteúdo do arquivo 
## original escrito em letras maiúsculas.

def count_words(id, texto):
    palavras = texto.split()
    contagem_palavras = collections.Counter(palavras)
    most_freq = contagem_palavras.most_common(1)
    palavra, freq = most_freq[0]
    logging.info(f"Thread {id}: total palavras: {len(palavras)}")
    logging.info(f"Thread {id}: palavra mais comum: {palavra}, frequencia: {freq}")

def count_vogal(id, texto):
    vogal = ["a","e","i","o","u"]
    count = 0
    count_vogal = [0] * 5
    for char in texto:
        for i in range(len(vogal)):
            if(char.lower() == vogal[i]):
                count_vogal[i] += 1
                count += 1
                break           
    mais_frequente = max(count_vogal)
    pos = count_vogal.index(mais_frequente)
    logging.info(f"Thread {id}: número de vogais: {count}")
    logging.info(f"Thread {id}: a vogal mais frequente é: {vogal[pos]}, qntd: {mais_frequente}")

def count_cons(id, texto):
    count = 0
    cons = ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"]
    count_cons = [0] * len(cons)
    for char in texto:
        for i in range(len(cons)):
            if(char.lower() == cons[i]):
                count_cons[i] += 1
                count += 1
                break           
    mais_frequente = max(count_cons)
    pos = count_cons.index(mais_frequente)
    logging.info(f"Thread {id}: número de consoantes: {count}")
    logging.info(f"Thread {id}: a vogal mais frequente é: {cons[pos]}, qntd: {mais_frequente}")

def texto_upper(id, texto, lista, dir):
    upper = texto.upper()
    new_name = dir + "/upper_" + lista[id]
    with open(new_name, "w", encoding="utf-8") as arquivo:
        arquivo.write(upper)


def thread_function(id, arquivo, dir):
    logging.info("Thread %s: starting", id)
    with open(arquivo, "r", encoding="utf-8") as texto:
        conteudo = texto.read()
        count_words(id, conteudo)
        count_vogal(id, conteudo)
        count_cons(id, conteudo)
    texto_upper(id, conteudo, lista_arquivos, dir)

    time.sleep(2)
    logging.info("Thread %s: finishing", id)

if __name__ == "__main__":
    #Manipulação de arquivos
    diretorio = os.getcwd() + "/Sistemas Operacionais/Threads/arquivos"
    print(diretorio)
    lista_arquivos = os.listdir(diretorio)

    thread = len(lista_arquivos)
    start = end = 0
    segmento = thread // thread
    threads = [] #armazena os descritores das threads

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    for id in range(0,thread):
        caminho_texto = os.path.join(diretorio, lista_arquivos[id])
        end += segmento
        t = threading.Thread(target=thread_function, args=(id, caminho_texto, diretorio)) #inicializa a thread, informa o nome da função e os parâmetros
        logging.info("Main    : before running thread")
        t.start()
        threads.append(t)
        logging.info("Main    : wait for the thread to finish")
        start = end

    for t in threads:
        t.join()

    logging.info("Main    : all done")
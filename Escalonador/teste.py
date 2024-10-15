import random
import os
import logging
import threading
import time

class Processo:
    def __init__(self, nome, pid, tempo, prioridade):
        self.nome = nome
        self.pid = pid
        self.tempo = tempo
        self.tempo_restante = self.tempo
        self.tempo_final = None
        self.prioridade = prioridade

    def __str__(self):
        return f"Processo {self.nome}, PID: {self.pid}, Tempo de Execucao: {self.tempo}, Tempo Final: {self.tempo_final}, Prioridade: {self.prioridade}"

def gerador_processos(algoritmo, clock, numProcessos): # Cria processos com valores aleatórios de acordo com a entrada do usuário
    # Primeiro cria um arquivo txt com n processos informado pelo usuário, os valores são randomicos
    lista_processos = []
    pasta = os.path.abspath(__file__)
    diretorio = os.path.dirname(pasta) # procura o diretório onde este arquivo está
    caminho_arquivo = os.path.join(diretorio, "entrada_escalonador.txt")
    out = open(caminho_arquivo, 'w')
    out.write(algoritmo+"|"+str(clock)+"\n")
    for i in range (0, numProcessos):
        tempo = random.randrange(1,5)*clock
        prioridade = random.randrange(1, 100)
        out.write("processo-"+str(i)+"|"+str(i)+"|"+str(tempo)+"|"+str(prioridade)+"\n")
    out.close()

    # Divide o arquivo em linhas, a partir de cada linha (com excessão da primeira) é criado um processo novo e armazenado em uma lista
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    for linha in linhas[1:]:
        nome_processo, pid, tempo, prioridade = linha.strip().split('|')
        novo_processo = Processo(nome_processo, int(pid), int(tempo), int(prioridade))
        lista_processos.append(novo_processo)

    return lista_processos

def novo_processo(lista_processos, numProcessos):
    for i in range(numProcessos):
        print(f"Informe o nome do processo {i}")
        nome_processo = str(input())
        print(f"Informe o pid do processo {nome_processo}")
        pid = int(input())
        print(f"Informe o tempo de execução do processo {nome_processo}")
        tempo = int(input())
        print(f"Informe a prioridade do processo {nome_processo}")
        prioridade = int(input())
        novo_processo = Processo(nome_processo, pid, tempo, prioridade)
        lista_processos.append(novo_processo)
    return lista_processos

def alternancia_circular(lista_processos, clock): # o processo termina de executar e vai para o final da fila
    clock_total = 0
    n = len(lista_processos)
    i = 0
    while(True):
        count = 0
        if(lista_processos[i].tempo_restante != 0):
            print(f"O Processo {lista_processos[i].nome} está na CPU, falta {lista_processos[i].tempo_restante}ms para terminar a execução!")
            time.sleep(3)
            if(lista_processos[i].tempo_restante > clock): # Caso tempo restante seja maior que o clock
                clock_total += clock
                lista_processos[i].tempo_restante -= clock
            else: # se tempo restante for menor ou igual ao clock
                clock_total += lista_processos[i].tempo_restante
                lista_processos[i].tempo_restante = 0
                lista_processos[i].tempo_final = clock_total
        else: # contador para verificar se há algum processo para executar
            count += 1
            if(count == n):
                return lista_processos
        n = len(lista_processos)
        ##########teste
        print("\n")
        for j in range(len(lista_processos)):
            print(lista_processos[j])
        print("\n")
        i = i + 1
        if(i == n):
            i = 0
    

                
def prioridade(lista_processos):
    clock_total = 0
    n = len(lista_processos)
    while(True):
        maior_prioridade = 101
        pos = n
        # escolhendo o processo com maior prioridade
        for i in range(len(lista_processos)):
            if((lista_processos[i].prioridade < maior_prioridade) and (lista_processos[i].tempo_restante != 0)):
                maior_prioridade = lista_processos[i].prioridade
                pos = i
        
        # Caso a pos seja diferente do tamanho da lista, execute o processo nessa posição
        if(pos != n):
            print(f"O Processo {lista_processos[pos].nome} está na CPU, falta {lista_processos[pos].tempo_restante}ms para terminar a execução!")
            time.sleep(2)
            clock_total += lista_processos[pos].tempo_restante
            lista_processos[pos].tempo_final = clock_total
            lista_processos[pos].tempo_restante = 0
        else: # caso pos seja um valor fora do intervalo da lista, significa que a lista não possui mais processos para executar
            return lista_processos
        
def loteria(lista_processo, clock):
    clock_total = 0
    bilhetes = []

    # Distribui os bilhetes para cada processo
    for processo in lista_processo:
        bilhetes.extend([processo] * processo.prioridade)

    while True:
        # Verifica se todos os processos foram concluídos
        if all(processo.tempo_restante == 0 for processo in lista_processo):
            break
        
        # Sorteia um bilhete vencedor
        vencedor = random.choice(bilhetes)
        
        print(f"Processo vencedor: {vencedor.nome}")

        # Executa o processo vencedor
        if vencedor.tempo_restante > 0:
            tempo_executado = min(vencedor.tempo_restante, clock)
            clock_total += tempo_executado
            vencedor.tempo_restante -= tempo_executado

            # Atualiza o tempo final se o processo terminar
            if vencedor.tempo_restante == 0:
                vencedor.tempo_final = clock_total  

            print(f"Processo em execução: {vencedor.nome}")
            print(f"Tempo total: {clock_total}, Tempo restante do processo: {vencedor.tempo_restante}\n")

    return lista_processo

def thread_function(threads, id, alg,  lista_processos, clock):
    logging.info("Thread %s: starting", id)
    if(id == 1): # thread responsável por criar novos processos durante a execução do código
        while(threads[0].is_alive() == True):
            criar_processo = None
            criar_processo = str(input())
            if(criar_processo != None and threads[0].is_alive() == True):
                nome_processo, pid, tempo, priorid = criar_processo.strip().split('|')
                novo_processo = Processo(nome_processo, int(pid), int(tempo), int(priorid))
                print("novo processo criado")
                lista_processos.append(novo_processo)
        pass
    else:
        # Chamando a função do algoritmo escolhido pelo usuário
        if(alg == 1):
            lista_processos = alternancia_circular(lista_processos, clock)
        elif(alg == 2):
            lista_processos = prioridade(lista_processos)
        elif(alg == 3):
            lista_processos = loteria(lista_processos, clock)
        else:
            pass

        # Mostra os resultados para o usuário
        print("\nFinal da execução do Algoritmo")
        for i in range(len(lista_processos)):
            print(lista_processos[i])

    logging.info("Thread %s: finishing", id)
    pass

if __name__ == "__main__":
    lista_algoritmos = ["alternancia_circular", "prioridade", "loteria", "CFS"]
    print("Bem-vindo ao gerador de arquivos de entrada para o escalonador!")
    print("Escolha o algoritmo: 1: alternancia circular, 2: prioridade, 3: loteria, 4: CFS")
    alg = int(input())
    print("Informe a fracao de CPU que cada processo tera direito por vez")
    clock = int(input())
    print("Informe o numero de processos a serem criados")
    numProcessos = int(input())
    
    # Verificando o algoritmo escolhido, caso seja um número diferente do intervalo de 1 a 4 encerra o programa
    if(alg >= 1 and alg <= 4):
        algoritmo = lista_algoritmos[alg - 1]
        lista_processos = gerador_processos(algoritmo, clock, numProcessos)
    else:
        print("O algoritmo informado nao existe")
        exit()

    # Inicializando as threads
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main    : before creating thread")
    threads = []
    logging.info("Main    : wait for the thread to finish")
    for id in range(2):
        t = threading.Thread(target=thread_function, args=(threads, id, alg,  lista_processos, clock, )) #inicializa a thread, informa o nome da função e os parâmetros
        logging.info("Main    : before running thread")
        threads.append(t)
        t.start()
        logging.info("Main    : wait for the thread to finish")
    
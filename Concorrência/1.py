#Em uma mesa circular N filósofos estão sentados. Em frente a cada filósofo há um prato e ao lado de cada prato há
#somente um hashi para que os filósofos possam comer macarrão. Para comer, um filósofo precisa pegar dois hashis, 
#que estão localizados a sua esquerda e a sua direita, respectivamente. Note que um filósofo compartilha os hashis
#com os filósofos sentados ao seu lado. Sua tarefa é desenvolver um algoritmo que coordene o processo de comer e pensar 
#de um filósofo. Caso um filósofo não consiga pegar os dois hashis, ele deverá deixar os hashis novamente na mesa para 
#evitar a ocorrência de impasses e inanição e pensar. Após terminar de pensar, ele deverá tentar comer novamente.
#(1,0 ponto)

#João Gabriel Freitas Acosta - 155487 e Allan Machado Gonçalçalves - 134496

import threading
import time
import random
import logging 

# Configuração básica do logger
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(threadName)s - %(message)s', 
    handlers=[logging.StreamHandler()]
)

# Função para coletar informações dos filósofos e o número máximo de refeições
def coletar_dados_dos_processos():
    # Usuário define quantos filósofos estão na mesa
    while True:
        n_filosofos = int(input("Quantos filósofos estão na mesa? "))
        if n_filosofos > 0:
            break
        else:
            logging.info("Digite um número válido maior que 0.")

    # Usuário define os nomes dos filósofos
    nomes_dos_filósofos = []
    for i in range(n_filosofos):
        nome = input(f"Digite o nome do filósofo {i + 1}: ")
        nomes_dos_filósofos.append(nome)

    # Usuário define o número máximo de refeições
    while True:
     max_refeicoes = int(input("Digite o número máximo de refeições para cada filósofo: "))
     if max_refeicoes > 0:
         break
     else:
         logging.info("Digite um número válido maior que 0.")


    # Retorna o número de filósofos, os nomes definidos e o número máximo de refeições
    return n_filosofos, nomes_dos_filósofos, max_refeicoes

# Função para simular o jantar dos filósofos com limite de refeições
def jantar(filosofo_id, nome, hashis, max_refeicoes):
    refeicoes = 0

    if len(hashis) == 1: 
        logging.info(f"{nome} pensou e concluiu que não dá pra comer com um só hashi")
        return 

    while refeicoes < max_refeicoes:
        # O filósofo pensa
        logging.info(f"{nome} está pensando.")
        time.sleep(random.randint(1,10))

        # Definindo os recursos (hashis esquerdo e direito)
        hashi_esquerdo = hashis[filosofo_id]
        hashi_direito = hashis[(filosofo_id + 1) % len(hashis)]

        # Um processo disputa os recursos (pegar dois hashis)
        logging.info(f"{nome} está tentando pegar os dois hashis.")
        doisHashis = False

        # Pega o hashi da esquerda
        with hashi_esquerdo:
            logging.info(f"{nome} pegou o hashi à esquerda.")
            # Tenta pegar o hashi da direita sem bloquear indefinidamente
            if hashi_direito.acquire(blocking=False):
                try:
                    logging.info(f"{nome} pegou o hashi à direita e agora está comendo.")
                    # Filósofo come
                    time.sleep(random.randint(1,10))
                    doisHashis = True
                    # Incrementa o contador de refeições
                    refeicoes += 1
                    logging.info(f"{nome} terminou de comer pela {refeicoes}ª vez.")
                finally:
                    # Libera o hashi da direita após comer
                    hashi_direito.release()
            else:
                # Se não conseguiu pegar o hashi da direita, deve liberar o hashi da esquerda
                logging.info(f"{nome} não conseguiu pegar ambos os hashis e vai pensar novamente.")
        
        # Se não conseguiu pegar ambos os hashis, volta a pensar
        if not doisHashis:
            continue

    logging.info(f"{nome} terminou suas refeições e está satisfeito!")

# Coletar o número de filósofos, seus nomes e o número máximo de refeições
num_filosofos, nomes_filosofos, max_refeicoes = coletar_dados_dos_processos()

# Criação dos hashis como locks
hashis = [threading.Lock() for i in range(num_filosofos)]

# Criação das threads para cada filósofo
filosofos = []
for i in range(num_filosofos):
    nome = nomes_filosofos[i]
    filosofo_thread = threading.Thread(target=jantar, args=(i, nome, hashis, max_refeicoes))
    filosofos.append(filosofo_thread)

# Iniciar todas as threads
for filosofo in filosofos:
    filosofo.start()

# Aguardar que todas as threads terminem
for filosofo in filosofos:
    filosofo.join()

if len(hashis) > 1:
  logging.info("Todos os filósofos terminaram suas refeições.")







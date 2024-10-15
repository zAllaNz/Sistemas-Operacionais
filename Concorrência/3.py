#João Gabriel Freitas Acosta - 155487 e Allan Machado Gonçalves - 134496


import threading
import random
import time
import logging

# Configuração básica do logger
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(threadName)s - %(message)s', # Formato das mensagens
    handlers=[
        logging.StreamHandler()  # Exibe os logs no console
    ]
)

class ContaCorrente:
    def __init__(self, identificador, saldoDisponivel, creditoDisponivel):
        self.identificador = identificador
        self.saldoDisponivel = saldoDisponivel
        self.creditoDisponivel = creditoDisponivel
        self.mutexGuardiao = threading.Lock() # faz um mutex pra cada conta 
        self.consulta_semaforo = threading.Semaphore(5)  # Permite até 5 consultas simultâneas

    # Operação 1: Creditar
    def creditar(self, valor):
        with self.mutexGuardiao: # a função with "pega" o mutex e  libera do mutex automaticamente após a execução da função
            if self.creditoDisponivel >= valor:
                self.creditoDisponivel -= valor
                logging.info(f"Conta {self.identificador}: Crédito usado de {valor}. Crédito atual: {self.creditoDisponivel}")
            else:
                logging.warning(f"Conta {self.identificador}: Não tem crédito suficiente para crédito de {valor}. Crédito atual: {self.creditoDisponivel}")

    # Operação 2: Aumentar Crédito
    def colocarCredito(self, valor):
        with self.mutexGuardiao:
            self.creditoDisponivel += valor
            logging.info(f"Conta {self.identificador}: Crédito aumentado em {valor}. Crédito atual: {self.creditoDisponivel}")

    # Operação 3: Debitar
    def debitar(self, valor):
        with self.mutexGuardiao:
            if self.saldoDisponivel >= valor:
                self.saldoDisponivel -= valor
                logging.info(f"Conta {self.identificador}: Débito de {valor}. Saldo atual: {self.saldoDisponivel}")
            else:
                logging.warning(f"Conta {self.identificador}: Saldo insuficiente para débito de {valor}. Saldo atual: {self.saldoDisponivel}")

    # Operação 4: Aumentar Saldo
    def colocarSaldo(self, valor):
        with self.mutexGuardiao:
            self.saldoDisponivel += valor
            logging.info(f"Conta {self.identificador}: Saldo aumentado em {valor}. Saldo atual: {self.saldoDisponivel}")


    # Operação 5: Consultar Saldo (até 5 simultâneos)
    def consultarSaldo(self):
        with self.consulta_semaforo:
            logging.info(f"Conta {self.identificador}: saldo atual: {self.saldoDisponivel}")
            time.sleep(1)
def operacao_bancaria(contas):
    while True:
        conta = random.choice(contas)  # Seleciona aleatoriamente uma conta
        tipoOperacao = random.choice(['creditar', 'colocarCredito', 'debitar', 'colocarSaldo', 'consultarSaldo'])
        valor = random.randint(1, 100)  # Valor aleatório entre 1 e 100

        if tipoOperacao == 'creditar':
            conta.creditar(valor)
        elif tipoOperacao == 'debitar':
            conta.debitar(valor)
        elif tipoOperacao == 'colocarCredito':
            conta.colocarCredito(valor)
        elif tipoOperacao == 'colocarSaldo':
            conta.colocarSaldo(valor)
        elif tipoOperacao == 'consultarSaldo':
            conta.consultarSaldo()    

        time.sleep(5)  # Intervalo entre operações

if __name__ == "__main__":
    # Criar múltiplas contas
    contas = [
        ContaCorrente(1, 500, 300),
        ContaCorrente(2, 700, 500),
        ContaCorrente(3, 1000, 200)
    ]

    # Criar múltiplas threads para simular operações em paralelo
    threads = []
    for i in range(8):  
        t = threading.Thread(target=operacao_bancaria, args=(contas,), name=f"Thread-{i+1}")
        threads.append(t)
        t.start()

    # Esperar um tempo para as operações ocorrerem
    time.sleep(10)  

    # Parar as threads após fazer uma função
    for t in threads:
        t.join() 

import random

class Processo:
    def __init__(self, nome, pid, tempo, prioridade):
        self.nome = nome
        self.pid = pid
        self.tempo = tempo
        self.tempo_restante = tempo
        self.tempo_final = None
        self.prioridade = prioridade

    def __str__(self):
        return f"Processo {self.nome}, PID: {self.pid}, Tempo de Execução: {self.tempo}, Tempo Final: {self.tempo_final}, Bilhete: {self.prioridade}"

#processo numero 1 
def alternancia_circular(lista_processo, clock):
    clock_total = 0
    n = len(lista_processo)
    while True:
        count = 0
        for processo in lista_processo:
            if processo.tempo_restante > 0:
                if processo.tempo_restante > clock:
                    clock_total += clock
                    processo.tempo_restante -= clock
                else:
                    clock_total += processo.tempo_restante
                    processo.tempo_restante = 0
                    processo.tempo_final = clock_total
            else:
                count += 1
        if count == n:
            return lista_processo

#processo numero 3
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

def criar_processos(num_processos, alg):
    lista_processos = []
    for i in range(num_processos):
        nome_processo = input(f"Informe o nome do processo {i}: ")
        pid = int(input(f"Informe o PID do processo {nome_processo}: "))
        tempo = int(input(f"Informe o tempo de execução do processo {nome_processo}: "))
        bilhete = None
        if alg == 3:
            bilhete = int(input(f"Informe o número de bilhetes do processo {nome_processo}: "))
        novo_processo = Processo(nome_processo, pid, tempo, bilhete)
        lista_processos.append(novo_processo)
    return lista_processos

if __name__ == "__main__":
    print("Bem-vindo ao gerador de arquivos de entrada para o escalonador!")
    print("Escolha o algoritmo: 1: alternância circular, 2: prioridade, 3: loteria, 4: CFS")
    alg = int(input())
    print("Informe a fração de CPU que cada processo terá direito por vez")
    clock = int(input())
    print("Informe o número de processos a serem criados")
    numProcessos = int(input())

    lista_processos = criar_processos(numProcessos, alg)

    if alg == 1:
        lista_processos = alternancia_circular(lista_processos, clock)
        algoritmo_selecionado = "alternância circular"
    elif alg == 2:
        algoritmo_selecionado = "prioridade"
    elif alg == 3:
        lista_processos = loteria(lista_processos, clock)
        algoritmo_selecionado = "loteria"
    elif alg == 4:
        algoritmo_selecionado = "CFS"
    else:
        print("O algoritmo informado não existe")
        exit()

    with open("entradaEscalonador.txt", 'w') as out:
        out.write(f"Escalonador: {algoritmo_selecionado} | Fração de CPU: {clock}\n")
        for processo in lista_processos:
            out.write(f"{processo}\n")

class Processo:
    def __init__(self, nome, pid, tempo, prioridade):
        self.nome = nome
        self.pid = pid
        self.tempo = tempo
        self.tempo_restante = self.tempo
        self.tempo_final = None
        self.prioridade = prioridade

    def __str__(self):
        return f"Processo {self.nome}, PID: {self.pid}, Tempo Final: {self.tempo_final}"

def alternancia_circular(lista_processo, clock):
    clock_total = 0
    n = len(lista_processo)
    while(True):
        count = 0
        for i in range(len(lista_processo)):
            if(lista_processo[i].tempo_restante != 0): # tr 5 cl 5 ct 0
                if(lista_processo[i].tempo_restante > clock): 
                    clock_total += clock
                    lista_processo[i].tempo_restante -= clock
                else:
                    clock_total += lista_processo[i].tempo_restante
                    lista_processo[i].tempo_restante = 0
                    lista_processo[i].tempo_final = clock_total
            else:
                count += 1
                if(count == n):
                    return lista_processo
            

                

clock = 5
lista = []
teste2 = []
teste = Processo("john",123,5,5)
lista.append(teste)
teste = Processo("gusta",133,30,5)
lista.append(teste)
teste = Processo("all",145,3,5)
lista.append(teste)
teste2 = alternancia_circular(lista, clock)
print(lista)
for j in range(len(teste2)):
        print(teste2[j])
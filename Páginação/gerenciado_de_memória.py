import os

class Processo:
    def __init__(self, nome_processo, pid, tempo, prioridade, qntd_memoria, sequencia_acesso):
        self.nome_processo = nome_processo
        self.pid = pid
        self.tempo = tempo
        self.tempo_restante = self.tempo
        self.tempo_final = None
        self.prioridade = prioridade
        self.qntd_memoria = qntd_memoria
        self.sequencia_acesso = sequencia_acesso
        self.seq_teste = list(sequencia_acesso)
        self.start = 0
        self.end = 0
        self.memoria_local = []

    def __repr__(self):
        return f"Processo {self.nome_processo}, PID: {self.pid}, Tempo de Execucao: {self.tempo}, Tempo Final: {self.tempo_final}, Prioridade: {self.prioridade}, Quantidade de memória: {self.qntd_memoria}, Sequencia de Acesso: {self.sequencia_acesso}"

    def get_nome(self):
        return self.nome_processo

    def decrease_tempo_restante(self, clock):
        self.tempo_restante -= clock

    def get_tempo_restante(self):
        return self.tempo_restante
    
    def set_tempo_restante(self, clock):
        self.tempo_restante = clock

    def set_tempo_final(self, clock):
        self.tempo_final = clock

    def set_start(self, aux):
        self.start += aux

    def get_start(self):
        return self.start
    
    def set_end(self, aux):
        self.end += aux

    def get_end(self):
        return self.end
    
    def get_pag(self, pos):
        return self.sequencia_acesso[pos]
    
    def get_qntd_pag(self):
        return self.qntd_memoria
    
    def teste(self):
        self.seq_teste.pop(0)
        #print(self.seq_teste)
    
    def lenght_seq_acesso(self):
        return len(self.sequencia_acesso)
    
    def append_memoria_local(self, pos):
        self.memoria_local.append(pos)
        # print(self.memoria_local)
    
    def pop_memoria_local(self, pos):
        aux = self.memoria_local[pos]
        self.memoria_local.pop(pos)
        return aux
    
    def reset_memoria_local(self):
        self.memoria_local = []

class Memoria:
    def __init__(self, politica, qntd_memoria):
        self.politica = politica
        self.memoria_fisica = []
        self.qntd_memoria = qntd_memoria
        self.troca_pag = 0
        self.clock = 5
        self.acesso = 2

    def __repr__(self):
        return self.memoria_fisica
    
    def get_troca_pag(self):
        return self.troca_pag
    
    def get_memoria_fisica(self):
        return self.memoria_fisica
    
    def reset_memoria(self, processo):
        tam = processo.get_qntd_pag()
        for i in range(1, tam+1):
            pag = processo.get_nome() + "|" + str(i)
            #print(pag)
            if (pag in self.memoria_fisica):
                self.memoria_fisica.remove(pag)

    def alocacao(self, processo, pos, lista_processos):
        pagina = processo.get_nome() + "|" + str(processo.get_pag(pos))
        #str(lista_processos[i].get_nome()) + "|" + str(lista_processos[i].sequencia_acesso[j]),
        if(pagina not in self.memoria_fisica):
            self.troca_pag += 1
            if(len(self.memoria_fisica) < qntd_moldura): #first fit
                self.memoria_fisica.append(pagina)
                print(f"Página: {str(processo.get_pag(pos))} do processo: {processo.get_nome()} foi alocado na memória")
                if(self.politica == "local"):
                    processo.append_memoria_local(processo.get_pag(pos))
            elif(len(self.memoria_fisica) >= qntd_moldura):
                self.otimo(processo, pos, lista_processos)
        else:
            print(f"Página: {pagina} já está na memória física!")

    def fifo(self, processo, pos):
        pagina = processo.get_nome() + "|" + str(processo.get_pag(pos))
        if(self.politica == "global"):
            print(f"Página {pagina} substituiu a página {self.memoria_fisica[0]} na memória física")
            self.memoria_fisica.pop(0)
            self.memoria_fisica.append(pagina)
        elif(self.politica == "local"):
            # Removendo a primeira pagina da memoria local e inserindo a nova pagina no final da memoria
            aux = processo.pop_memoria_local(0)
            processo.append_memoria_local(processo.get_pag(pos))
            # Removendo a pagina da memoria fisica e adicionando a nova
            self.memoria_fisica.remove(processo.get_nome() + "|" + str(aux))
            print(f"Página {pagina} substituiu a página {processo.get_nome() + "|" + str(aux)} na memória física")
            self.memoria_fisica.append(pagina)

    def nuf(self):
        pass

    def otimo(self, processo, pos, lista_processos):
        processo_subs = processo.get_nome() + "|" + str(processo.get_pag(pos))
        if(self.politica == "global"):
            tempo = {}
            for i, pagina in enumerate(self.memoria_fisica):
                partes = pagina.split('|')
                pag = int(partes[1])
                proc = int(partes[0].split('-')[1])
                if(pag in lista_processos[proc].seq_teste):
                    indice = lista_processos[proc].seq_teste.index(pag)
                    tempo[pag] = (indice, i)
                else:
                    tempo[pag] = (float('inf'), i)
            maior = max(tempo, key=lambda x: tempo[x][0])
            subs = tempo[maior][1]
            print(f"Página {processo_subs} substituiu a página {self.memoria_fisica[subs]} na memória física")
            self.memoria_fisica[subs] = processo_subs
        elif(self.politica == "local"):
            lista_aux = []
            for elemento in self.memoria_fisica:
                if elemento.startswith(processo.get_nome()):
                    lista_aux.append(elemento)
            tempo = {}
            for i, pagina in enumerate(lista_aux):
                partes = pagina.split('|')
                pag = int(partes[1])
                proc = int(partes[0].split('-')[1])
                if(pag in lista_processos[proc].seq_teste):
                    indice = lista_processos[proc].seq_teste.index(pag)
                    tempo[pag] = (indice, i)
                else:
                    tempo[pag] = (float('inf'), i)
            maior = max(tempo, key=lambda x: tempo[x][0])
            subs = processo.get_nome() + "|" + str(maior)
            if(subs in self.memoria_fisica):
                indice = self.memoria_fisica.index(subs)
                print(f"Página {processo_subs} substituiu a página {self.memoria_fisica[indice]} na memória física")
                self.memoria_fisica[indice] = processo_subs

def entrada_arquivo():
    lista_processos = []
    diretorio = os.path.abspath(__file__) # diretório onde encontrasse o arquivo
    pasta = os.path.dirname(diretorio) # pasta onde está localizado o arquivo
    caminho_arquivo = os.path.join(pasta, "entrada_escalonador.txt")
    # Separando cada linha do arquivo em uma posição da lista
    with open(caminho_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
    # Configurando o ambiente
    algoritmo, clock, politica, tam_memoria, tam_pag_moldura, percentual_aloc, acesso_por_ciclo = linhas[0].strip().split('|')
    # Criando os processos a partir da primeira linha
    for linha in linhas[1:]:
        nome_processo, pid, tempo, prioridade, qntd_memoria, sequencia_acesso = linha.strip().split('|')
        sequencia_acesso = sequencia_acesso.strip().split(" ") # transformando os elementos da sequencia de acesso em uma lista
        sequencia_acesso = list(map(int, sequencia_acesso)) # convertendo os elementos de str para int
        aux = int(qntd_memoria) / int(tam_pag_moldura)
        novo_processo = Processo(nome_processo, int(pid), int(tempo), int(prioridade), int(aux), sequencia_acesso)
        lista_processos.append(novo_processo)
    return algoritmo, int(clock), politica, int(tam_memoria), int(tam_pag_moldura), int(percentual_aloc), int(acesso_por_ciclo), lista_processos

def alternancia_circular(lista_processos, clock, memoria_fisica, acesso):
    clock_total = 0
    n = len(lista_processos)
    ciclo_atual = 0 
    while(True):
        count = 0
        for i in range(len(lista_processos)):
            if(lista_processos[i].get_tempo_restante() != 0):
                print("-------------------------------------------------------------")
                print(f"O Processo {lista_processos[i].nome_processo} está na CPU, faltam {lista_processos[i].get_tempo_restante()}ms para terminar a execução!")
                aux = clock
                if(lista_processos[i].get_tempo_restante() > clock): 
                    clock_total += clock
                    lista_processos[i].decrease_tempo_restante(clock)
                else:
                    aux = lista_processos[i].get_tempo_restante()
                    clock_total += aux
                    lista_processos[i].decrease_tempo_restante(aux)
                    lista_processos[i].set_tempo_final(clock_total)
                # percorre a lista da sequencia de acesso dependendo dos acessos por ciclo
                lista_processos[i].set_end(aux)
                start, end = lista_processos[i].get_start() * acesso, lista_processos[i].get_end() * acesso
                for j in range(start, end):
                    #print(f"pag process: {lista_processos[i].get_pag(j)}")
                    memoria_fisica.alocacao(lista_processos[i], j, lista_processos)
                    lista_processos[i].teste()
                    ciclo_atual += 1 
                lista_processos[i].set_start(aux)
                print(f"Memória física: {memoria_fisica.get_memoria_fisica()}")
                # Caso termine o tempo de execução do processo, resete a memoria local e tire suas paginas da memoria física
                if(lista_processos[i].get_tempo_restante() == 0):
                    print(f"Processo {lista_processos[i].get_nome()} terminou de executar, removendo suas páginas da memória física")
                    lista_processos[i].reset_memoria_local()
                    memoria_fisica.reset_memoria(lista_processos[i])
            else:
                count += 1
                if(count == n):
                    return lista_processos

if __name__ == "__main__":
    lista_troca_pag = []
    algoritmo, clock, politica, tam_memoria, tam_pag_moldura, percentual_aloc, acesso_por_ciclo, lista_processos = entrada_arquivo()
    qntd_moldura = int((tam_memoria//tam_pag_moldura) * (percentual_aloc/100))
    memoria_fisica = Memoria(politica, qntd_moldura)
    lista_processos = alternancia_circular(lista_processos, clock, memoria_fisica, acesso_por_ciclo)
    lista_troca_pag.append(memoria_fisica.get_troca_pag())
    print(f"Quantidade de trocas de páginas: {memoria_fisica.get_troca_pag()}")
    print("------------------------------------------")
    
    for i in range(len(lista_processos)):
        print(lista_processos[i])

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
        self.freq_paginas = {} # para o mru  e nuf 

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
        
    def append_memoria_local(self, pos):
       self.memoria_local.append(pos)
       self.freq_paginas[pos] = 1  # Inicia a contagem de frequência local

    def pop_memoria_local(self, pos):
        aux = self.memoria_local[pos]
        self.memoria_local.pop(pos)
        if aux in self.freq_paginas:
            del self.freq_paginas[aux]  # Remove da frequência local
        return aux
    
    def update_frequencia_local(self, pagina):
        # Atualiza a frequência da página local ao processo
        if pagina in self.freq_paginas:
            self.freq_paginas[pagina] += 1
        else:
            self.freq_paginas[pagina] = 1    

class Memoria:
    def __init__(self, politica, qntd_memoria):
        self.politica = politica
        self.memoria_fisica = []
        self.qntd_memoria = qntd_memoria
        self.troca_pag = 0
        self.usoPagina = [] #lista que mantem a ordem de uso 
        self.frequencia = {} #guarda a frequencia de cada pagina


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

    def alocacao(self, processo, pos, lista_processos, alg):
        pagina = processo.get_nome() + "|" + str(processo.get_pag(pos))
        #str(lista_processos[i].get_nome()) + "|" + str(lista_processos[i].sequencia_acesso[j]),
        if(pagina not in self.memoria_fisica):
            self.troca_pag += 1
            if(len(self.memoria_fisica) < qntd_moldura): #first fit
                self.memoria_fisica.append(pagina)
                self.usoPagina.append(pagina)
                self.frequencia[pagina] = 1  # Inicializa a contagem de acessos
                print(f"Página: {str(processo.get_pag(pos))} do processo: {processo.get_nome()} foi alocado na memória")
                if(self.politica == "local"):
                    processo.append_memoria_local(processo.get_pag(pos))
            elif(len(self.memoria_fisica) >= qntd_moldura):
                if(alg == "fifo"):
                    self.fifo(processo, pos)
                elif(alg == "nuf"):
                    self.nao_usado_frequentemente(processo, pos)
                elif(alg == "mru"):
                    self.menos_recentemente_usada(processo, pos)
                elif(alg == "otimo"):
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

    # implementação do algoritmo NUF
    def nao_usado_frequentemente(self, processo, pos):
        pagina = processo.get_nome() + "|" + str(processo.get_pag(pos))
  
        if self.politica == "global" and self.frequencia:
            # Encontrar a menor frequência de uso globalmente
            minfreq = min(self.frequencia.values())
            paginas_menos_usadas = [p for p in self.frequencia if self.frequencia[p] == minfreq]

            # Ordena as páginas com mesma frequência mínima numericamente pelo ID (parte após "|")
            paginas_menos_usadas.sort(key=lambda x: int(x.split("|")[1]))

            if paginas_menos_usadas:
                # Verificar se há empate (várias páginas com o mesmo ID e mesma frequência)
                if len(paginas_menos_usadas) > 1 and paginas_menos_usadas[0].split("|")[1] == paginas_menos_usadas[1].split("|")[1]:
                    print("empate")

                # Selecionar a primeira página para remoção (a de menor ID)
                print(paginas_menos_usadas[1])
                pagina_menos_usada = paginas_menos_usadas[0]
                self.memoria_fisica.remove(pagina_menos_usada)
                del self.frequencia[pagina_menos_usada]

                print(f"Página {pagina_menos_usada} foi removida da memória física.")

            # Adicionar a nova página à memória física e inicializar a frequência
            if len(self.memoria_fisica) >= self.qntd_memoria:
                # Remove a página menos usada antes de adicionar a nova página
                self.memoria_fisica.append(pagina)
                self.frequencia[pagina] = 1  # Inicializa a contagem de acessos para a nova página
                self.troca_pag += 1
                print(f"Página {pagina} foi alocada na memória global.")
    
        if politica == "local":
            processo.update_frequencia_local(processo.get_pag(pos))

            if pagina in processo.memoria_local:
                print(f"Página {pagina} já está na memória local do processo {processo.get_nome()}.")
                return    

            if len(processo.memoria_local) <= processo.get_qntd_pag(): 
                minfreq_local = min(processo.freq_paginas.values())
                paginas_menos_usadas_local = [p for p in processo.freq_paginas if processo.freq_paginas[p] == minfreq_local]
                if paginas_menos_usadas_local:
                    # Verificar se há empate (várias páginas com o mesmo ID e mesma frequência)
                    print(paginas_menos_usadas_local[0])
                    if len(paginas_menos_usadas_local) > 1 and paginas_menos_usadas_local[0].split("|")[1] == paginas_menos_usadas_local[1].split("|")[1]:
                        print("empate")
                
                # criterio de desempate e remoção
                pagina_menos_usada_local = paginas_menos_usadas_local[0]
                processo.memoria_local.remove(pagina_menos_usada_local)
                self.memoria_fisica.remove(processo.get_nome() + "|" + str(pagina_menos_usada_local))
                del processo.freq_paginas[pagina_menos_usada_local]
    
                print(f"Página {processo.get_nome()}|{pagina_menos_usada_local} foi removida da memória local e física.")

            # Adicionar a nova página à memória local e física
            processo.memoria_local.append(processo.get_pag(pos))
            self.memoria_fisica.append(pagina)
            processo.freq_paginas[processo.get_pag(pos)] = 1  # Inicializa a frequência local
            self.troca_pag += 1
            print(f"Página {pagina} foi alocada na memória local do processo {processo.get_nome()}.")

    def menos_recentemente_usada(self, processo, pos):
        pagina = processo.get_nome() + "|" + str(processo.get_pag(pos))
        
        # Se a política for global
        if self.politica == "global":
            if pagina in self.usoPagina:
                # Página já está na memória, atualiza a ordem de uso
                self.usoPagina.remove(pagina)
                self.usoPagina.append(pagina)

            else:
                # Memória cheia, remover a menos recentemente usada
                if len(self.memoria_fisica) >= self.qntd_memoria:
                    pagina_menos_usada = self.usoPagina.pop(0)  # Remove a menos recentemente usada
                    self.memoria_fisica.remove(pagina_menos_usada)
        
        
        # Se a política for local
        elif self.politica == "local":
            if pagina in processo.memoria_local:
                # Página já está na memória local, atualiza a ordem de uso
                processo.memoria_local.remove(pagina)
                processo.memoria_local.append(pagina)
            else:
                # Memória local do processo cheia, remover a menos recentemente usada
                if len(processo.memoria_local) >= processo.get_qntd_pag():
                    pagina_menos_usada = processo.memoria_local.pop(0) # escolhe a pagina com menos acessos recentes 
                    self.memoria_fisica.remove(processo.get_nome() + "|" + str(pagina_menos_usada))
                    
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

def alternancia_circular(lista_processos, clock, memoria_fisica, acesso, alg):
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
                    memoria_fisica.alocacao(lista_processos[i], j, lista_processos, alg)
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
    lista_algoritmos = ["fifo", "nuf", "mru", "otimo"]
    for alg in lista_algoritmos:
        algoritmo, clock, politica, tam_memoria, tam_pag_moldura, percentual_aloc, acesso_por_ciclo, lista_processos = entrada_arquivo()
        qntd_moldura = int((tam_memoria//tam_pag_moldura) * (percentual_aloc/100))
        memoria_fisica = Memoria(politica, qntd_moldura)
        lista_processos = alternancia_circular(lista_processos, clock, memoria_fisica, acesso_por_ciclo, alg)
        lista_troca_pag.append(memoria_fisica.get_troca_pag())
        print(f"Quantidade de trocas de páginas: {memoria_fisica.get_troca_pag()}")
        print("------------------------------------------")
    
    for i in range(len(lista_processos)):
        print(lista_processos[i])

    # Imprimindo os resultados de troca de paginas
    otimo = lista_troca_pag[3]
    lista_troca_pag.pop(3)
    melhor = min(lista_troca_pag)
    if(lista_troca_pag.count(melhor) > 1):
        melhor = "empate"
    else:
        melhor = lista_algoritmos[lista_troca_pag.index(melhor)]
    
    print(f"FIFO: {lista_troca_pag[0]}|NUF: {lista_troca_pag[1]}|MRU: {lista_troca_pag[2]}|ótimo {otimo}|{melhor}")
    print(melhor)
        
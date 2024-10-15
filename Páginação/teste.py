class Memoria:
    def __init__(self, politica, qntd_memoria):
        self.politica = politica
        self.memoria_fisica = []
        self.qntd_memoria = qntd_memoria

    def alocacao(self, processo):
        if(processo not in self.memoria_fisica and len(self.memoria_fisica) < self.qntd_memoria):
            self.memoria_fisica.append(processo)
        else:
            self.fifo(processo)

    def fifo(self, processo):
        if(self.politica == "global"):
            self.memoria_fisica.pop(0)
            self.memoria_fisica.append(processo)

lista = Memoria("global", 3)
lista.alocacao("processo-1")
lista.alocacao("processo-2")
lista.alocacao("processo-3")
lista.alocacao("processo-4")
lista.alocacao("processo-5")
print(lista.memoria_fisica[0])

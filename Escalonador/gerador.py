for i in range(numProcessos):
        print(f"Informe o nome do processo {i}")
        nome_processo = str(input())
        print(f"Informe o pid do processo {nome_processo}")
        pid = int(input())
        print(f"Informe o tempo de execução do processo {nome_processo}")
        tempo = int(input())
        if(alg == 3):
            print(f"Informe o bilhete do processo {nome_processo}")
            bilhete = int(input())
        novo_processo = Processo(nome_processo, pid, tempo, bilhete)
        lista_processos.append(novo_processo)
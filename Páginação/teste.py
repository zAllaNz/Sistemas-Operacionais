paginas_disponiveis = [1, 2, 3, 4, 5, 6]
sequencia_acessos = [5, 1, 4, 2, 3, 3, 5, 2, 1, 4]

# Armazena o índice de quando a página vai aparecer
tempo_para_aparecer = {}

# Para cada página disponível
for pagina in paginas_disponiveis:
    if pagina in sequencia_acessos:
        # Encontrar o índice da próxima ocorrência
        indice = sequencia_acessos.index(pagina)
        tempo_para_aparecer[pagina] = indice
    else:
        # Se a página não aparecer mais, consideramos que demorará "infinitamente"
        tempo_para_aparecer[pagina] = float('inf')

# Descobrir a página que demora mais para aparecer
pagina_demora_mais = max(tempo_para_aparecer, key=tempo_para_aparecer.get)

print(f"A página que vai demorar mais para aparecer novamente é: {pagina_demora_mais}")
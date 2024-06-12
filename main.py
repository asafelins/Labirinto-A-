from pyamaze import maze, agent, textLabel
from queue import PriorityQueue

destino = (1, 1)


# Função para calcular a heurística (distância de Manhattan) entre uma célula e o destino
def hscore(celula, destino):
    linhac = celula[0]
    colunac = celula[1]
    linhad = destino[0]
    colunad = destino[1]
    return abs(colunac - colunad) + abs(linhac - linhad)

#A*
def aestrelha(lab):
    #Tabuleiro com todas as celular com fscore infinito
    fscore = {celula: float("inf") for celula in lab.grid}
    gscore = {}
    celula_inicial = (lab.rows, lab.cols)
    
    #calculo da celula inicial 
    gscore[celula_inicial] = 0 
    fscore[celula_inicial] = gscore[celula_inicial] + hscore(celula_inicial, destino)
    print(fscore)

    # Inicialização da fila de prioridade
    fila = PriorityQueue()
    item = (fscore[celula_inicial], hscore(celula_inicial, destino), celula_inicial)
    fila.put(item)
    

    caminho = {}
    while not fila.empty():
        celula = fila.get()[2]
        
        # Se a célula atual é o destino, sair do loop
        if celula == destino:
            break

        # Iterar sobre as direções possíveis (Norte, Sul, Leste, Oeste)
        for direcao in "NSEW":
            if lab.maze_map[celula] [direcao] == 1:

                linha_celula = celula[0]
                coluna_celula = celula[1]


                # Determinar a próxima célula com base na direção
                if direcao == "N":
                    proxima_celula = (linha_celula - 1, coluna_celula)
                elif direcao == "S":
                    proxima_celula = (linha_celula + 1, coluna_celula)
                elif direcao == "W":
                    proxima_celula = (linha_celula, coluna_celula - 1)
                elif direcao == "E":
                    proxima_celula = (linha_celula, coluna_celula + 1)

                # Calcular os novos valores de gscore e fscore
                novo_gscore = gscore[celula] + 1
                novo_fscore = novo_gscore + hscore(proxima_celula, destino)

                # Atualizar fscore e gscore se o novo fscore for menor
                if novo_fscore < fscore[proxima_celula]:
                    fscore[proxima_celula] =  novo_fscore
                    gscore[proxima_celula] = novo_gscore
                    item = (novo_fscore, hscore(proxima_celula, destino), proxima_celula)
                    fila.put(item)
                    caminho[proxima_celula] = celula

    # Reconstruir o caminho final do destino para a célula inicial
    caminho_final = {}
    celula_analisada = destino
    print("Celulas analisadas", len(caminho.keys()))
    while celula_analisada != celula_inicial:
        caminho_final[caminho[celula_analisada]] = celula_analisada
        celula_analisada = caminho[celula_analisada]
    return caminho_final

# Criação do labirinto
lab = maze(20, 20)
lab.CreateMaze(loopPercent=50)

caminho_perfeito = lab.path
#print(caminho)

# Criação do agente no labirinto
agente = agent(lab, footprints=True, filled=True)

# Encontrar o caminho usando o algoritmo A* e executar ele no labirinto criado
caminho = aestrelha(lab)
lab.tracePath({agente: caminho}, delay=200)
texto = textLabel(lab, title= "Custo: ", value=len(caminho))

# Imprimir informações adicionais para analises
print("Total de celulas", len(lab.maze_map.keys()))
print("Custo Total:", len(caminho))
print("Custo Perfeito:", len(caminho_perfeito))

# Executar o labirinto
lab.run()
import matplotlib.pyplot as plt
import numpy as np
import heapq
from matplotlib.colors import ListedColormap
from collections import defaultdict


def print_mapa(grid, caminho=[], title=""):
    """
    Esta função gera uma representação visual do mapa usando matplotlib.
    """
    cores = [
        "#9c5a3c",  # Nada
        "#3d1e10",  # Obstaculo
        "#FFCA00",  # Tesouro
        "#EBCF87",  # Caminho
        "#EBAD87"   # Lama
    ]

    grid_cores = {
        '.': 0,  # Vazio
        '#': 1,  # Obstaculo
        'I': 0,  # Inicio
        'T': 2,  # Tesouro
        '*': 3,  # Caminho
        'L': 4   # Lama
    }

    # cria um colormap personalizado
    cmap = ListedColormap(cores)

    n, m = len(grid), len(grid[0])
    map_visual = np.zeros((n, m))

    # Conte quantas vezes cada célula é visitada no caminho
    path_indices = defaultdict(list)

    for idx, pos in enumerate(caminho):
        path_indices[pos].append(idx)


    for i in range(n):
        for j in range(m):
            # Altera as cores das celulas que estao no caminho
            if (i, j) in caminho:
                if grid[i][j] == 'I':
                    map_visual[i][j] = grid_cores['*']
                elif grid[i][j] == 'T':
                    map_visual[i][j] = grid_cores['*']
                elif grid[i][j] == '.':
                    map_visual[i][j] = grid_cores['*']
                elif grid[i][j] == 'L':
                    map_visual[i][j] = grid_cores['*']
                else:
                    map_visual[i][j] = grid_cores[grid[i][j]]
            else:
                map_visual[i][j] = grid_cores.get(grid[i][j], 0)

    if title:
        plt.title(title)
    # Plota o mapa
    plt.imshow(map_visual, cmap=cmap, vmin=0, vmax=len(cores) - 1)

    # Adicionar anotações de texto a cada célula
    for i in range(n):
        for j in range(m):
            # Exibir o indice do caminho no canto inferior direito se a celula estiver no caminho
            if (i, j) in path_indices:
                index = ", ".join(map(str, path_indices[(i, j)]))
                plt.text(j + 0.35, i + 0.35, index, ha='right', va='bottom', color='red', fontsize=4)
                plt.text(j, i, grid[i][j], ha='center', va='center', color='black', fontsize=12, fontweight='bold')
            else:
               plt.text(j, i, grid[i][j], ha='center', va='center', color='white', fontsize=12, fontweight='bold')



    plt.grid(which='both', color='black', linestyle='-', linewidth=2)
    plt.xticks(np.arange(-0.5, m, 1), [])
    plt.yticks(np.arange(-0.5, n, 1), [])

    # Mostra o mapa
    plt.show()

def print_caminho(grid, caminho, title=""):
    """
    Esta função recebe uma matriz e um caminho como argumentos e mostra o caminho percorrido na matriz.
    """
    # Cria uma copia da grade para evitar modificar a original
    grid_copia = [linha[:] for linha in grid]

    # Marque o caminho com '*'
    for (x, y) in caminho:
        if grid_copia[x][y] == '.':  # Marca apenas celulas vazias
            grid_copia[x][y] = '*'

    print_mapa(grid_copia, caminho, title)
def busca_custo_uniforme(grid, pos_inicial, pos_tesouro):
    fila_prioridade= []
    heapq.heappush(fila_prioridade, (0, pos_inicial))
    visitados= set()
    caminho={}
    caminho[pos_inicial]= None
    linha = len(grid)
    coluna = len(grid[0])
    direçoes= [(0 , 1), (1,0), (0,-1), (-1,0)]
    while fila_prioridade:
        custo , pos_atual= heapq.heappop(fila_prioridade)
        if pos_atual in visitados:
            continue
        visitados.add(pos_atual)
        if pos_atual== pos_tesouro:
            caminho_encontrado= []
            while pos_atual is not None:
                caminho_encontrado.append(pos_atual)
                pos_atual=caminho[pos_atual]
            caminho_encontrado.reverse()
            return caminho_encontrado
        for direçao in direçoes:
            vizinho= (pos_atual[0]+ direçao[0], pos_atual[1]+ direçao[1])
            if 0 <= vizinho[0] < linha and 0 <= vizinho[1] < coluna:
                if grid[vizinho[0]][vizinho[1]]!= "#":
                    if grid[vizinho[0]][vizinho[1]]== "L":
                        custo_novo= custo + 5
                    elif grid[vizinho[0]][vizinho[1]] == ".":
                        custo_novo = custo + 1
                    heapq.heappush(fila_prioridade,(custo_novo, vizinho))
                    if vizinho not in caminho:
                        caminho[vizinho]= pos_atual
    return []
def busca_gulosa(grid, pos_inicial, pos_tesouro):
    fila_prioridade=[]
    
    visitados= set()
    caminho={}
    caminho[pos_inicial]= None
    linha = len(grid)
    coluna = len(grid[0])
    direçoes= [(0 , 1), (1,0), (0,-1), (-1,0)]
    def heuristica(a, b ):
        return abs(a[0] - b[0]) + abs(a[1]- b[1])
    heapq.heappush(fila_prioridade, (0, pos_inicial))
    while fila_prioridade:
        _ , pos_atual= heapq.heappop(fila_prioridade)
        if pos_atual in visitados:
            continue
        visitados.add(pos_atual)
        if pos_atual== pos_tesouro:
            caminho_encontrado= []
            while pos_atual is not None:
                caminho_encontrado.append(pos_atual)
                pos_atual=caminho[pos_atual]
            caminho_encontrado.reverse()
            return caminho_encontrado
        for direçao in direçoes:
            vizinho= (pos_atual[0]+ direçao[0], pos_atual[1]+ direçao[1])
            if 0 <= vizinho[0] < linha and 0 <= vizinho[1] < coluna and vizinho not in visitados and grid[vizinho[0]][vizinho[1]] != "#":
                prioridade= heuristica(vizinho, pos_tesouro)
                heapq.heappush(fila_prioridade,(prioridade, vizinho))
                caminho[vizinho]= pos_atual
    


                
                    
    return []
def busca_a_estrela(grid, pos_inicial, pos_tesouro):
    fila_prioridade=[]
    
    visitados= set()
    caminho={}
    caminho[pos_inicial]= (0, None)
    linha = len(grid)
    coluna = len(grid[0])
    direçoes= [(0 , 1), (1,0), (0,-1), (-1,0)]
    def heuristica(pos ):
        return abs(pos[0] - pos_tesouro[0]) + abs(pos[1]- pos_tesouro[1])
    heapq.heappush(fila_prioridade, (heuristica(pos_inicial),0, pos_inicial))
    while fila_prioridade:
        _ ,custo_acumulado, pos_atual= heapq.heappop(fila_prioridade)
        if pos_atual in visitados:
            continue
        visitados.add(pos_atual)
        if pos_atual== pos_tesouro:
            caminho_encontrado= []
            while pos_atual is not None:
                caminho_encontrado.append(pos_atual)
                pos_atual=caminho[pos_atual][1]
            caminho_encontrado.reverse()
            return caminho_encontrado
        for direçao in direçoes:
            vizinho= (pos_atual[0]+ direçao[0], pos_atual[1]+ direçao[1])
            if 0 <= vizinho[0] < linha and 0 <= vizinho[1] < coluna:
                if grid[vizinho[0]][vizinho[1]]!= "#":
                    if grid[vizinho[0]][vizinho[1]]== "L":
                        custo_novo= custo_acumulado +5
                    elif grid[vizinho[0]][vizinho[1]] == ".":
                        custo_novo= custo_acumulado + 1
                    vizinho_novo=heuristica(vizinho)
                    total= vizinho_novo + custo_novo
                    if vizinho not in caminho:
                        caminho[vizinho]= (custo_novo, pos_atual)
                        heapq.heappush(fila_prioridade,(total, custo_novo, vizinho))
    return []

    

                   

grid = [
    ['I', '#', '.', '#', 'L', 'L', 'T'],
    ['.', '#', '.', '#', 'L', '#', '.'],
    ['.', '#', '.', '#', 'L', '#', '.'],
    ['.', '#', '.', '.', '.', '#', '.'],
    ['.', '#', '.', '#', '.', '#', '.'],
    ['.', '#', '.', '#', '.', '#', '.'],
    ['.', '.', '.', '#', '.', '.', '.'],
]
posicao_inicial = (0, 0)
posicao_tesouro = (3, 3)
caminho_bcu = busca_custo_uniforme(grid, posicao_inicial, posicao_tesouro)
caminho_busca_gulosa= busca_gulosa(grid, posicao_inicial, posicao_tesouro)
caminho_a_estrela= busca_a_estrela(grid, posicao_inicial, posicao_tesouro)
    

print_mapa(grid)
print_caminho(grid, caminho_bcu, "Custo uniforme")
print_caminho(grid, caminho_busca_gulosa, "Busca gulosa") 
print_caminho(grid,caminho_a_estrela, " A estrela" ) 


             
                    
                





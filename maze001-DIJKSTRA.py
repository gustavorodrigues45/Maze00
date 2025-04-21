import pygame
import sys
import copy
import random
import heapq
from random import randint

class ArestasFechadas:
    def __init__(self, superior, inferior, esquerda, direita):
        self.superior = superior
        self.inferior = inferior
        self.esquerda = esquerda
        self.direita = direita

class Celula:
    def __init__(self, arestasFechadas, corPreenchimento, corVisitada, corLinha, corAberta, visitada, aberta):
        self.arestasFechadas = arestasFechadas
        self.corPreenchimento = corPreenchimento
        self.corVisitada = corVisitada
        self.corLinha = corLinha
        self.corAberta = corAberta
        self.visited = visitada
        self.aberta = aberta
        self.distancia = float('inf')  # Distância inicial
        self.pai = None  # Pai para reconstruir o caminho

    def get_corPreenchimento(self):
        return self.corPreenchimento

    def get_arestasFechadas(self):
        return self.arestasFechadas

    def is_visited(self):
        return self.visited

    def desenhar(self, tela, x, y, aresta):
        # x : coluna
        # y : linha
        arSuperiorIni = (x, y)
        arSuperiorFim = (x + aresta, y)
        arInferiorIni = (x, y + aresta)
        arInferiorFim = (x + aresta, y + aresta)
        arEsquerdaIni = (x, y)
        arEsquerdaFim = (x, y + aresta)
        arDireitaIni = (x + aresta, y)
        arDireitaFim = (x + aresta, y + aresta)

        if self.aberta:
            pygame.draw.rect(tela, self.corAberta, (x, y, aresta, aresta))
        else:
            pygame.draw.rect(tela, self.corPreenchimento, (x, y, aresta, aresta))

        pygame.draw.line(tela, self.corLinha, arSuperiorIni, arSuperiorFim)
        pygame.draw.line(tela, self.corLinha, arInferiorIni, arInferiorFim)
        pygame.draw.line(tela, self.corLinha, arEsquerdaIni, arEsquerdaFim)
        pygame.draw.line(tela, self.corLinha, arDireitaIni, arDireitaFim)

class AldousBroder:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.matriz = Malha(qtLinhas, qtColunas, aresta, celulaPadrao)
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao

    def __len__(self):
        return len(self.matriz)

    def __iter__(self):
        return iter(self.matriz)

    def resetaLabirinto(self):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna] = copy.deepcopy(self.celulaPadrao)

    def SorteiaCelulaVizinha(self, linhaCelulaAtual, colunaCelulaAtual):
        encontrou = False
        while (encontrou == False):
            linhaVizinha = linhaCelulaAtual + randint(-1, 1)
            colunaVizinha = colunaCelulaAtual + randint(-1, 1)
            if (
                    linhaVizinha >= 0 and linhaVizinha < self.qtLinhas and colunaVizinha >= 0 and colunaVizinha < self.qtColunas):
                encontrou = True

        return linhaVizinha, colunaVizinha

    def GeraLabirinto(self):
        self.resetaLabirinto()
        unvisitedCells = self.qtLinhas * self.qtColunas
        currentCellLine, currentCellColumn, neighCellLine, neighCellColumn = -1, -1, -1, -1

        currentCellLine = randint(0, self.qtLinhas - 1)
        currentCellColumn = randint(0, self.qtColunas - 1)

        while (unvisitedCells > 0):
            neighCellLine, neighCellColumn = self.SorteiaCelulaVizinha(currentCellLine, currentCellColumn)

            if (self.matriz[neighCellLine][neighCellColumn].visited == False):
                self.matriz[currentCellLine][currentCellColumn].aberta = True
                self.matriz[neighCellLine][neighCellColumn].visited = True
                unvisitedCells -= 1

            currentCellLine, currentCellColumn = neighCellLine, neighCellColumn

class Malha:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao
        self.matriz = self.GeraMatriz()

    def __len__(self):
        return len(self.matriz)

    def __iter__(self):
        return iter(self.matriz)

    def __getitem__(self, index):
        return self.matriz[index]

    def __setitem__(self, index, value):
        self.matriz[index] = value

    def GeraMatriz(self):
        matriz = []
        for i in range(self.qtLinhas):
            linha = []
            for j in range(self.qtColunas):
                linha.append(copy.deepcopy(self.celulaPadrao))
            matriz.append(linha)
        return matriz

    def DesenhaLabirinto(self, tela, x, y):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna].desenhar(tela, x + coluna * self.aresta, y + linha * self.aresta, self.aresta)

def resolve_labirinto_dijkstra(labirinto):
    pq = []
    start = (1, 0)
    end = (len(labirinto) - 1, len(labirinto[0]) - 1)
    
    labirinto[1][0].distancia = 0
    heapq.heappush(pq, (0, start))

    while pq:
        current_dist, (current_row, current_col) = heapq.heappop(pq)

        if (current_row, current_col) == end:
            break

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for d in directions:
            new_row, new_col = current_row + d[0], current_col + d[1]

            if 0 <= new_row < len(labirinto) and 0 <= new_col < len(labirinto[0]) and labirinto[new_row][new_col].aberta:
                new_dist = current_dist + 1

                if new_dist < labirinto[new_row][new_col].distancia:
                    labirinto[new_row][new_col].distancia = new_dist
                    labirinto[new_row][new_col].pai = (current_row, current_col)
                    heapq.heappush(pq, (new_dist, (new_row, new_col)))

    caminho = []
    current = end
    while current:
        caminho.append(current)
        current = labirinto[current[0]][current[1]].pai
    return caminho[::-1]

def main():
    pygame.init()

    azul = (50, 50, 255)
    preto = (0, 0, 0)
    verde = (0,128,0)
    vermelho = (255, 0, 0)
    branco = (255, 255, 255)
    cinza = (128, 128, 128)

    largura, altura = 600, 600

    N = 50
    M = 50
    aresta = 10

    celulaPadrao = Celula(ArestasFechadas(False, False, False, False), preto, cinza, preto, verde, False, False)
    labirinto = AldousBroder(N, M, aresta, celulaPadrao)
    labirinto.GeraLabirinto()

    labirinto.matriz[1][0].aberta = True
    labirinto.matriz[N-1][M-1].aberta = True

    caminho = resolve_labirinto_dijkstra(labirinto.matriz)

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Mostra Malha')

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela.fill(branco)
        [linha, coluna] = ((tela.get_width() - (M * aresta)) // 2,
                           (tela.get_height() - (N * aresta)) // 2)

        labirinto.matriz.DesenhaLabirinto(tela, linha, coluna)

        for (r, c) in caminho:
            pygame.draw.rect(tela, vermelho, (linha + c * aresta, coluna + r * aresta, aresta, aresta))

        pygame.display.flip()

if __name__ == '__main__':
    main()

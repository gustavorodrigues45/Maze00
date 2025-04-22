## Gustavo da Encarnação Rodrigues 20232075 #
# João Pedro Mendes Noguiera 202311204 #

#Comparação Dijkstra vs força bruta 
# 
# Ao comparar o Dijkstra com o força-bruta, dá pra ver como o Dijkstra 
# é muito mais eficiente. O algoritmo sempre vai pelo caminho com menor custo, o que evita que
# a gente perca tempo testando caminhos inúteis. Já o força-bruta tenta de tudo, sem muito critério e 
# acaba demorando muito, especialmente se o labirinto for grande. Mesmo sendo mais simples de codificar 
# ele não é prático pra resolver labirintos mais complexos. Em suma, o Dijkstra é mais rápido, inteligente,
# e é mais benéfico em termos de desempenho.#
# 

import pygame
import sys
import copy
import random
from random import randint
import heapq

# ----------------- Classes Base -----------------

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
        self.no_caminho_dfs = False
        self.no_caminho_dijkstra = False

    def desenhar(self, tela, x, y, aresta, modo):
        cor = self.corAberta if self.aberta else self.corPreenchimento
        if modo == "dfs" and self.no_caminho_dfs:
            cor = (255, 0, 0)  # vermelho
        elif modo == "dijkstra" and self.no_caminho_dijkstra:
            cor = (255, 255, 0)  # amarelo

        pygame.draw.rect(tela, cor, (x, y, aresta, aresta))
        pygame.draw.line(tela, self.corLinha, (x, y), (x + aresta, y))
        pygame.draw.line(tela, self.corLinha, (x, y + aresta), (x + aresta, y + aresta))
        pygame.draw.line(tela, self.corLinha, (x, y), (x, y + aresta))
        pygame.draw.line(tela, self.corLinha, (x + aresta, y), (x + aresta, y + aresta))


class Malha:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.matriz = self.GeraMatriz(celulaPadrao)

    def GeraMatriz(self, celulaPadrao):
        return [[copy.deepcopy(celulaPadrao) for _ in range(self.qtColunas)] for _ in range(self.qtLinhas)]

    def DesenhaLabirinto(self, tela, x, y, modo):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna].desenhar(tela, x + coluna * self.aresta, y + linha * self.aresta, self.aresta, modo)

    def in_bounds(self, l, c):
        return 0 <= l < self.qtLinhas and 0 <= c < self.qtColunas

    def copia(self):
        nova = Malha(self.qtLinhas, self.qtColunas, self.aresta, self.matriz[0][0])
        nova.matriz = [[copy.deepcopy(self.matriz[i][j]) for j in range(self.qtColunas)] for i in range(self.qtLinhas)]
        return nova


class AldousBroder:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao
        self.matriz = Malha(qtLinhas, qtColunas, aresta, celulaPadrao)

    def resetaLabirinto(self):
        self.matriz = Malha(self.qtLinhas, self.qtColunas, self.aresta, self.celulaPadrao)

    def SorteiaCelulaVizinha(self, l, c):
        direcoes = [(0,1), (0,-1), (1,0), (-1,0)]
        random.shuffle(direcoes)
        for dl, dc in direcoes:
            nl, nc = l+dl, c+dc
            if self.matriz.in_bounds(nl, nc):
                return nl, nc
        return l, c

    def GeraLabirinto(self):
        self.resetaLabirinto()
        unvisited = self.qtLinhas * self.qtColunas
        l, c = randint(0, self.qtLinhas - 1), randint(0, self.qtColunas - 1)

        while unvisited > 0:
            nl, nc = self.SorteiaCelulaVizinha(l, c)
            if not self.matriz.matriz[nl][nc].visited:
                self.matriz.matriz[l][c].aberta = True
                self.matriz.matriz[nl][nc].visited = True
                unvisited -= 1
            l, c = nl, nc

        self.matriz.matriz[1][0].aberta = True
        self.matriz.matriz[self.qtLinhas-1][self.qtColunas-1].aberta = True

    def ResolvedorForcaBruta(self):
        caminho = []
        visitados = [[False]*self.qtColunas for _ in range(self.qtLinhas)]

        def busca(l, c):
            if not self.matriz.in_bounds(l, c): return False
            if visitados[l][c]: return False
            if not self.matriz.matriz[l][c].aberta: return False

            visitados[l][c] = True
            caminho.append((l, c))

            if (l, c) == (self.qtLinhas-1, self.qtColunas-1):
                return True

            for dl, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                if busca(l+dl, c+dc):
                    return True

            caminho.pop()
            return False

        busca(1, 0)
        for l, c in caminho:
            self.matriz.matriz[l][c].no_caminho_dfs = True

    def ResolvedorDijkstra(self):
        inicio = (1, 0)
        fim = (self.qtLinhas - 1, self.qtColunas - 1)
        dist = [[float('inf')] * self.qtColunas for _ in range(self.qtLinhas)]
        anteriores = [[None] * self.qtColunas for _ in range(self.qtLinhas)]

        heap = []
        dist[inicio[0]][inicio[1]] = 0
        heapq.heappush(heap, (0, inicio))

        while heap:
            custo, (l, c) = heapq.heappop(heap)
            if (l, c) == fim:
                break

            for dl, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                nl, nc = l+dl, c+dc
                if self.matriz.in_bounds(nl, nc) and self.matriz.matriz[nl][nc].aberta:
                    novo_custo = custo + 1
                    if novo_custo < dist[nl][nc]:
                        dist[nl][nc] = novo_custo
                        anteriores[nl][nc] = (l, c)
                        heapq.heappush(heap, (novo_custo, (nl, nc)))

        # Reconstruir caminho
        l, c = fim
        if anteriores[l][c] is not None:
            while (l, c) != inicio:
                self.matriz.matriz[l][c].no_caminho_dijkstra = True
                l, c = anteriores[l][c]
            self.matriz.matriz[l][c].no_caminho_dijkstra = True

# ----------------- Main -----------------

def main():
    pygame.init()
    branco = (255, 255, 255)
    preto = (0, 0, 0)
    cinza = (150, 150, 150)

    N, M = 20, 20
    aresta = 20

    largura = 2 * (M * aresta + 50)
    altura = N * aresta + 100
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Comparação DFS × Dijkstra")

    celulaPadrao = Celula(ArestasFechadas(False, False, False, False), preto, cinza, preto, branco, False, False)

    lab = AldousBroder(N, M, aresta, celulaPadrao)
    lab.GeraLabirinto()

    lab_dfs = copy.deepcopy(lab)
    lab_dijkstra = copy.deepcopy(lab)

    lab_dfs.ResolvedorForcaBruta()
    lab_dijkstra.ResolvedorDijkstra()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela.fill(branco)
        offsetY = (altura - N * aresta) // 2

        # Lado esquerdo: DFS
        offsetX_dfs = 50
        lab_dfs.matriz.DesenhaLabirinto(tela, offsetX_dfs, offsetY, "dfs")

        # Lado direito: Dijkstra
        offsetX_dij = largura // 2 + 25
        lab_dijkstra.matriz.DesenhaLabirinto(tela, offsetX_dij, offsetY, "dijkstra")

        pygame.display.flip()

if __name__ == "__main__":
    main()

# Gustavo da Encarnação Rodrigues 20232075 #
# João Pedro Mendes Noguiera 202311204 #

import pygame
import sys
import copy
import random
from random import randint

# ---------------------- CLASSES BÁSICAS ----------------------

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
        self.no_caminho = False

    def desenhar(self, tela, x, y, aresta):
        cor = self.corAberta if self.aberta else self.corPreenchimento
        if self.no_caminho:
            cor = (255, 0, 0)  # vermelho para caminho encontrado

        pygame.draw.rect(tela, cor, (x, y, aresta, aresta))
        pygame.draw.line(tela, self.corLinha, (x, y), (x + aresta, y))
        pygame.draw.line(tela, self.corLinha, (x, y + aresta), (x + aresta, y + aresta))
        pygame.draw.line(tela, self.corLinha, (x, y), (x, y + aresta))
        pygame.draw.line(tela, self.corLinha, (x + aresta, y), (x + aresta, y + aresta))


# ---------------------- MALHA E LABIRINTO ----------------------

class Malha:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.matriz = self.GeraMatriz(celulaPadrao)

    def GeraMatriz(self, celulaPadrao):
        return [[copy.deepcopy(celulaPadrao) for _ in range(self.qtColunas)] for _ in range(self.qtLinhas)]

    def DesenhaLabirinto(self, tela, x, y):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna].desenhar(tela, x + coluna * self.aresta, y + linha * self.aresta, self.aresta)

    def in_bounds(self, l, c):
        return 0 <= l < self.qtLinhas and 0 <= c < self.qtColunas


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

        # Força abertura de entrada e saída
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
                return True  # achou saída

            for dl, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                if busca(l+dl, c+dc):
                    return True

            caminho.pop()
            return False

        busca(1, 0)
        for l, c in caminho:
            self.matriz.matriz[l][c].no_caminho = True


# ---------------------- PYGAME MAIN ----------------------

def main():
    pygame.init()
    preto = (0, 0, 0)
    cinza = (150, 150, 150)
    branco = (255, 255, 255)

    N = 20  # linhas
    M = 20  # colunas
    aresta = 20

    largura = M * aresta + 100
    altura = N * aresta + 100

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Labirinto com Força Bruta')

    celulaPadrao = Celula(ArestasFechadas(False, False, False, False), preto, cinza, preto, branco, False, False)
    lab = AldousBroder(N, M, aresta, celulaPadrao)
    lab.GeraLabirinto()
    lab.ResolvedorForcaBruta()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela.fill(branco)
        offsetX = (largura - M * aresta) // 2
        offsetY = (altura - N * aresta) // 2
        lab.matriz.DesenhaLabirinto(tela, offsetX, offsetY)
        pygame.display.flip()


if __name__ == '__main__':
    main()

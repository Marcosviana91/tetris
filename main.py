import pygame
from pygame.locals import *
from sys import exit
from random import choice


class Quadrado:
	'''Inicializa o quadrado'''
	def __init__(self, tam, x, surface):
		self.tamanho_y = tam
		self.tamanho_x = tam*choice((1,1))
		self._cor = choice((VERDE, VERMELHO, AZUL))
		self._x_pos = x - tam//2
		self._y_pos = altura_tela//10
		self._surface = surface
		self._posicao_atual_x = pos_linha//2#posição inicial/atual na lista_linha_pos
		self._posicao_atual_y = pos_coluna-1#posição inicial/atual na coluna (lista_linha_alt)


	def mover_direita(self, passo):
		if (self.desenhar().right+tam_padrao) <= (contorno().right):
			self._x_pos += passo
			self._posicao_atual_x += 1


	def mover_esquerda(self, passo):
		if self._x_pos >= largura_tela//4+tam_padrao:
			self._x_pos -= passo
			self._posicao_atual_x -= 1
	
	
	def cair(self, vel):
		cair = False
		if self.desenhar().bottom+tam_padrao < contorno().bottom:
			self._y_pos += vel
			self._posicao_atual_y -= 1
			cair = True
		#if self.desenhar()
		return cair
		
		
	def desenhar(self):
		return pygame.draw.rect(self._surface, self._cor, (self._x_pos, self._y_pos,self.tamanho_x,self.tamanho_y))
	
	@property
	def get_pos(self):
		return (self._posicao_atual_x, self._posicao_atual_y)



def contorno():
	'''desenha os limitadores do jogo e retorna um Rect'''
	return pygame.draw.rect(tela,BRANCO,(largura_tela//10*2.3,altura_tela//10,largura_tela//10*5.3,altura_tela//10*5),10,10)


def controles():#desenha controles tatil
	botao_direito = pygame.draw.polygon(tela, BRANCO,[(largura_tela//10*9, altura_tela//10*7), (largura_tela//10*10, altura_tela//10*8),(largura_tela//10*9,altura_tela//10*9)])
	botao_esquerdo = pygame.draw.polygon(tela, BRANCO,[(largura_tela//10*1,altura_tela//10*7),(0, altura_tela//10*8),(largura_tela//10*1,altura_tela//10*9)])
	botao_baixo = pygame.draw.polygon(tela,BRANCO,[(largura_tela//4,altura_tela*0.9),(largura_tela//2, altura_tela),(largura_tela//4*3, altura_tela*0.9)])
	return ((botao_direito),( botao_esquerdo), (botao_baixo))#retorno uma tupla com os rect da cada botao (direita, esquerda, baixo)



#CORES
BRANCO = (255,255,255)
PRETO = (0,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)
VERMELHO = (255,0,0)


fps = 30 #os calculos continuam acontecendo mesmo que o quadro não seja exibido.


pygame.init()#INICIALIZA O MODULO
relogio = pygame.time.Clock()

#Ajustes da tela
tela = pygame.display.set_mode()
largura_tela = tela.get_width()
altura_tela = tela.get_height()
print(f'Largura (X): {largura_tela}')
print(f'Altura (Y): {altura_tela}')
tam_padrao = (largura_tela//10)
pygame.display.set_caption('Tetris 0.5')

contador = 0#faz uma contagem a cada quadro para simular uma pausa de 1 seg, sem pausar os calculos.

#listas e posicoes
pos_linha = contorno()[2]//tam_padrao
pos_coluna = contorno()[3]//tam_padrao


lista_todos = []#lista todos os quadrados que serão desenhados
lista_linha_pos = ['' for x in range(pos_linha)]#lista todos as posições dos quadrados parados
lista_linha_alt = [lista_linha_pos.copy() for x in range(pos_coluna)]#lista todas as colunas com quadrados

#

lista_todos.append(Quadrado(tam_padrao, largura_tela//2, tela))

while True:
	lista_todos[-1].desenhar()
	relogio.tick(fps)
	tela.fill(PRETO)
	contorno()#desenha o contorno
	controles()#desenha os controles
	
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		if event.type == KEYDOWN:
			if event.key in (K_LEFT, K_a):
				lista_todos[-1].mover_esquerda(tam_padrao)
			if event.key in (K_RIGHT, K_l):
				lista_todos[-1].mover_direita(tam_padrao)
			if event.key == K_SPACE:
				contador = fps
		if event.type == MOUSEBUTTONDOWN:
			if controles()[0].collidepoint(event.pos):
				lista_todos[-1].mover_direita(tam_padrao)
			if controles()[1].collidepoint(event.pos):
				lista_todos[-1].mover_esquerda(tam_padrao)
			if controles()[2].collidepoint(event.pos):
				contador = fps
		
		
	for item in lista_todos:#desenha cada item da lista_todos
		item.desenhar()
	
	if contador < fps:#conta 1 seg antes de cair
		contador += 1
	else:
		contador = 0
		if not lista_todos[-1].cair(tam_padrao):#se nao cair
			print(lista_todos[-1].get_pos)
			lista_linha_alt[lista_todos[-1].get_pos[1]][lista_todos[-1].get_pos[0]] = lista_todos[-1]
			for y in range(pos_coluna):
				if lista_linha_alt[y].count('') == 0:#completou a linha
					print('Completou a linha')
					for c in range(pos_linha):
						i = lista_todos.index(lista_linha_pos[c])
						del lista_todos[i]# --------- PENDENTE
					lista_linha_pos = ['' for x in range(len(lista_linha_pos))]#lista todos as posições dos quadrados parados

			lista_todos.append(Quadrado(tam_padrao, largura_tela//2, tela))
	pygame.display.flip()

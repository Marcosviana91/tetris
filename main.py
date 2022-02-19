import pygame
from pygame.locals import *
from sys import exit
from random import choice


class Quadrado:
	'''Inicializa o quadrado'''
	def __init__(self, tam, x, surface):
		self.tamanho_y = tam
		self.tamanho_x = tam*choice((1,1))
		self._cor = choice((VERDE, VERMELHO, AZUL,VERDE_ESCURO, CIANO, LARANJA, OURO, ROSA_CHOQUE, INDIGO, VIOLETA))
		self._x_pos = x - tam//2
		self._y_pos = altura_tela//10
		self._surface = surface
		self._posicao_atual_x = pos_linha//2#posição inicial/atual na lista_linha_pos
		self._posicao_atual_y = pos_coluna-1#posição inicial/atual na coluna (lista_linha_alt)


	def mover_direita(self, passo):
		if self._x_pos+self.tamanho_x < contorno().right  and lista_linha_alt[self._posicao_atual_y][self._posicao_atual_x+1] is None:
			self._x_pos += passo
			self._posicao_atual_x += 1


	def mover_esquerda(self, passo):
		if self._x_pos > contorno().left+tam_padrao and lista_linha_alt[self._posicao_atual_y][self._posicao_atual_x-1] is None:
			self._x_pos -= passo
			self._posicao_atual_x -= 1
	
	
	def cair(self):
		'''verifica a existencia de itens abaixo ou linha base.
		retorna verdadeiro enquanto não houver colisão'''
		cair = False
		if self.get_rect[1]+self.tamanho_y+15 < contorno().bottom and lista_linha_alt[self._posicao_atual_y-1][self._posicao_atual_x] is None:
			cair = True
		
		if cair:
			self._y_pos += tam_padrao
			self._posicao_atual_y -= 1
		return cair
		
		
	def desenhar(self):
		return pygame.draw.rect(self._surface, self._cor, (self._x_pos, self._y_pos,self.tamanho_x,self.tamanho_y))
	
	@property
	def get_pos(self):
		return (self._posicao_atual_x, self._posicao_atual_y)
		
	
	@property
	def get_rect(self):
		return (self._x_pos, self._y_pos)


def contorno():
	'''desenha os limitadores do jogo e retorna um Rect'''
	return pygame.draw.rect(tela,BRANCO,(largura_tela//10*2.3,altura_tela//10,(largura_tela//10*5.3)-11,altura_tela//10*5),15,5)


def controles():
	'''desenha controles tatil.	retorna uma tupla com o rect da cada botao (direita,	esquerda, baixo)'''
	botao_direito = pygame.draw.polygon(tela, BRANCO,[(largura_tela//10*9, altura_tela//10*7), (largura_tela//10*10, altura_tela//10*8),(largura_tela//10*9,altura_tela//10*9)])
	botao_esquerdo = pygame.draw.polygon(tela, BRANCO,[(largura_tela//10*1,altura_tela//10*7),(0, altura_tela//10*8),(largura_tela//10*1,altura_tela//10*9)])
	botao_baixo = pygame.draw.polygon(tela,BRANCO,[(largura_tela//4,altura_tela*0.9),(largura_tela//2, altura_tela),(largura_tela//4*3, altura_tela*0.9)])
	return ((botao_direito),( botao_esquerdo), (botao_baixo))#retorna uma tupla com o rect de cada botao (direita, esquerda, baixo)


#CORES
BRANCO = (255,255,255)
PRETO = (0,0,0)
VERDE = (0,255,0)
VERDE_ESCURO = (0,100,0)
CIANO = (0,255,255)
AZUL = (0,0,255)
VERMELHO = (255,0,0)
LARANJA = (255,140,0)
OURO = (255,215,0)
ROSA_CHOQUE = (255,20,147)
INDIGO = (75,0,130)
VIOLETA = (148,0,211)

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
pygame.display.set_caption('Tetris 0.8')

contador = 0#faz uma contagem a cada quadro para simular uma pausa de 1 seg, sem pausar os calculos.

#listas e posicoes
pos_linha = contorno()[2]//tam_padrao
pos_coluna = contorno()[3]//tam_padrao
lista_linha_pos = [None for x in range(pos_linha)]#lista todas as posições dos quadrados parados
lista_linha_alt = [lista_linha_pos.copy() for x in range(pos_coluna)]#lista todas as colunas com quadrados

q1 = Quadrado(tam_padrao, largura_tela//2, tela)

while True:
	relogio.tick(fps)
	tela.fill(PRETO)
	q1.desenhar()
	contorno()#desenha o contorno
	controles()#desenha os controles

	#eventos de interação (contrles)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		if event.type == KEYDOWN:
			if event.key in (K_LEFT, K_a):
				q1.mover_esquerda(tam_padrao)
			if event.key in (K_RIGHT, K_l, K_d):
				q1.mover_direita(tam_padrao)
			if event.key in (K_SPACE, K_s):
				contador = fps
		if event.type == MOUSEBUTTONDOWN:
			if controles()[0].collidepoint(event.pos):
				q1.mover_direita(tam_padrao)
			if controles()[1].collidepoint(event.pos):
				q1.mover_esquerda(tam_padrao)
			if controles()[2].collidepoint(event.pos):
				contador = fps
			
	if contador < fps:#conta 1 seg antes de cair
		contador += 1
	else:
		contador = 0
		if not q1.cair():#se nao cair, verifica se a linha está completa e limpa a linha
			lista_linha_alt[q1.get_pos[1]][q1.get_pos[0]] = q1 #Adiciona o objeto q1 na posição correspondente
			if lista_linha_alt[q1.get_pos[1]].count(None) == 0:#completou a linha
				lista_linha_alt[q1.get_pos[1]] = [None for x in range(pos_linha)]#apaga os objetos da linha.
				
				#verifica se algum objeto ainda pode cair após limpar a linha de baixo
				for linha_alt in range(pos_coluna-1):
						for linha_pos in range(pos_linha):
							if lista_linha_alt[linha_alt][linha_pos] is not None:
								lista_linha_alt[linha_alt][linha_pos].cair()
								lista_linha_alt[linha_alt-1][linha_pos] = lista_linha_alt[linha_alt][linha_pos]
								lista_linha_alt[linha_alt][linha_pos] = None
					
			#Verifica o fim de jogo
			if lista_linha_alt[-1][pos_linha//2] is not None:
				lista_linha_pos = [None for x in range(pos_linha)]
				lista_linha_alt = [lista_linha_pos.copy() for x in range(pos_coluna)]

			q1 = Quadrado(tam_padrao, largura_tela//2, tela)
	
	#Desenhar os itens na tela
	for col in lista_linha_alt:
		for pos in col:
			if isinstance(pos,Quadrado):
				pos.desenhar()
				
	pygame.display.flip()

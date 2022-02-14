import pygame
from pygame.locals import *
from sys import exit
from random import choice

class Quadrado:
	'''Inicializa o quadrado'''
	def __init__(self, cor, tam, x, surface):
		self.tamanho_y = tam
		self.tamanho_x = tam*choice((1,1))
		self._cor = choice((VERDE, VERMELHO, AZUL))
		self._x_pos = x - tam_padrao//2
		self._y_pos = altura_tela*0.1
		self._surface = surface
		self._posicao_atual_x = 4#posição inicial/atual na lista_linha_pos
		self._posicao_atual_y = 0#posição inicial/atual na coluna (lista_linha_alt)


	def mover_direita(self, passo):
		if (self._x_pos+self.tamanho_x) <= (largura_tela//4*3-tam_padrao):
			self._x_pos += passo
			self._posicao_atual_x += 1


	def mover_esquerda(self, passo):
		if self._x_pos >= largura_tela//4+tam_padrao:
			self._x_pos -= passo
			self._posicao_atual_x -= 1
	
	
	def cair(self, vel):
		cair = False
		if self._y_pos+self.tamanho_y < altura_tela*0.9-self.tamanho_y:
			self._y_pos += vel
			self._posicao_atual_y += 1
			cair = True
		if self.desenhar()
		return cair
		
		
	def desenhar(self):
		return pygame.draw.rect(self._surface, self._cor, (self._x_pos, self._y_pos,self.tamanho_x,self.tamanho_y))



def contorno():#desenha os limitadores
	pygame.draw.lines(tela,BRANCO,True,((largura_tela//4+tam_padrao//2,altura_tela*0.1),(largura_tela//4+tam_padrao//2,altura_tela*0.9), (largura_tela//4*3-tam_padrao//2,altura_tela*0.9),(largura_tela//4*3-tam_padrao//2,altura_tela*0.1)), tam_padrao//10)


def controles():#desenha controles tatil
	botao_direito = pygame.draw.polygon(tela, BRANCO,[(largura_tela//4*3-tam_padrao//2, altura_tela//4), (largura_tela, altura_tela//2),(largura_tela//4*3-tam_padrao//2,altura_tela//4*3)])
	botao_esquerdo = pygame.draw.polygon(tela, BRANCO,[(largura_tela//4+tam_padrao//2,altura_tela//4),(0, altura_tela//2),(largura_tela//4+tam_padrao//2,altura_tela//4*3)])
	botao_baixo = pygame.draw.polygon(tela,BRANCO,[(largura_tela//4,altura_tela*0.9),(largura_tela//2, altura_tela),(largura_tela//4*3, altura_tela*0.9)])
	return ((botao_direito),( botao_esquerdo), (botao_baixo))#retorno uma tupla com os rect da cada botao (direita, esquerda, baixo)



#CORES
BRANCO = (255,255,255)
PRETO = (0,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)
VERMELHO = (255,0,0)

CEL = 0#

contador = 0#faz uma contagem a cada quadro para simular uma pausa de 1 seg, sem pausar os calculos.
lista_todos = list()#lista todos os quadrados que serão desenhados
lista_linha_pos = ['','','','','','','','','']#lista todos as posições dos quadrados parados
lista_linha_alt = list()#lista todas as colunas com quadrados


pygame.init()

fps = 60 #os calculos continuam acontecendo mesmo que o quadro não seja exibido.
relogio = pygame.time.Clock()


#Ajustes da tela
tela = pygame.display.set_mode()
largura_tela = tela.get_width()
altura_tela = tela.get_height()
print(f'X: {largura_tela}')
print(f'Y: {altura_tela}')
altura_tela = altura_tela-(555*CEL)
tam_padrao = (largura_tela//2)//10
pygame.display.set_caption('Tetris 0.5')



#

lista_todos.append(Quadrado(BRANCO,tam_padrao, largura_tela//2, tela))

while True:
	print(lista_todos[-1].desenhar())
	relogio.tick(fps)
	tela.fill(PRETO)
	contorno()#desenha o contorno
	if CEL == 1:
		controles()
	
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
		if event.type == MOUSEBUTTONDOWN and CEL ==1:
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
		if not lista_todos[-1].cair(tam_padrao):
			lista_linha_pos[lista_todos[-1]._posicao_atual_x] = lista_todos[-1]
			
			if lista_linha_pos.count('') == 0:#completou a linha
				print('Completou a linha')
				for c in range(0, 9):#A linha tem apenas 9 posições possíveis
					i = lista_todos.index(lista_linha_pos[c])
					del lista_todos[i]# --------- PENDENTE
				lista_linha_pos = ['','','','','','','','','']
			lista_todos.append(Quadrado(BRANCO,tam_padrao, largura_tela//2, tela))


	pygame.display.flip()

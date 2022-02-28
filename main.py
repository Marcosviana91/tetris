import pygame #install pip
from pygame.locals import *
from sys import exit
from random import choice


class Quadrado(Rect):
	'''Inicializa o quadrado:
		tam: comprimento e altura do objeto
		x: posição X onde o objeto será desenhado (sempre no meio da tela)
		'''
	def __init__(self, tam):
		self.left = largura_tela//2 - tam//2
		self.top = altura_tela//10
		self.height = tam
		self.width = tam * choice((1,1,1,2,2,3))
		self._cor = choice((VERDE, VERMELHO, AZUL,VERDE_ESCURO, CIANO, LARANJA, OURO, ROSA_CHOQUE, INDIGO, VIOLETA))


	def mover_direita(self, passo):
		mover = False
		if self.right+passo < contorno().right:
			mover = True
			for item in lista_todos:
				if self.collidepoint(item.centerx-tam_padrao, item.centery):
					mover = False
		if mover:
			snd_mover.play()
			self.left += passo


	def mover_esquerda(self, passo):
		mover = False
		if self.left-passo > contorno().left:
			mover = True
			for item in lista_todos:
				if self.collidepoint(item.centerx+tam_padrao, item.centery):
					mover = False
		if mover:
			snd_mover.play()
			self.left -= passo
	
	
	def cair(self):
		'''verifica a existencia de itens abaixo ou linha base.
		retorna verdadeiro enquanto não houver colisão'''
		cair = False
		if self.bottom+self.height < contorno().bottom:
			cair = True
			for item in lista_todos:
				if self.collidepoint(item.left, item.top-tam_padrao) or self.collidepoint(item.right-10, item.top-tam_padrao) or self.collidepoint(item.centerx, item.top-tam_padrao):
					cair = False
			if cair:
				snd_cair.play()
				self.top += tam_padrao
		return cair
		
		
	def desenhar(self, surface):
		pygame.draw.rect(surface, self._cor, (self.left, self.top,self.width,self.height))


def contorno():
	'''desenha os limitadores do jogo e retorna um Rect'''
	return pygame.draw.rect(tela,BRANCO,(largura_tela//2-(tam_padrao*2.5)-15,(altura_tela//10)-12,largura_tela/2+30,(altura_tela//10*5)+18),10,5)


def controles():
	'''desenha controles tatil.	retorna uma tupla com o rect da cada botao (direita,	esquerda, baixo)'''
	botao_direito = pygame.draw.polygon(tela, BRANCO,[(largura_tela//4*3, altura_tela//10*7), (largura_tela//10*10, altura_tela//10*8),(largura_tela//4*3,altura_tela//10*9)])
	botao_esquerdo = pygame.draw.polygon(tela, BRANCO,[(largura_tela//4,altura_tela//10*7),(0, altura_tela//10*8),(largura_tela//4,altura_tela//10*9)])
	botao_baixo = pygame.draw.polygon(tela,BRANCO,[(largura_tela//4,altura_tela*0.9),(largura_tela//2, altura_tela),(largura_tela//4*3, altura_tela*0.9)])
	return ((botao_direito),( botao_esquerdo), (botao_baixo))#retorna uma tupla com o rect de cada botao (direita, esquerda, baixo)


def limpar_linha(todos, y, tam):
	linha = []
	limpar = False
	for item in todos:
		if item[1] == y:
			linha.append(todos.index(item))
	soma = 0
	for x in linha:
		soma += todos[x][2]
	if soma == tam*5:
		limpar = True
		linha.sort(reverse=True)
		for x in linha:
			del todos[x]
		linha.clear()
	return (limpar, todos)


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
vel = 1
contador_max = fps

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

###TEXTOS###
ponto = 0
FONTE_PADRAO = pygame.font.get_default_font()
FONTE = pygame.font.SysFont(FONTE_PADRAO, tam_padrao)
FONTEp = pygame.font.SysFont(FONTE_PADRAO, tam_padrao//2)

###AUDIO### - https://themushroomkingdom.net/media/smw/wav
snd_linha_completa = pygame.mixer.Sound('smw_power-up.wav')
snd_linha_completa.set_volume(0.6)
snd_cair = pygame.mixer.Sound('smw_fireball.wav')
snd_cair.set_volume(0.6)
snd_mover = pygame.mixer.Sound('smw_lava_bubble.wav')
snd_mover.set_volume(0.6)
snd_novo_quad = pygame.mixer.Sound('smw_swimming.wav')
snd_game_over = pygame.mixer.Sound('smw_game_over.wav')
snd_game_over.set_volume(0.6)

contador = 0#faz uma contagem a cada quadro para simular uma pausa de 1 seg, sem pausar os calculos.

#lista de quadrados
lista_todos = []

q1 = Quadrado(tam_padrao)
snd_novo_quad.play()

while True:
	relogio.tick(fps)
	tela.fill(PRETO)
	q1.desenhar(tela)
	contorno()#desenha o contorno
	controles()#desenha os controles
	#HUD
	mensagem_ponto = f'Pontuação: {ponto}'
	mensagem_vel = f'Velocidade: {vel}'
	mensagem_ponto_formatada = FONTE.render(mensagem_ponto, True, VERDE)
	mensagem_vel_formatada = FONTEp.render(mensagem_vel,True,VERDE)
	mensagem_fim_de_jogo = ['FIM DE JOGO','APERTE R PARA CONTINUAR']
	mensagem_fim_de_jogo_linha1 = FONTE.render(mensagem_fim_de_jogo[0], True, VERMELHO)
	mensagem_fim_de_jogo_linha2 = FONTEp.render(mensagem_fim_de_jogo[1], True, OURO)
	

	#eventos de interação (controles)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		if event.type == KEYDOWN:
			if event.key in (K_LEFT, K_a):
				q1.mover_esquerda(tam_padrao)
			if event.key in (K_RIGHT, K_l, K_d):
				q1.mover_direita(tam_padrao)
			if event.key in (K_SPACE, K_s, K_DOWN):
				contador = fps
		if event.type == MOUSEBUTTONDOWN:
			if controles()[0].collidepoint(event.pos):
				q1.mover_direita(tam_padrao)
			if controles()[1].collidepoint(event.pos):
				q1.mover_esquerda(tam_padrao)
			if controles()[2].collidepoint(event.pos):
				contador = fps
			
	if contador < contador_max:#conta 1 seg antes de cair
		contador += vel
	else:
		contador = 0
		if not q1.cair():
			lista_todos.append(q1) #Adiciona o objeto
			
			if limpar_linha(lista_todos, q1.y, tam_padrao)[0]:
				snd_linha_completa.play()
				ponto += 5
				vel += 1
				
				#verifica se algum objeto ainda pode cair após limpar a linha de baixo
			for quad in lista_todos:
				while quad.cair():
					quad.cair()
				limpou = limpar_linha(lista_todos, quad.y, tam_padrao)
				if limpou[0]:
					#lista_todos.clear()
					lista_todos = limpou[1].copy()
			q1 = Quadrado(tam_padrao)
			snd_novo_quad.play()
			#Verifica o fim de jogo
			if len(lista_todos) > 0 and q1.colliderect(lista_todos[-1]):
				fim_de_jogo = True
				snd_game_over.play()
				tela.fill(PRETO)
				text1 = mensagem_fim_de_jogo_linha1.get_rect().center[0]
				text2 = mensagem_fim_de_jogo_linha2.get_rect().center[0]
				tela.blit(mensagem_fim_de_jogo_linha1, (largura_tela//2-text1,altura_tela//2))
				fim_button = tela.blit(mensagem_fim_de_jogo_linha2, (largura_tela//2-text2,(altura_tela//2)+tam_padrao*2))
				tela.blit(mensagem_ponto_formatada, (largura_tela//2-text2,(altura_tela//2)+tam_padrao))
				
				pygame.display.update()
				while fim_de_jogo:
					for event in pygame.event.get():
						if event.type == QUIT:
							pygame.quit()
							exit()
						if event.type == KEYDOWN:
							if event.key == K_r:
								fim_de_jogo = False
						if event.type == MOUSEBUTTONDOWN:
							if fim_button.collidepoint(event.pos):
								fim_de_jogo = False
								
				lista_todos.clear()
				snd_game_over.stop()
				ponto = 0
				vel = 1
	
	#Desenhar os itens na tela
	for quad in lista_todos:
		quad.desenhar(tela)
				
	tela.blit(mensagem_ponto_formatada, (0,0))
	tela.blit(mensagem_vel_formatada,(0,tam_padrao))
	pygame.display.flip()

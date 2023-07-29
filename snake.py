# Importando as bibliotecas necessárias
import pygame, sys, random
from pygame.math import Vector2


# Definindo a classe da cobra
class Snake:
	def __init__(self):
		# Inicialização da cobra com três blocos em uma posição inicial fixa (5, 10), (4, 10) e (3, 10)
		self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
		self.direction = Vector2(0, 0)  # A direção inicial é nula, pois a cobra não está se movendo no início.
		self.new_block = False

		# Carregando as imagens da cabeça e da cauda da cobra, bem como as imagens do corpo e suas intersecções.
		self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
		self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
		self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
		self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
		self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
		self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
		self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
		self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

		self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
		self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

		self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
		self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
		self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
		self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

		# Carregando o som que será reproduzido quando a cobra comer uma maçã.
		self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

	# Método para desenhar a cobra na tela.
	def draw_snake(self):
		# Atualizando as imagens da cabeça e cauda da cobra.
		self.update_head_graphics()
		self.update_tail_graphics()

		# Desenhando cada bloco da cobra na tela de acordo com sua posição e aparência.
		for index, block in enumerate(self.body):
			x_pos = int(block.x * cell_size)
			y_pos = int(block.y * cell_size)
			block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

			# Desenhando a cabeça da cobra no primeiro bloco do corpo.
			if index == 0:
				screen.blit(self.head, block_rect)
			# Desenhando a cauda da cobra no último bloco do corpo.
			elif index == len(self.body) - 1:
				screen.blit(self.tail, block_rect)
			# Desenhando o corpo da cobra nos blocos intermediários.
			else:
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				if previous_block.x == next_block.x:
					screen.blit(self.body_vertical, block_rect)
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal, block_rect)
				else:
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
						screen.blit(self.body_tl, block_rect)
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
						screen.blit(self.body_bl, block_rect)
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
						screen.blit(self.body_tr, block_rect)
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
						screen.blit(self.body_br, block_rect)

	# Método para atualizar a imagem da cabeça da cobra com base em sua direção.
	def update_head_graphics(self):
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(1, 0):
			self.head = self.head_left
		elif head_relation == Vector2(-1, 0):
			self.head = self.head_right
		elif head_relation == Vector2(0, 1):
			self.head = self.head_up
		elif head_relation == Vector2(0, -1):
			self.head = self.head_down

	# Método para atualizar a imagem da cauda da cobra com base na posição do penúltimo e último blocos do corpo.
	def update_tail_graphics(self):
		tail_relation = self.body[-2] - self.body[-1]
		if tail_relation == Vector2(1, 0):
			self.tail = self.tail_left
		elif tail_relation == Vector2(-1, 0):
			self.tail = self.tail_right
		elif tail_relation == Vector2(0, 1):
			self.tail = self.tail_up
		elif tail_relation == Vector2(0, -1):
			self.tail = self.tail_down

	# Método para mover a cobra.
	def move_snake(self):
		# Se a cobra deve crescer, adiciona um novo bloco à frente dela.
		if self.new_block:
			body_copy = self.body[:]
			body_copy.insert(0, body_copy[0] + self.direction)
			self.body = body_copy[:]
			self.new_block = False
		# Caso contrário, atualiza as posições dos blocos do corpo para movimentar a cobra.
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0, body_copy[0] + self.direction)
			self.body = body_copy[:]

	# Método chamado quando a cobra come uma maçã para adicionar um novo bloco no próximo movimento.
	def add_block(self):
		self.new_block = True

	# Método para reproduzir o som de "crunch" quando a cobra come uma maçã.
	def play_crunch_sound(self):
		self.crunch_sound.play()

	# Método para redefinir a cobra para sua configuração inicial.
	def reset(self):
		self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
		self.direction = Vector2(0, 0)

# Definindo a classe das maçãs
class Fruit:
	def __init__(self):
		self.randomize()

	# Método para desenhar a maçã na tela.
	def draw_fruit(self):
		fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
		screen.blit(apple, fruit_rect)

	# Método para escolher uma posição aleatória para a maçã dentro da área do jogo.
	def randomize(self):
		self.x = random.randint(0, cell_number - 1)
		self.y = random.randint(0, cell_number - 1)
		self.pos = Vector2(self.x, self.y)


# Definindo a classe principal do jogo
class MAIN:
	def __init__(self):
		# Criando instâncias das classes da cobra e das maçãs
		self.snake = SNAKE()
		self.fruit = Fruit()

	# Método para atualizar o estado do jogo a cada frame
	def update(self):
		self.snake.move_snake()  # Movendo a cobra
		self.check_collision()   # Verificando colisões
		self.check_fail()        # Verificando se o jogo terminou

	# Método para desenhar os elementos do jogo na tela
	def draw_elements(self):
		self.draw_grass()       # Desenhando o fundo da tela (grama)
		self.fruit.draw_fruit() # Desenhando a maçã
		self.snake.draw_snake() # Desenhando a cobra
		self.draw_score()       # Desenhando a pontuação

	# Método para verificar se a cobra colidiu com a maçã
	def check_collision(self):
		if self.fruit.pos == self.snake.body[0]:
			self.fruit.randomize()   # Atualizando a posição da maçã
			self.snake.add_block()   # Adicionando um novo bloco à cobra
			self.snake.play_crunch_sound()  # Reproduzindo o som de "crunch"

	# Método para verificar se o jogo terminou devido à colisão da cobra com as bordas da tela ou consigo mesma
	def check_fail(self):
		# Verificando colisão com as bordas da tela
		if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
			self.game_over()

		# Verificando colisão com o próprio corpo
		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				self.game_over()

	# Método chamado quando o jogo termina
	def game_over(self):
		self.snake.reset()  # Reiniciando a cobra

	# Método para desenhar o fundo da tela com quadrados verdes simulando grama.
	def draw_grass(self):
		grass_color = (167, 209, 61)
		for row in range(cell_number):
			if row % 2 == 0:
				for col in range(cell_number):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
						pygame.draw.rect(screen, grass_color, grass_rect)
			else:
				for col in range(cell_number):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
						pygame.draw.rect(screen, grass_color, grass_rect)

	# Método para desenhar a pontuação atual na tela.
	def draw_score(self):
		score_text = str(len(self.snake.body) - 3)
		score_surface = game_font.render(score_text, True, (56, 74, 12))
		score_x = int(cell_size * cell_number - 60)
		score_y = int(cell_size * cell_number - 40)
		score_rect = score_surface.get_rect(center=(score_x, score_y))
		apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)

		pygame.draw.rect(screen, (167, 209, 61), bg_rect)
		screen.blit(score_surface, score_rect)
		screen.blit(apple, apple_rect)
		pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)


# Inicialização do Pygame e configurações iniciais do jogo
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 15
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

# Definindo um evento personalizado para atualizar a tela a cada 150 milissegundos (150 ms).
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Instanciando a classe MAIN para criar o jogo.
# main_game = MAIN()

# Loop principal do jogo
"""
while True:
	# Processando os eventos do Pygame
	for event in pygame.event.get():
		# Verificando se o jogador fechou a janela do jogo
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		# Verificando se o evento de atualização da tela ocorreu (150 ms passaram)
		if event.type == SCREEN_UPDATE:
			main_game.update()  # Atualizando o jogo

		# Verificando se alguma tecla foi pressionada
		if event.type == pygame.KEYDOWN:
			# Mudando a direção da cobra com base na tecla pressionada pelo jogador
			if event.key == pygame.K_UP:
				if main_game.snake.direction.y != 1:
					main_game.snake.direction = Vector2(0, -1)
			if event.key == pygame.K_RIGHT:
				if main_game.snake.direction.x != -1:
					main_game.snake.direction = Vector2(1, 0)
			if event.key == pygame.K_DOWN:
				if main_game.snake.direction.y != -1:
					main_game.snake.direction = Vector2(0, 1)
			if event.key == pygame.K_LEFT:
				if main_game.snake.direction.x != 1:
					main_game.snake.direction = Vector2(-1, 0)

	# Preenchendo a tela com a cor de fundo
	screen.fill((175, 215, 70))

	# Desenhando os elementos do jogo na tela
	main_game.draw_elements()

	# Atualizando a tela
	pygame.display.update()

	# Limitando o número de frames por segundo (FPS) para 60
	clock.tick(60)
"""

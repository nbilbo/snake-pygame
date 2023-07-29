import pygame, sys, random
from pygame.math import Vector2

from snake import Snake, Fruit


class GameScene:
    def __init__(self, screen, SCREEN_UPDATE, cell_number, cell_size, game_font, apple, clock, player_name):
		# Criando instâncias das classes da cobra e das maçãs
        self.screen = screen
        self.cell_number = cell_number
        self.cell_size = cell_size
        self.game_font = game_font
        self.apple = apple
        self.clock = clock
        self.player_name = player_name
        self.snake = Snake()
        self.fruit = Fruit()

        while True:
        # Processando os eventos do Pygame
            for event in pygame.event.get():
                # Verificando se o jogador fechou a janela do jogo
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Verificando se o evento de atualização da tela ocorreu (150 ms passaram)
                if event.type == SCREEN_UPDATE:
                    self.update()  # Atualizando o jogo

                # Verificando se alguma tecla foi pressionada
                if event.type == pygame.KEYDOWN:
                    # Mudando a direção da cobra com base na tecla pressionada pelo jogador
                    if event.key == pygame.K_UP:
                        if self.snake.direction.y != 1:
                            self.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_RIGHT:
                        if self.snake.direction.x != -1:
                            self.snake.direction = Vector2(1, 0)
                    if event.key == pygame.K_DOWN:
                        if self.snake.direction.y != -1:
                            self.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT:
                        if self.snake.direction.x != 1:
                            self.snake.direction = Vector2(-1, 0)

	# Preenchendo a tela com a cor de fundo
            self.screen.fill((175, 215, 70))

	# Desenhando os elementos do jogo na tela
            self.draw_elements()

	# Atualizando a tela
            pygame.display.update()

	# Limitando o número de frames por segundo (FPS) para 60
            self.clock.tick(60)

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
        self.draw_score()       # Desenhando a pontuaçãa

	# Método para verificar se a cobra colidiu com a maçã
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()   # Atualizando a posição da maçã
            self.snake.add_block()   # Adicionando um novo bloco à cobra
            self.snake.play_crunch_sound()  # Reproduzindo o som de "crunch"

	# Método para verificar se o jogo terminou devido à colisão da cobra com as bordas da tela ou consigo mesma
    def check_fail(self):
		# Verificando colisão com as bordas da tela
        if not 0 <= self.snake.body[0].x < self.cell_number or not 0 <= self.snake.body[0].y < self.cell_number:
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
        for row in range(self.cell_number):
            if row % 2 == 0:
                for col in range(self.cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                        pygame.draw.rect(self.screen, grass_color, grass_rect)
            else:
                for col in range(self.cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                        pygame.draw.rect(self.screen, grass_color, grass_rect)

	# Método para desenhar a pontuação atual na tela.
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = self.game_font.render(score_text, True, (56, 74, 12))
        score_x = int(self.cell_size * self.cell_number - 60)
        score_y = int(self.cell_size * self.cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        self.apple_rect = self.apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(self.apple_rect.left, self.apple_rect.top, self.apple_rect.width + score_rect.width + 6, self.apple_rect.height)

        pygame.draw.rect(self.screen, (167, 209, 61), bg_rect)
        self.screen.blit(score_surface, score_rect)
        self.screen.blit(self.apple, self.apple_rect)
        pygame.draw.rect(self.screen, (56, 74, 12), bg_rect, 2)

        # player name
        # game_score_font = pygame.font.SysFont("consolas", 40)
        game_score_font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 25)
        game_score_surface = game_score_font.render(self.player_name, True, (0, 0, 0))
        game_score_rect = game_score_surface.get_rect()
        game_score_rect.midtop = (400, 15)
        self.screen.blit(game_score_surface, game_score_rect)


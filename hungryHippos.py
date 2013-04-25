#!/usr/bin/env python

import pygame
import random
import math
from pygame.sprite import Sprite

pygame.display.init()
pygame.font.init()
HEIGHT_RES = 768
WIDTH_RES = 768
totalScore = 0

class Menu:
    field_list = []
    field = []
    dest_surface = pygame.Surface
    number_fields = 0
    background_color = (52, 73, 94)
    font_size = 36
    font_color =  (255, 255, 255)
    selection_color = (26, 188, 156)
    selection_position = 0
    position = (0,0)
    menu_width = 0
    menu_height = 0

    class Field:
    	text = ''
    	field = pygame.Surface
    	field_rect = pygame.Rect
    	selection_rect = pygame.Rect

    def move_menu(self, top, left):
    	self.position = (top, left)

    def set_colors(self, text, selection, background):
    	self.background_color = background
    	self.font_color = text
    	self.selection_color = selection

    def get_position(self):
    	return self.selection_position

    def init(self, item_list, dest_surface):
    	self.field_list = item_list
    	self.dest_surface = dest_surface
    	self.number_fields = len(self.field_list)
    	self.create_structures()

    def draw(self, move=0):
        if move:
            self.selection_position += move 
            if self.selection_position == -1:
                self.selection_position = self.number_fields - 1
            self.selection_position %= self.number_fields
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.background_color)
        selection_rect = self.field[self.selection_position].selection_rect
        pygame.draw.rect(menu, self.selection_color, selection_rect)

        for i in xrange(self.number_fields):
            menu.blit(self.field[i].field, self.field[i].field_rect)
        self.dest_surface.blit(menu, self.position)
        return self.selection_position

    def create_structures(self):
        shift = 0
        self.menu_height = 0
        self.font = pygame.font.Font(None, self.font_size)
        for i in xrange(self.number_fields):
            self.field.append(self.Field())
            self.field[i].text = self.field_list[i]
            self.field[i].field = self.font.render(self.field[i].text, 1, self.font_color)

            self.field[i].field_rect = self.field[i].field.get_rect()
            shift = int(self.font_size * 0.2)

            height = self.field[i].field_rect.height
            self.field[i].field_rect.left = shift
            self.field[i].field_rect.top = shift + (shift * 2 + height) * i

            width = self.field[i].field_rect.width + shift*2
            height = self.field[i].field_rect.height + shift*2            
            left = self.field[i].field_rect.left - shift
            top = self.field[i].field_rect.top - shift
            if width > self.menu_width:
            	self.menu_width = width
            else:
            	width = self.menu_width

            self.field[i].selection_rect = (left, top, width, height)
            self.menu_height += height
        x = self.dest_surface.get_rect().centerx - self.menu_width / 2
        y = self.dest_surface.get_rect().centery - self.menu_height / 2
        mx, my = self.position
        self.position = (x + mx, y + my) 

class Hippo(Sprite):
	""" HANDLES HIPPO BEHAVIOURS """
	def __init__(self, position, player):
		Sprite.__init__(self)
		self.player = player
		self.loadImage()
		self.image = self.imageBwd
		self.rect = pygame.Rect(position, (100,100))
		self.position = position
		# FALSE = back TRUE = Forward
		self.state = False

	def loadImage(self):
		if(self.player == 1):
			self.imageBwd = pygame.image.load('Images/Hippo1.png')
			self.imageFwd = pygame.image.load('Images/Hippo1Fwd.png')
		elif(self.player == 2):
			self.imageBwd = pygame.image.load('Images/Hippo2.png')
			self.imageFwd = pygame.image.load('Images/Hippo2Fwd.png')
		elif(self.player == 3):
			self.imageBwd = pygame.image.load('Images/Hippo3.png')
			self.imageFwd = pygame.image.load('Images/Hippo3Fwd.png')
		elif(self.player == 4):
			self.imageBwd = pygame.image.load('Images/Hippo4.png')
			self.imageFwd = pygame.image.load('Images/Hippo4Fwd.png')

	def forward(self):
		self.image = self.imageFwd
		if (self.player == 2):
			self.rect = pygame.Rect((self.position[0]-100, self.position[1]), (200, 100))
			pass
		elif (self.player == 4):
			self.rect = pygame.Rect((self.position[0], self.position[1]-100), (200, 100))
		else:
			self.rect = pygame.Rect(self.position, (200, 100))
		pygame.draw.rect(self.image, pygame.Color("black"), self.rect)
		self.state = True

	def back(self):
		self.image = self.imageBwd
		self.rect = pygame.Rect(self.position, (100, 100))
		pygame.draw.rect(self.image, pygame.Color("black"), self.rect)
		self.state = False

		
class Ball(Sprite):
	""" HANDLES BALL BEHAVIOURS """
	def __init__(self, color, score, hippos):
		Sprite.__init__(self)
		self.image = pygame.Surface((20, 20))
		self.image.set_colorkey(pygame.Color("black"))
		pygame.draw.circle(self.image, pygame.Color(color), (10, 10), 10)

		self.hippos = hippos
		self.score = score
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH_RES/2, HEIGHT_RES/2)
		angle = random.uniform(0, (math.pi/2)-0.18) # 0.18 ~= 10 degress
		angle *= random.choice([-1,1])
		side = random.choice([-1,1])
		self.velocity = [side * 15 * math.cos(angle), 15 * math.sin(angle)]
		self.start = (WIDTH_RES/2, HEIGHT_RES/2)

	def update(self):
		self.rect.move_ip(*self.velocity)
		# Detect if eaten
		for hippo in self.hippos:
			if self.rect.colliderect(hippo.rect):
				if hippo.state == True:
					for score in self.score:
						if score.player == hippo.player:
							self.score[score.player-1].increase()
					self.rect.center = self.start
					self.velocity = [0, 0]
					self.image.set_alpha(0)
					global totalScore
					totalScore += 1
					return True
				else:
					self.velocity[0] *= -1
					self.velocity[1] *= -1

		# bounce ball of the top screen border
		if self.rect.top < 0:
			self.velocity[1] *= -1
			self.rect.top = 1
		# bounce ball off bottom screen border
		elif self.rect.bottom > HEIGHT_RES:
			self.velocity[1] *= -1
			self.rect.bottom = HEIGHT_RES-1
		# bounce ball off left screen border
		elif self.rect.left < 0:
			self.velocity[0] *= -1
			self.rect.left = 1
		# bounce ball off right screen border
		elif self.rect.right > WIDTH_RES:
			self.velocity[0] *= -1
			self.rect.right = WIDTH_RES-1
		return False

class Score(Sprite):
	def __init__(self, color, position, player):
		pygame.sprite.Sprite.__init__(self)

		self.color = pygame.Color(color)
		if(player <= 2):
			self.size = (20,300)
		else:
			self.size = (300, 20)

		self.image = pygame.Surface(self.size)
		self.image.set_colorkey(pygame.Color("black"))
		self.player = player
		self.score = 0
		self.rect = pygame.Rect(position, self.size)
		self.render_balls()

	def render_balls(self):
		for i in range (0, self.score):
			if(self.player <= 2):
				pygame.draw.circle(self.image, self.color, (10, (i*20)+10), 10)
			else:
				pygame.draw.circle(self.image, self.color, ((i*20)+10, 10), 10)

	def increase(self):
		self.score += 1
		self.render_balls()

class ScoreBalls(Sprite):
	"""docstring for ScoreBalls"""
	def __init__(self, Score):
		pygame.sprite.Sprite.__init__(self)
		self.score = Score

	def render_balls(self):
		for i in range (0, self.score):
			pygame.draw.circle(self.image, pygame.Color(color), (i*10, 10), 10)

		
def main():
	def nop():
		pass

	def createBall(players):
		if players == 2:
			return Ball("white", [score1, score2], [player1, player2])
		elif players == 3:
			return Ball("white", [score1, score2, score3], [player1, player2, player3])
		elif players == 4:
			return Ball("white", [score1, score2, score3, score4], [player1, player2, player3, player4])

	def getWinner(scores):
		highScore = 0
		for score in scores:
			if score.score > highScore:
				highScore = score.score
				winner = score.player
		return winner

	# SET RESOLUTION
	screen = pygame.display.set_mode((WIDTH_RES, HEIGHT_RES))
	background = pygame.image.load('Images/background.png')
	screen.blit(background,(0, 0))
	players = 0
	menu = Menu()
	menu.init([' 2 player ', ' 3 player ', ' 4 player '], screen)
	menu.draw()
	clock = pygame.time.Clock()
	start_menu = True
	running_game = True
	win_menu = True

	# INITAL GAME LOOP PRESENTING MENU
	while start_menu:
		clock.tick(60)
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running_game = False
				start_menu = False
				win_menu = False
			elif event.type == pygame.KEYDOWN:
			   	if event.key == pygame.K_UP:
			   		menu.draw(-1)
			  	elif event.key == pygame.K_DOWN:
				   	menu.draw(1)
			  	elif event.key == pygame.K_RETURN:
				   	if menu.get_position() == 0:
				   		players = 2
				   	elif menu.get_position() == 1:
				   		players = 3
				   	elif menu.get_position() == 2:
				   		players = 4
				   	start_menu = False

	# THIS RUNS WHEN NUMBER OF PLAYERS HAS BEEN CHOSEN
	# RESET SCREEN
	screen = pygame.display.set_mode((WIDTH_RES, HEIGHT_RES))
	background = pygame.image.load('Images/background.png')
	screen.blit(background,(0, 0))

	# INITIALIZE SPRITES BASED ON PLAYERS
	if players >= 2:
		score1 = Score("white", (20, 10), 1)
		score2 = Score("white", ((WIDTH_RES-40, (HEIGHT_RES/2)+70)), 2)
		scoreList = [score1, score2]
		player1 = Hippo((0, (HEIGHT_RES/2)-50), 1)
		player2 = Hippo((WIDTH_RES-100, (HEIGHT_RES/2)-50), 2)
		sprites = pygame.sprite.RenderClear([score1, score2, player1, player2])
		# KEYMAP
		key_map = {
			pygame.K_q: [player1.forward, player1.back],
			pygame.K_p: [player2.forward, player2.back]
		}
	if players >= 3:
		score3 = Score("white", ((WIDTH_RES/2)+70, 20), 3)
		scoreList = [score1, score2, score3]
		player3 = Hippo(((WIDTH_RES/2)-50, 0), 3)
		sprites = pygame.sprite.RenderClear([score1, score2, score3, player1, player2, player3])
		# KEYMAP
		key_map = {
			pygame.K_q: [player1.forward, player1.back],
			pygame.K_p: [player2.forward, player2.back],
			pygame.K_m: [player3.forward, player3.back]
		}
	if players == 4:
		score4 = Score("white", (10, HEIGHT_RES-40), 4)
		scoreList = [score1, score2, score3, score4]
		player4 = Hippo(((WIDTH_RES/2)-50, HEIGHT_RES-100), 4)
		sprites = pygame.sprite.RenderClear([score1, score2, score3, score4, player1, player2, player3, player4])
		# KEYMAP
		key_map = {
			pygame.K_q: [player1.forward, player1.back],
			pygame.K_p: [player2.forward, player2.back],
			pygame.K_m: [player3.forward, player3.back],
			pygame.K_z: [player4.forward, player4.back]
		}

	ball1 = createBall(players)

	# INITIALISE LIST OF BALLS
	ballList = [ball1]
	ballSprite = pygame.sprite.RenderClear(ballList)
	global totalScore

	counter = 0
	clock = pygame.time.Clock()
	# GAME LOOP
	running_game = True
	while running_game:
		clock.tick(60)
		counter += 1
		sprites.update()
		ballSprite.update()
		# EVERY 3 SECONDS ADD A NEW BALL TO BALL LIST
		if (counter%60 == 0 and len(ballList) < players*10):
			ballList.append(createBall(players))
			ballSprite = pygame.sprite.RenderClear(ballList)
		sprites.draw(screen)
		ballSprite.draw(screen)
		pygame.display.flip()
		sprites.clear(screen, background)
		ballSprite.clear(screen, background)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running_game = False
				win_menu = False
			elif event.type == pygame.KEYDOWN and event.key in key_map:
				key_map[event.key][0]()
			elif event.type == pygame.KEYUP and event.key in key_map:
				key_map[event.key][1]()

		if totalScore == players*10:
			running_game = False

	menu = Menu()
	winner = getWinner(scoreList)
	menu.init(['Player '+str(winner)+' Wins!', '  Play again  ', '     Quit     '], screen)
	menu.draw()

	while win_menu:
		clock.tick(60)
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				win_menu = False
			elif event.type == pygame.KEYDOWN:
			   	if event.key == pygame.K_UP:
			   		menu.draw(-1)
			  	elif event.key == pygame.K_DOWN:
				   	menu.draw(1)
			  	elif event.key == pygame.K_RETURN:
				   	if menu.get_position() == 1:
				  		main()
				   	elif menu.get_position() == 2:
				   		win_menu = False

if __name__ == "__main__":
	main()
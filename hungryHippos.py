#!/usr/bin/env python

import pygame
import random
import math
from pygame.sprite import Sprite
from menu import Menu

pygame.display.init()
pygame.font.init()
HEIGHT_RES = 768
WIDTH_RES = 768
totalScore = 0

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
		if self.player == 2:
			self.rect = pygame.Rect((self.position[0]-100, self.position[1]), (200, 100))
		elif self.player == 3:
			self.rect = pygame.Rect(self.position, (100, 200))
		elif self.player == 4:
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
	def __init__(self, score, hippos):
		Sprite.__init__(self)
		self.setImage()

		self.hippos = hippos
		self.score = score
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH_RES/2, HEIGHT_RES/2)

		angle = random.uniform(0, (math.pi/2)-0.18) # 0.18 ~= 10 degress
		angle *= random.choice([-1,1])
		side = random.choice([-1,1])
		self.setVelocity(side, angle)
		self.start = (WIDTH_RES/2, HEIGHT_RES/2)

	def setImage(self):
		self.image = pygame.image.load('Images/ball.png')

	def setVelocity(self, side, angle):
		self.velocity = [side * 15 * math.cos(angle), 15 * math.sin(angle)]

	def adjustScore(self, player):
		self.score[player-1].increase()

	def update(self):
		global totalScore
		#  If ball is in play edit trajectory
		if self.image.get_alpha() != 0:
			self.velocity[0] += 0.01
	 		self.velocity[1] -= 0.01

		self.rect.move_ip(*self.velocity)

		# Detect if eaten
		for hippo in self.hippos:
			if self.rect.colliderect(hippo.rect):
				if hippo.state == True:
					for score in self.score:
						if score.player == hippo.player:
							self.adjustScore(score.player)
					self.rect.center = self.start
					self.velocity = [0, 0]
					self.image = pygame.Surface((0,0))
					totalScore += 1
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

class damageBall(Ball):
	""" HANDLES DAMAGE_BALL BEHAVIOURS """
	def setImage(self):
		self.image = pygame.image.load('Images/Bomb.png')

	def setVelocity(self, side, angle):
		self.velocity = [side * 10 * math.cos(angle), 10 * math.sin(angle)]

	def adjustScore(self, player):
		self.score[player-1].decrease()

class Score(Sprite):
	def __init__(self, position, player):
		pygame.sprite.Sprite.__init__(self)
		self.color = pygame.Color("white")
		self.player = player
		self.score = 0
		self.draw(position)
			
	def draw(self, position):
		self.position = position
		if self.player <= 2:
			self.size = (20,300)
		else:
			self.size = (300, 20)
		self.image = pygame.Surface(self.size)
		self.image.set_colorkey(pygame.Color("black"))
		self.rect = pygame.Rect(self.position, self.size)
		self.render()
		self.rect.center = position

	def render(self):
		self.image = pygame.Surface(self.size)
		self.image.set_colorkey(pygame.Color("black"))
		self.rect = pygame.Rect(self.position, self.size)
		for i in range (0, self.score):
			if self.player <= 2:
				pygame.draw.circle(self.image, self.color, (10, (i*20)+10), 10)
			else:
				pygame.draw.circle(self.image, self.color, ((i*20)+10, 10), 10)

	def increase(self):
		self.score += 1
		self.render()

	def decrease(self):
		self.score -= 2
		self.render()

class textScore(Score):
	def draw(self, position):
		if self.player == 1:
			self.position = (20, (HEIGHT_RES/2)-70)
		elif self.player == 2:
			self.position = (WIDTH_RES-40, (HEIGHT_RES/2)+70)
		elif self.player == 3:
			self.position = ((WIDTH_RES/2)+70, 20)
		elif self.player == 4:
			self.position = ((WIDTH_RES/2)-70, HEIGHT_RES-40)
		self.font = pygame.font.Font("pixelated_bold.ttf", 36)
		self.render()
		self.rect = self.image.get_rect()
		self.rect.center = self.position

	def render(self):
		self.image = self.font.render(str(self.score), True, self.color)

def setScreen(screen, background):
	screen = pygame.display.set_mode((WIDTH_RES, HEIGHT_RES))
	background = pygame.image.load('Images/background.png')
	screen.blit(background,(0, 0))

def createBall(scoreList, playerList):
	if random.randint(1,10) == 1:
		return damageBall(scoreList, playerList)
	else:
		return Ball(scoreList, playerList)

def createScore(position, player, apocalypse):
	if apocalypse:
		return textScore(position, player)
	else:
		return Score(position, player)

def getWinner(scores):
		highScore = 0
		winner = 0
		for score in scores:
			if score.score > highScore:
				highScore = score.score
				winner = score.player
		return winner

def main():

	global totalScore
	players = 0
	counter = 0
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((WIDTH_RES, HEIGHT_RES))
	background = pygame.image.load('Images/background.png')
	game_menu = True
	player_menu = True
	running_game = True
	win_menu = True
	apocalypse = False
	multiplayer = False
	singleplayer = False

	# Game type menu
	setScreen(screen, background)

	menu = Menu()
	menu.init([' HUNGRY HIPPOS ', '  infinite mode ', '  multiplayer ', '  single player '], screen, True)
	menu.draw()

	while game_menu:
		clock.tick(60)
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_menu = False
				player_menu = False
				running_game = False
				win_menu = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
			   		menu.draw(-1)
			  	elif event.key == pygame.K_DOWN:
				   	menu.draw(1)
			  	elif event.key == pygame.K_RETURN:
				   	if menu.get_position() == 1:
				   		apocalypse = True
				   	elif menu.get_position() == 2:
				   		multiplayer = True
				   	elif menu.get_position() == 3:
				   		singleplayer = True
				   	if menu.get_position() != 0:
 				   		game_menu = False


	# Player choice menu
	setScreen(screen, background)

	menu = Menu()
	menu.init(['  2 player ', '  3 player ', '  4 player ', '  back '], screen, False)
	menu.draw()

	while player_menu:
		clock.tick(60)
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running_game = False
				player_menu = False
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
				   	elif menu.get_position() == 3:
				   		main()
				   	player_menu = False

	# Reset Screen to start game
	setScreen(screen, background)

	# Initialize Sprites based on user chosen players.
	if players >= 2:
		score1 = createScore((20, 24), 1, apocalypse)
		score2 = createScore(((WIDTH_RES-40, (HEIGHT_RES/2)+60)), 2, apocalypse)
		scoreList = [score1, score2]
		player1 = Hippo((0, (HEIGHT_RES/2)-50), 1)
		player2 = Hippo((WIDTH_RES-100, (HEIGHT_RES/2)-50), 2)
		playerList = [player1, player2]
		key_map = {
			pygame.K_q: [player1.forward, player1.back],
			pygame.K_p: [player2.forward, player2.back]
		}

	if players >= 3:
		score3 = createScore(((WIDTH_RES/2)+70, 20), 3, apocalypse)
		scoreList.append(score3)
		player3 = Hippo(((WIDTH_RES/2)-50, 0), 3)
		playerList.append(player3)
		key_map[pygame.K_m] = [player3.forward, player3.back]

	if players == 4:
		score4 = createScore((10, HEIGHT_RES-40), 4, apocalypse)
		scoreList.append(score4)
		player4 = Hippo(((WIDTH_RES/2)-50, HEIGHT_RES-100), 4)
		playerList.append(player4)
		key_map[pygame.K_z] = [player4.forward, player4.back]

	sprites = pygame.sprite.RenderClear(scoreList + playerList)
	ball = createBall(scoreList, playerList)

	# Set balls into a list so more can be dynamically added
	ballList = [ball]
	ballSprite = pygame.sprite.RenderClear(ballList)

	# Run Game
	stage = 91
	while running_game:
		clock.tick(60)
		counter += 1
		sprites.update()
		ballSprite.update()

		# Every 60 seconds add a ball whilst there are less balls than 10*players
		if apocalypse:
			if  stage > 1 and counter%90 == 0:
				stage -= 1
				print stage
			if counter%stage == 0:
				ballList.append(createBall(scoreList, playerList))
				ballSprite = pygame.sprite.RenderClear(ballList)
		else:
			if (counter%60 == 0 and len(ballList) < players*10):
				ballList.append(createBall(scoreList, playerList))
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

		# When all balls have been used end game loop.
		if totalScore == players*10 and not apocalypse:
			running_game = False

	# End game menu 
	menu = Menu()
	winner = getWinner(scoreList)
	menu.init(['PLAYER '+str(winner)+' WINS!', '  play again  ', '     quit     '], screen, True)
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
				  		win_menu = False
				   	elif menu.get_position() == 2:
				   		win_menu = False

if __name__ == "__main__":
	main()
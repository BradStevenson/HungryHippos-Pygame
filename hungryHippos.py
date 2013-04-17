#!/usr/bin/env python

import pygame
import random
import math
from pygame.sprite import Sprite

pygame.display.init()
pygame.font.init()
HEIGHT_RES = 768
WIDTH_RES = 768

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
		self.velocity = [side * 10 * math.cos(angle), 10 * math.sin(angle)]
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
					angle = random.uniform(0, math.pi/2)
					angle *= random.choice([-1,1])
					side = random.choice([-1,1])
					self.velocity = [side * 15 * math.cos(angle), 15 * math.sin(angle)]
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
			self.size = (20,210)
		else:
			self.size = (210, 20)

		self.image = pygame.Surface(self.size)
		self.image.set_colorkey(pygame.Color("black"))
		self.player = player
		self.score = 0
		self.rect = pygame.Rect(position, self.size)
		# self.rect.center = position
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

	# SET RESOLUTION
	screen = pygame.display.set_mode((WIDTH_RES, HEIGHT_RES))
	background = pygame.image.load('background.png')
	screen.blit(background,(0, 0))

	# INITIALIZE SPRITES
	score1 = Score("white", (20, (HEIGHT_RES/2)-270), 1)
	score2 = Score("white", ((WIDTH_RES-40, (HEIGHT_RES/2)+70)), 2)
	score3 = Score("white", ((WIDTH_RES/2)+70, 20), 3)
	score4 = Score("white", ((WIDTH_RES/2)-270, HEIGHT_RES-40), 4)
	player1 = Hippo((0, (HEIGHT_RES/2)-50), 1)
	player2 = Hippo((WIDTH_RES-100, (HEIGHT_RES/2)-50), 2)
	player3 = Hippo(((WIDTH_RES/2)-50, 0), 3)
	player4 = Hippo(((WIDTH_RES/2)-50, HEIGHT_RES-100), 4)
	ball1 = Ball("white", [score1, score2, score3, score4], [player1, player2, player3, player4])

	sprites = pygame.sprite.RenderClear([score1, score2, score3, score4, player1, player2, player3, player4])
	ballList = [ball1]
	ballSprite = pygame.sprite.RenderClear(ballList)

	# KEYMAP
	key_map = {
		pygame.K_q: [player1.forward, player1.back],
		pygame.K_p: [player2.forward, player2.back],
		pygame.K_m: [player3.forward, player3.back],
		pygame.K_z: [player4.forward, player4.back]
	}

	counter = 0
	clock = pygame.time.Clock()
	# GAME LOOP
	running = True
	while running:
		clock.tick(60)
		counter += 1
		sprites.update()
		ballSprite.update()
		if (counter%180 == 0 and len(ballList) < 28):
			ballList.append(Ball("white", [score1, score2], [player1, player2, player3, player4]))
			ballSprite = pygame.sprite.RenderClear(ballList)
		sprites.draw(screen)
		ballSprite.draw(screen)
		pygame.display.flip()
		sprites.clear(screen, background)
		ballSprite.clear(screen, background)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN and event.key in key_map:
				key_map[event.key][0]()
			elif event.type == pygame.KEYUP and event.key in key_map:
				key_map[event.key][1]()

if __name__ == "__main__":
	main()
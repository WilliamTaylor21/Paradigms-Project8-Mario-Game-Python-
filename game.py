import pygame
import time

from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, xPos, yPos, width, height, im):
		self.x = xPos
		self.y = yPos
		self.w = width
		self.h = height
		self.vert_velocity = 0;
		self.direction = True
		self.image = pygame.image.load(im)
		
class Mario(Sprite):
	def __init__(self, xPos, yPos):
		super(Mario, self).__init__(xPos, yPos, 60, 95, "mario1.png")
		
class Tube(Sprite):
	def __init__(self, xPos, yPos):
		super(Tube, self).__init__(xPos, yPos, 55, 400, "tube.png")
		
class Fireball(Sprite):
	def __init__(self, xPos, yPos):
		super(Fireball, self).__init__(xPos, yPos, 47, 47, "fireball.png")
		
class Goomba(Sprite):
	def __init__(self, xPos, yPos):
		super(Goomba, self).__init__(xPos, yPos, 90, 118, "goomba.png")
		
class Model():
	def __init__(self):
		self.dest_x = 0
		self.dest_y = 0
		self.jump = 0;
		self.jumpTimer = 30;
		self.sprites = []
		self.mario = Mario(0,0)
		self.sprites.append(self.mario)
		self.tube1 = Tube(600,420)
		self.sprites.append(self.tube1)
		self.tube2 = Tube(200,400)
		self.sprites.append(self.tube2)
		self.goomba = Goomba (400,500)
		self.sprites.append(self.goomba)
		self.offset = self.mario.x
		self.frame = 1
		self.onFire = False
		self.killCount = 0
		
	def update(self):
		for sprite in self.sprites:
			if isinstance(sprite, Mario):
				self.mario.px = self.mario.x
				self.i = 1
				if self.mario.y > 424:
					self.jumpTimer = 0
				if ((self.mario.y < 425) and (self.jump == 0)):
					self.mario.y += 15
				if ((self.jumpTimer < 20 ) and (self.jump == 1)):
					self.mario.y -= 15
				if self.mario.x < self.dest_x:
					self.mario.x += 5
				if self.mario.x > self.dest_x:
					self.mario.x -= 5
				if self.mario.px != self.mario.x:
					self.frame += 1
					if self.frame == 1:
						self.mario.image = pygame.image.load("mario1.png")
					if self.frame == 2:
						self.mario.image = pygame.image.load("mario2.png")
					if self.frame == 3:
						self.mario.image = pygame.image.load("mario3.png")
					if self.frame == 4:
						self.mario.image = pygame.image.load("mario4.png")
					if self.frame == 5:
						self.mario.image = pygame.image.load("mario5.png")
						self.frame = 1
			self.j = 1
			if isinstance(sprite, Goomba):
				if self.onFire == True:
					self.killCount += 1
					self.goomba.image = pygame.image.load("goomba_fire.png")
					if self.killCount == 100:
						self.sprites.pop()
						self.tube3 = Tube(200,400)
						self.sprites.append(self.tube2)
						self.killCount = 0
						self.onFire = False
					
				self.k = 1
				self.goomba.y = 425
				if (self.goomba.direction):
					self.goomba.x = self.goomba.x + 2;
				if (not self.goomba.direction):
					self.goomba.x = self.goomba.x - 2;
					self.k = 1
				for sprite in self.sprites:
					if isinstance(sprite, Tube):
						if((self.goomba.x+90 > self.sprites[self.k].x)and(self.goomba.x < self.sprites[self.k].x+55)):
							self.goomba.direction = not self.goomba.direction
						self.k += 1
					if isinstance(sprite, Fireball):
						if((self.fireball.x+45 > self.goomba.x)and(self.fireball.y+45>self.goomba.y)):
							self.sprites.pop()
							self.onFire = True
							
				self.j += 1 
			if isinstance(sprite, Fireball):
				if self.fireball.x > 800:
					self.sprites.pop()
				self.fireball.x += 6;
				self.fireball.vert_velocity += .8;
				self.fireball.y += self.fireball.vert_velocity;
				if(self.fireball.y >= 500):
					self.fireball.y = 500;
					self.fireball.vert_velocity = -self.fireball.vert_velocity;
				
		self.i = 1
		for sprite in self.sprites:
			if isinstance(sprite, Tube):
				if((self.mario.x+60 > self.sprites[self.i].x)and(self.mario.y+95 > self.sprites[self.i].y)and(self.mario.x+50 < self.sprites[self.i].x)):
					self.mario.x = self.mario.x - 10
					self.dest_x = self.mario.x
				if((self.mario.x < self.sprites[self.i].x+55)and(self.mario.y+95 > self.sprites[self.i].y)and(self.mario.x > self.sprites[self.i].x+45)):
					self.mario.x = self.mario.x + 10
					self.dest_x = self.mario.x
				if((self.mario.y+95>self.sprites[self.i].y)and(self.mario.x+60>self.sprites[self.i].x)and(self.mario.x<self.sprites[self.i].x+55)):
					self.mario.y = self.sprites[self.i].y-95
					self.jumpTimer = 0;
				self.i += 1
	def set_dest(self, pos):
		self.dest_x = pos[0]
		self.dest_y = pos[1]
		
	def fireballFunction(self):
		if len(self.sprites) < 5:
			self.fireball = Fireball(self.mario.x + 55,self.mario.y + 20)
			self.sprites.append(self.fireball)
		print(self.fireball.x)

class View():
	def __init__(self, model):
		screen_size = (800,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model

	def update(self):
		self.screen.fill([0,200,100])
		for sprite in self.model.sprites:
			self.screen.blit(sprite.image, (sprite.x, sprite.y))
		pygame.display.update()

class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False

		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.dest_x -= 5
		if keys[K_RIGHT]:
			self.model.dest_x += 5
		if keys[K_UP]:
			self.model.jump = 1
			self.model.jumpTimer += 1
		if self.model.jumpTimer > 20:
			self.model.jump = 0
		if keys[K_UP] == False:
			self.model.jump = 0
			self.model.jumpTimer = 20
		if keys[K_LCTRL]:
			self.model.fireballFunction()
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")
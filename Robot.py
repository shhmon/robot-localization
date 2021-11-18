import numpy as np
import pygame
from Dir import Dir

class RobotSim:

	# x, y = 3, 6
	
	def __init__(self, start, head):
		self.pos = start
		self.head = head
	
	def move(self):
		pass
		#probs = self.tm.getT()[self.state]
		#choices = range(len(probs))
		#self.state = np.random.choice(choices, p=probs)
		#return self.state
	
	def sense(self, maze):
		if self.head in maze.shape[self.pos[1]][self.pos[0]]:
			return 1
		else:
			return 0
	
	def step(self):
		if self.head == Dir.N:
			self.pos = self.pos[0], self.pos[1] - 1
		elif self.head == Dir.E:
			self.pos = self.pos[0] + 1, self.pos[1]
		elif self.head == Dir.S:
			self.pos = self.pos[0], self.pos[1] + 1
		elif self.head == Dir.W:
			self.pos = self.pos[0] - 1, self.pos[1]
	
	def update(self, maze):
		dirs = maze.shape[self.pos[1]][self.pos[0]]

		if self.head in dirs:
			self.step()
		else:
			self.head = Dir.Next(self.head, dirs)
		
		return self.pos[0], self.pos[1], self.head
	
	def draw(self, surface, wallLength):
		tomid = lambda x: x * wallLength + wallLength / 2
		bpos = (tomid(self.pos[0]), tomid(self.pos[1]))
		pygame.draw.circle(surface, (0, 255, 0), bpos, 10)

		modifier = wallLength / 8

		if self.head == Dir.N:
			hpos = (bpos[0], bpos[1] - modifier)
		elif self.head == Dir.E:
			hpos = (bpos[0] + modifier, bpos[1])
		elif self.head == Dir.S:
			hpos = (bpos[0], bpos[1] + modifier)
		elif self.head == Dir.W:
			hpos = (bpos[0] - modifier, bpos[1])

		pygame.draw.circle(surface, (255, 0, 0), hpos, 2)

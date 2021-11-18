import numpy as np
import pygame
from Dir import Dir
from Utils import forward

class RobotSim:

	# x, y = 3, 6
	
	def __init__(self, start, head):
		self.pos = start
		self.head = head
	
	def sense(self, maze):
		dirs = maze.shape[self.pos[1]][self.pos[0]]

		# Wall sensor
		if self.head in dirs:
			return 1
		else:
			return 0

		# Line sensors
		# fPath = self.head in dirs
		# lPath = Dir.Left(self.head) in dirs
		# rPath = Dir.Right(self.head) in dirs

		# if fPath and lPath and rPath:
		# 	return 0
		# elif fPath and lPath:
		# 	return 1
		# elif fPath and rPath:
		# 	return 2
		# elif lPath and rPath:
		# 	return 3
		# elif rPath:
		# 	return 4
		# elif fPath:
		# 	return 5
		# elif lPath:
		# 	return 6
		# else:
		# 	return 7
	
	def step(self):
		self.pos = forward(self.pos[0], self.pos[1], self.head.value)
	
	def update(self, maze):
		dirs = maze.shape[self.pos[1]][self.pos[0]]

		if (self.pos[0] == 2 and self.pos[1] == 3):
			dirs = [*dirs, Dir.S]
		elif (self.pos[0] == 2 and self.pos[1] == 4):
			dirs = [*dirs, Dir.N]

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

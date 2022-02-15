import numpy as np
import pygame

class HMMFilter:
	def __init__(self, tm, om):
		self.tm, self.om = tm, om
		self.states = tm.getNrOfStates()
		self.sense = None
	
	def initialize(self, state):
		self.f = np.zeros(self.states)
		self.f[state] = 1
		self.f = self.f.T
	
	def draw(self, surface, stateModel, sense, wallLength):
		vector = self.om.getOr(sense)
		print("SENSE + VECTOR", sense, vector)
		x, y, h = stateModel.robotStateToXYH(np.argmax(vector))
		rect = pygame.Rect(x * wallLength, y * wallLength, wallLength, wallLength)
		pygame.draw.rect(surface, (0,0,0), rect)
	
	def update(self, sense):
		vector = self.om.getOr(sense)
		o  = np.diag(vector)
		tt = self.tm.getT_transp()
		ott = np.dot(o, tt)
		# print(f'O state: {ott[np.argmax(vector)]}')
		f = np.dot(ott, self.f)
		f = f / np.linalg.norm(f)
		self.f = f.T
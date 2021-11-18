import numpy as np

class HMMFilter:
	def __init__(self, tm, om):
		self.tm, self.om = tm, om
		self.states = tm.getNrOfStates()
	
	def initialize(self, state):
		self.f = np.zeros(self.states).T
		self.f[state] = 1
	
	def update(self, sense):
		o  = np.diag(self.om.getOr(sense))
		tt = self.tm.getT_transp()
		f = np.dot(np.dot(o, tt), self.f)
		f = f / np.linalg.norm(f)
		self.f = f.T
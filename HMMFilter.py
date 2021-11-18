import numpy as np

class HMMFilter:
	def __init__(self, tm, om):
		self.tm, self.om = tm, om
		self.states = tm.getNrOfStates()
	
	def initialize(self, state):
		self.f = np.zeros(self.states)
		self.f[state] = 1
		self.f = self.f.T
	
	def update(self, sense):
		vector = self.om.getOr(sense)
		o  = np.diag(vector)
		tt = self.tm.getT_transp()
		ott = np.dot(o, tt)
		f = np.dot(ott, self.f)
		f = f / np.linalg.norm(f)
		self.f = f.T
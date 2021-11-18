from enum import Enum, auto

class Dir(Enum):
	N = 0
	W = 1
	S = 2
	E = 3
	R = -1

	@staticmethod
	def Next(head, alts):
		valid = lambda d: d in alts

		if head == Dir.N:
			seq = [Dir.W, Dir.E, Dir.S]
		elif head == Dir.W:
			seq = [Dir.S, Dir.N, Dir.E]
		elif head == Dir.S:
			seq = [Dir.E, Dir.W, Dir.N]
		elif head == Dir.E:
			seq = [Dir.N, Dir.S, Dir.W]

		try:		
			return next(d for d in seq if valid(d))
		except:
			return Dir.R

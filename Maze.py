import pygame
from Dir import Dir

class Maze:

	shape = [
		[[Dir.E, Dir.S], [Dir.W, Dir.S], [Dir.S], [Dir.E, Dir.S], [Dir.W], [Dir.E], [Dir.W, Dir.S]],
		[[Dir.N, Dir.S], [Dir.E, Dir.N], [Dir.N, Dir.W, Dir.S], [Dir.N, Dir.S], [Dir.E, Dir.S], [Dir.E, Dir.W], [Dir.W, Dir.N]],
		[[Dir.N, Dir.S], [Dir.E, Dir.S], [Dir.N, Dir.W, Dir.S], [Dir.N, Dir.E], [Dir.N, Dir.W, Dir.S], [Dir.E, Dir.S], [Dir.W]],
		[[Dir.N, Dir.S], [Dir.N, Dir.S], [Dir.N, Dir.E], [Dir.W, Dir.E], [Dir.W, Dir.E, Dir.N], [Dir.N, Dir.W, Dir.E], [Dir.W, Dir.S]],
		[[Dir.N, Dir.S], [Dir.N, Dir.S], [Dir.E], [Dir.E, Dir.W, Dir.S], [Dir.E, Dir.W], [Dir.E, Dir.W, Dir.S],  [Dir.N, Dir.W, Dir.S]],
		[[Dir.N, Dir.E], [Dir.N, Dir.S, Dir.E, Dir.W], [Dir.W, Dir.S, Dir.E], [Dir.N, Dir.W], [Dir.E, Dir.S], [Dir.N, Dir.W], [Dir.N, Dir.S]],
		[[Dir.E], [Dir.N, Dir.W], [Dir.N, Dir.E], [Dir.W], [Dir.N, Dir.E], [Dir.E, Dir.W], [Dir.N, Dir.W]]
	]

	def __init__(self, wallLength, lineWidth, wallColor, lineColor):
		self.wallLength = wallLength
		self.lineWidth = lineWidth
		self.wallColor = wallColor
		self.lineColor = lineColor
	
	def draw(self, surface):
		pygame.font.init()
		#myfont = pygame.font.SysFont('Comic Sans MS', 20)

		for y, row in enumerate(self.shape):
			for x, col in enumerate(row):
				walls = [dir for dir in Dir.Values() if dir not in col]

				#textsurface = myfont.render(f'x:{x} y:{y}', False, (0, 0, 0))
				#surface.blit(textsurface, (x * self.wallLength + self.wallLength / 4, y * self.wallLength + self.wallLength / 4))

				# Borders
				for wall in walls:
					if wall == Dir.N:
						start = (x * self.wallLength, y * self.wallLength)
						end = (x * self.wallLength + self.wallLength, y * self.wallLength)
					elif wall == Dir.E:
						start = (x * self.wallLength + self.wallLength, y * self.wallLength)
						end = (x * self.wallLength + self.wallLength, y * self.wallLength + self.wallLength)
					elif wall == Dir.S:
						start = (x * self.wallLength, y * self.wallLength + self.wallLength)
						end = (x * self.wallLength + self.wallLength, y * self.wallLength + self.wallLength)
					elif wall == Dir.W:
						start = (x * self.wallLength, y * self.wallLength)
						end = (x * self.wallLength, y * self.wallLength + self.wallLength)
					
					pygame.draw.line(surface, self.wallColor, start, end, self.lineWidth)

				# Follow line
				for door in col:
					start = (x * self.wallLength + self.wallLength/2, y * self.wallLength + self.wallLength/2)

					if door == Dir.N:
						end = (x * self.wallLength + self.wallLength/2, y * self.wallLength)
					elif door == Dir.E:
						end = (x * self.wallLength + self.wallLength, y * self.wallLength + self.wallLength/2)
					elif door == Dir.S:
						end = (x * self.wallLength + self.wallLength/2, y * self.wallLength + self.wallLength)
					elif door == Dir.W:
						end = (x * self.wallLength, y * self.wallLength + self.wallLength/2)

					pygame.draw.line(surface, self.lineColor, start, end, self.lineWidth//2)
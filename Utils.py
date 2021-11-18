from Dir import Dir

def forward(x, y, h):
	if h == Dir.N.value:
		nx, ny = x, y-1
	elif h == Dir.W.value:
		nx, ny = x-1, y
	elif h == Dir.S.value:
		nx, ny = x, y+1
	elif h == Dir.E.value:
		nx, ny = x+1, y

	return nx, ny

def inside(x, y, rows, cols):
	return x >= 0 and x < cols and y >= 0 and y < rows
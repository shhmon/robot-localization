# The state model describes the dimensions of the grid and provides methods to transfrom a pose (x, y, h)
# or a position (x, y) into a state i or a sensor reading state r and/or vice versa.

class StateModel:
    
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.head = 4
        
    def robotStateToXYH(self, s):
        x = s // (self.cols * self.head)
        y = (s - x * self.cols * self.head ) // self.head
        h = s % self.head
        
        return x, y, h;
    
    def xyhToRobotState(self, x, y, h):
        return x * self.cols * self.head + y * self.head + h

    def robotStateToXY(self, s):
        x = s // (self.cols * self.head)
        y = (s - x * self.cols * self.head ) // self.head

        return x, y
    
    def getDimensions(self):
        return self.rows, self.cols, self.head
    
    
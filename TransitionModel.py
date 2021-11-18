import numpy as np
import matplotlib.pyplot as plt
from Maze import Maze
from Dir import Dir

# The transition model contains the transition matrix and some methods for convenience, 
# including transposition

class TransitionModel:

    def __init__(self, stateModel):
        self.stateModel = stateModel
        self.rows, self.cols, self.head = self.stateModel.getDimensions()

        # Number possible states
        self.dim = self.rows * self.cols * self.head

        # Transition matrix (entry ij = probability of going from state i to j)
        self.matrix = np.zeros(shape=(self.dim, self.dim), dtype=float)

        vis = np.empty(shape=(self.dim, self.dim), dtype=object)
        np.set_printoptions(threshold=np.inf)

        for i in range(self.dim):
            x, y, h = self.stateModel.robotStateToXYH(i)

            dirs = list(map(lambda d: d.value, Maze.shape[y][x]))
            next = Dir.Next(Dir(h), Maze.shape[y][x]).value

            # Current heading available
            if h in dirs:
                if h == Dir.N.value:
                    nx, ny, nh = x, y-1, h
                elif h == Dir.W.value:
                    nx, ny, nh = x-1, y, h
                elif h == Dir.S.value:
                    nx, ny, nh = x, y+1, h
                elif h == Dir.E.value:
                    nx, ny, nh = x+1, y, h

                j = self.stateModel.xyhToRobotState(nx, ny, nh)
                self.matrix[i, j] = 1
            else:
                print(next)
                j = self.stateModel.xyhToRobotState(x, y, next)
                self.matrix[i, j] = 1
                
                
    # retrieve the number of states represented in the matrix                        
    def getNrOfStates(self):
        return self.dim

    # get the probability to go from state i to j
    def getTij(self, i, j): 
        return self.matrix[i,j]

    # get the probability to go from pose (x, y, h) to (X, Y, H)
    def getTxyhToXYH(self, x, y, h, X, Y, H):
        return self.matrix[self.stateModel.xyhToRobotState(x, y, h), self.stateModel.xyhToRobotState(X, Y, H)]

    # get the entire matrix
    def getT(self): 
        return self.matrix.copy()
    
    # get the transposed transition matrix
    def getT_transp(self):
        transp = np.transpose(self.matrix)
        return transp
    
    # plot matrix as a heat map
    def plotTMatrix(self):
        plt.matshow(self.matrix)
        plt.colorbar()
        plt.show()
        
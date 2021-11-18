import numpy as np
import matplotlib.pyplot as plt
from Maze import Maze
from Dir import Dir
from Utils import forward, inside

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

        for i in range(self.dim):
            x, y, h = self.stateModel.robotStateToXYH(i)

            # More relaxed transitions
            # for j in range(self.dim):
            #     nx, ny, nh = self.stateModel.robotStateToXYH(j)

            #     if (nx, ny) == (x, y) and nh != h:
            #         if nh == Dir.Left(Dir(h)).value:
            #             self.matrix[i, j] = 2
            #         else:
            #             self.matrix[i, j] = 1
            #     elif abs(x-nx) + abs(y-ny) == 1:
            #         if (nx, ny) == forward(x, y, h):
            #             self.matrix[i, j] = 2
            #         else:
            #             self.matrix[i, j] = 0.5
            
            # if sum(self.matrix[i]) > 0:
            #     self.matrix[i] /= sum(self.matrix[i])
            

            dirs = list(map(lambda d: d.value, Maze.shape[y][x]))
            next = Dir.Next(Dir(h), Maze.shape[y][x])

            nx, ny = forward(x, y, h)
            j = self.stateModel.xyhToRobotState(nx, ny, h)

            # Current heading available
            if h in dirs:
                self.matrix[i, j] = 1
            # Wall in front
            else:
                if inside(nx, ny, self.rows, self.cols):
                    self.matrix[i, j] = 0.05

                cur = Dir.Next(Dir(h), Dir.Values())
                cnt = 0

                while cur != next:
                    j = self.stateModel.xyhToRobotState(x, y, cur.value)
                    fx, fy = forward(x, y, cur.value)

                    if inside(fx, fy, self.rows, self.cols):
                        self.matrix[i, j] = 0.2 - cnt*0.1
                        cnt += 1

                    cur = Dir.Left(cur)
                
                j = self.stateModel.xyhToRobotState(x, y, next.value)
                self.matrix[i, j] = 1 - cnt*0.2 - (cnt-1)*0.1 - 0.05
                
                
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
        
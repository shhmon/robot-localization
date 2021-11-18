import numpy as np
import matplotlib.pyplot as plt
from Maze import Maze
from Dir import Dir

# The observation model contains the diagonals (stored as vectors) of the observation 
# matrices for each possible sensor reading
# The last of these vectors contains the probabilities for the sensor to produce nothing

class ObservationModel:
    def __init__(self, stateModel) :
        self.stateModel = stateModel
        self.rows, self.cols, self.head = stateModel.getDimensions()

        self.dim = self.rows * self.cols * self.head
        # Wall, noWall, nothing
        self.numOfReadings = 2 # + 1

        self.vectors = np.ones(shape=(self.numOfReadings, self.dim))
        
        for o in range(self.numOfReadings-1):
            for rs in range(self.dim):
                x, y, h = self.stateModel.robotStateToXYH(rs)
                dirs = list(map(lambda d: d.value, Maze.shape[y][x]))

                # Enum, not sure if this is ok
                # If current heading blocked by wall
                if h not in dirs:
                    self.vectors[o, rs] = 0.8
                else:
                    self.vectors[o, rs] = 0.2

                # Add nothing
                # self.vectors[self.numOfReadings-1, rs] = 0.1

    # get the number of possible sensor readings
    def getNrOfReadings( self) :
        return self.numOfReadings

    # get the probability for the sensor to have produced reading "reading" when in state i
    def getOri(self, reading, i) :
        return self.vectors[reading,i]

    # get the entire vector with probabilies to have produced reading "reading"
    # use None for "no reading"
    def getOr(self, reading) :
        if(reading == None): reading = self.numOfReadings-1
        return self.vectors[reading,:]

    # get the probability to have produced reading <rX, rY> when in position <x, y>
    # send in rX or rY as None to get teh values for "no reading"
    def getOrXY(self, rX, rY, x, y) :
        if rX == None or rY == None:
            return self.vectors[self.numOfReadings-1, x * self.cols * self.head + y * self.head]
        return self.vectors[rX * self.cols + rY, x * self.cols * self.head + y * self.head]

    # plot the vectors as heat map(s)
    def plotODiags(self):
        plt.matshow(self.vectors)
        plt.colorbar()
        plt.show()
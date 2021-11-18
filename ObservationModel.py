import numpy as np
import matplotlib.pyplot as plt
from Maze import Maze
from Dir import Dir

# The observation model contains the diagonals (stored as vectors) of the observation 
# matrices for each possible sensor reading
# The last of these vectors contains the probabilities for the sensor to produce nothing

class ObservationModel:
    def __init__(self, stateModel):
        self.stateModel = stateModel
        self.rows, self.cols, self.head = stateModel.getDimensions()

        self.dim = self.rows * self.cols * self.head

        # Three light sensors, Left Front Right
        # 0 = LLL, 1 = LLN, 2 = NLL, 2 = LNL
        # 4 = NNL, 5 = NLN, 6 = LNN, 7 = NNN
        #self.numOfReadings = 2**3

        self.numOfReadings = 2

        self.vectors = np.zeros(shape=(self.numOfReadings, self.dim))

        # Wall sensor
        for rs in range(self.dim):
            x, y, h = self.stateModel.robotStateToXYH(rs)
            dirs = list(map(lambda d: d.value, Maze.shape[y][x]))

            if h not in dirs:
                self.vectors[0, rs] = 1
            else:
                self.vectors[1, rs] = 1

        # Line sensors
        # for rs in range(self.dim):
        #     x, y, h = self.stateModel.robotStateToXYH(rs)

        #     dirs = Maze.shape[y][x]
        #     head = Dir(h)
            
        #     fPath = head in dirs
        #     lPath = Dir.Left(head) in dirs
        #     rPath = Dir.Right(head) in dirs

        #     if fPath and lPath and rPath:
        #         self.vectors[0, rs] = 1
        #     elif fPath and lPath:
        #         self.vectors[1, rs] = 1
        #     elif fPath and rPath:
        #         self.vectors[2, rs] = 1
        #     elif lPath and rPath:
        #         self.vectors[3, rs] = 1
        #     elif rPath:
        #         self.vectors[4, rs] = 1
        #     elif fPath:
        #         self.vectors[5, rs] = 1
        #     elif lPath:
        #         self.vectors[6, rs] = 1
        #     else:
        #         self.vectors[7, rs] = 1
                
        
        for o in range(self.numOfReadings):
            self.vectors[o] /= sum(self.vectors[o])

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
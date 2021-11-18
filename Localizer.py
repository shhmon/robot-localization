import numpy as np
from HMMFilter import HMMFilter
from TransitionModel import TransitionModel
from ObservationModel import ObservationModel

# The Localizer binds the models together and controls the update cycle in its "update" method.

class Localizer:
    def __init__(self, stateModel, state) :
        self.stateModel = stateModel
        self.rows, self.cols, self.head = stateModel.getDimensions()
        
        self.tm = TransitionModel(self.stateModel)
        self.om = ObservationModel(self.stateModel)
        self.hmm = HMMFilter(self.tm, self.om)
         
        # change in initialise in case you want to start out with something else...
        self.initialise(state)
        
    # for convenience, one can also ask the StateModel
    def getNumRows(self):
        return self.rows

    # for convenience, one can also ask the StateModel
    def getNumCols(self):
        return self.cols
    
    # for convenience, one can also ask the StateModel
    def getNumHead(self):
        return self.head

    # retrieve the transition model that we are currently working with
    def getTransitionModel(self):
        return self.tm

    # retrieve the observation model that we are currently working with
    def getObservationModel(self): 
        return self.om

    # the current true pose (x, h, h) that should be kept in the local variable trueState
    def getCurrentTruePose(self): 
        x, y, h = self.stateModel.robotStateToXYH( self.trueState)
        return x, y, h

    # the current probability distribution over all states
    def getCurrentProbDist(self): 
        return self.probs

    # the current sensor reading. "Nothing" is expressed as None
    def getCurrentReading(self): 
        ret = None
        
        if self.sense != None : 
            ret = self.stateModel.sensorStateToXY(self.sense)
    
        return ret
    
    # get the currently most likely position, based on single most probable pose     
    def getEstimatedPosition(self):
        index = np.argmax(self.probs)
        return self.stateModel.robotStateToXY(index)
    
    def getEvaluationMeasures(self):
        return self.__totalError, self.__correctEstimates

    # (re-)initialise for a new run without change of size
    def initialise(self, state):
        self.trueState = state
        self.sense = None
        self.hmm.initialize(state)
        self.probs = self.hmm.f
        
        # simple evaluation measures that go into the visualisation
        self.__totalError = 0.0
        self.__correctEstimates = 0
        self.__meanManDist = 0
        self.__updateCount = 0

    def update(self, trueState, sense):
        print('prev:', self.stateModel.robotStateToXYH(self.trueState))
        self.sense = sense
        self.trueState = trueState

        self.hmm.update(self.sense)
        probs = self.probs = self.hmm.f
        
        self.__updateCount += 1
        
        tsX, tsY = self.stateModel.robotStateToXY(self.trueState)
        pX, pY = self.getEstimatedPosition()
        
        manDist = abs(tsX - pX) + abs(tsY - pY)      
        self.__meanManDist += (manDist - self.__meanManDist) / self.__updateCount
        
        if not manDist:
            self.__correctEstimates += 1
        
        print(f'<Mean Distance (Manhattan)>: {self.__meanManDist}')
        print(f'<Accuracy>: {self.__correctEstimates / self.__updateCount}')

        return pX, pY
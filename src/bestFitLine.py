import numpy as np
from scipy.optimize import leastsq, least_squares

class bestFitLines():

    def __init__(self, data):
        self.data = data
    
    def linearLOBF(self):
        xMean = self.calculateMean(0)
        yMean = self.calculateMean(1)

        numeratorSum = 0.0
        denominatorSum = 0.0
        for row in self.data:
            numeratorSum += (row[0]-xMean)*(row[1]-yMean)
            denominatorSum += (row[0]-xMean)**2
        slope = numeratorSum/denominatorSum
        yIntercept = yMean-(slope*xMean)
        modifiers = [slope, yIntercept]

        equation = lambda modifiers, t: modifiers[0]*t+modifiers[1] 
        rSquared = self.rSquared(self.data, equation, modifiers)
        return modifiers, rSquared

    def sinusodialLOBF(self, columnNumber, data = None):
        if data is None:
            data = self.data
        column = data[:,columnNumber]
        t = np.linspace(0, 20, data.shape[0])
        sinEquation = lambda modifiers, points: modifiers[0]*np.sin(modifiers[1]*points + modifiers[2])+modifiers[3]
        guess = [(np.max(column)+np.min(column))/2, 1, 1, (np.max(column)-np.min(column))/2]
        #print(np.max(column))
        modifiers = self.LOBF(columnNumber, sinEquation, guess, t)[0]
        rSquared = self.rSquared(column, sinEquation, modifiers)
        return modifiers, rSquared


    def risingSinusodialLOBF(self, columnNumber):
        column = self.data[:,columnNumber]
        t = np.linspace(0, 20, self.data.shape[0])
        equation = lambda modifiers, points: modifiers[0]*np.sin(modifiers[1]*points + modifiers[2])+modifiers[3]+modifiers[4]*points
        guess = [(np.max(column)+np.min(column))/2, 1, 1, (np.max(column)-np.min(column))/2, (self.data[0][0]-self.data[-1][0])/(self.data[0][1]-self.data[-1][1])]
        modifiers = self.LOBF(columnNumber, equation, guess, t)[0]
        rSquared = self.rSquared(column, equation, modifiers)
        print(modifiers)
        return modifiers, rSquared

    def customLOBF(self, columnNumber, equation, guess):
        
        maxInDataSet = np.max(self.data[:,0])
        t = np.linspace(0, maxInDataSet, self.data.shape[0])
        modifiers = self.LOBF(columnNumber, equation, guess, t)[0]
        rSquared = self.rSquared(self.data[:,columnNumber], equation, modifiers)
        return modifiers, rSquared
        
    def LOBF(self, columnNumber, equation, guess, equationPoints):
        
        delta = lambda modifiers: equation(modifiers, equationPoints) - self.data[:,columnNumber]
        return leastsq(delta, guess)

    def calculateMean(self, columnNumber, data=None):
        if data is None:
            data = self.data
        sum = 0.0
        #print(data)

        for row in data:
            #print(row)
            try:
                sum += row[columnNumber]
            except:
                sum += row
        return sum/(self.data.shape[0])

    def rSquared(self, data, equation, modifiers):

        t = np.linspace(0, np.max(self.data[:,0]), data.shape[0])
        equData = equation(modifiers, t)
        average = self.calculateMean(0,data)
        SSR = 0
        SSTO = 0
        for index in range(data.shape[0]):
            SSR += (equData[index]-average)**2
            SSTO += (data[index]-average)**2
        return SSR/SSTO        
    
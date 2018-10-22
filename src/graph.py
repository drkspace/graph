import sys
import matplotlib.pyplot as plot
import csv
import numpy as np
from math import sqrt
from bestFitLine import bestFitLines

class graph():

    #Data for the graph
    data = []

    #Title of the graph
    title = ""

    #Label for the x axis
    xAxisName = ""

    #Label for the y axis
    yAxisName = ""

    def __init__(self, file=None, data=[], title = "", xAxisName = "", yAxisName = ""):
        if type(data) is not type(np.array([])):
            self.data = data
        if file is not None and data is not []:
            self.importData(file)
        self.title = title
        self.xAxisName = xAxisName
        self.yAxisName = yAxisName

    def importData(self, file):
        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                rowData = []
                for elemnt in row:
                    rowData.append(float(elemnt))
                self.data.append(rowData)
        self.data = np.array(self.data)

    """
    All of the variables do nothing yet
    """
    def graph(self, xMin = 0, xMax = 0, yMin = 0, yMax = 0, addBestFit = False):
        
        plot.suptitle(self.title)
        plot.plot(self.data[:,0],self.data[:,1])
        plot.xlabel(self.xAxisName)
        plot.ylabel(self.yAxisName)
        

    def calculateStdDev(self, columnNumber=0):
        mean = self.calculateMean(columnNumber)
        sum = 0.0
        for row in self.data:
            sum += (row[columnNumber]-mean)**2
        result = sqrt(sum/self.data.shape[0])
        return result

    def calculateMean(self, columnNumber):
        sum = 0.0
        for row in self.data:
            sum += row[columnNumber]
        return sum/(self.data.shape[0])

    def removeOutliers(self, columnNumber=0, sigmaToRemove = 5):
        sigma = self.calculateStdDev(columnNumber=columnNumber)
        mean = self.calculateMean(columnNumber)
        range = sigmaToRemove*sigma
        goodData = []
        lowData = []
        highData = []
        
        for row in self.data:
            if row[columnNumber] >= mean+range:
                highData.append(row[columnNumber])
            elif row[columnNumber] <= mean-range:
                lowData.append(row[columnNumber])
            else:
                goodData.append(row[columnNumber])
        print("Values below {} Standard Deviations:\n{}".format(sigmaToRemove, lowData))
        print("Values above {} Standard Deviations:\n{}".format(sigmaToRemove, highData))

        return np.array(goodData)

    """
    Type codes:
        l = linear best fit
        s = sinusoidal best fit
        sr = rising sinusoidal best fit
        p[number] = polynomial with degree number (i.e. p2 tries a polynomial with degree 2) (NOT IMPLEMENTED YET)
        c = custom best fit equation (guess is a list of a guess of what the constants and coefficients are, but it doesn't really matter what you put)
        None = try all and see which one has the best r^2 value (NOT IMPLEMENTED YET)
    """
    def lineOfBestFit(self, type, equation=None, guess = None):

        xColumnNumber = 1
        x = np.linspace(0, np.max(self.data[:,0]), 1000)
        bestFit = bestFitLines(self.data)
        equationInfo = []
        if type is "l":
            equationInfo = bestFit.linearLOBF()
            lineModifiers = equationInfo[0]
            plot.plot(x, lineModifiers[0]*x+lineModifiers[1])
        elif type is "s":
            equationInfo = bestFit.SinusodialLOBF(xColumnNumber)
            lineModifiers = equationInfo[0]
            plot.plot(x, lineModifiers[0]*np.sin(lineModifiers[1]*x+lineModifiers[2])+lineModifiers[3])
        elif type is "sr":
            equationInfo = bestFit.risingSinusodialLOBF(xColumnNumber)
            lineModifiers = equationInfo[0]
            plot.plot(x, lineModifiers[0]*np.sin(lineModifiers[1]*x+lineModifiers[2])+lineModifiers[3]+lineModifiers[4]*x)
        elif type[0] is "p":
            pass
        elif type is "c":
            if equation is None or guess is None:
                print("Please make sure that you have given an equation and a guess")
            else:
                #print(guess
                equationInfo = bestFit.customLOBF(xColumnNumber, equation, guess)
                lineModifiers = equationInfo[0]
                
                plot.plot(x, equation(lineModifiers, x), label="LOBF")
        elif type is None:
            pass
        else:
            pass
        
        return equationInfo

    def setXAxisName(self, xAxisName):
        self.xAxisName = xAxisName

    def setYAxisName(self, yAxisName):
        self.yAxisName = yAxisName

a = graph(file="testData.csv")
a.graph()
equation = lambda modifiers, x: modifiers[0]*x**2 + modifiers[1]*x + modifiers[2]

print(a.lineOfBestFit(("c"),  equation, [10,23,125]))
plot.show()

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
        x = np.linspace(0, np.max(self.data[:,0]), 100)
        plot.suptitle(self.title)
        plot.plot(self.data[:,0],self.data[:,1])
        plot.xlabel(self.xAxisName)
        plot.ylabel(self.yAxisName)
       

        #plot.legend()
        plot.show()

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
        s = sinusodal best fit
        sr = rising sinusodal best fit
        p[number] = polynomial with degree number (i.e. p2 tries a polynomial with degree 2)
        None = try all and see which one has the best r^2 value
    """
    def lineOfBestFit(self, type):

        x = np.linspace(0, np.max(self.data[:,0]), 1000)
        bestFit = bestFitLines(self.data)
        rSquared = -1
        equationInfo = []
        if type is "l":
            equationInfo = bestFit.linearLOBF()
            lineModifiers = equationInfo[0]
            plot.plot(x, lineModifiers[0]*x+lineModifiers[1])
        elif type is "s":
        elif type is "sr":
            equationInfo = bestFit.risingSinusodialLOBF(1)
            rSquared = equationInfo[1]
            lineModifiers = equationInfo[0]

            plot.plot(x, lineModifiers[0]*np.sin(lineModifiers[1]*x+lineModifiers[2])+lineModifiers[3]+lineModifiers[4]*x)
        elif type[0] is "p":
        elif type is None:
        else:

        

    def setXAxisName(self, xAxisName):
        self.xAxisName = xAxisName

    def setYAxisName(self, yAxisName):
        self.yAxisName = yAxisName

a = graph(file="testData.csv")
a.graph()
import matplotlib.pyplot as plt


class data:
    def __init__(self,dataName):
        self.name = dataName
        self.values = []

    def addDataPoint(self,dataPoint):
        #try:
        self.values.append(float(dataPoint))
        #except:
        #    print "Unable to convert data point to float skipping: ",dataPoint

    def getName(self):
        return self.name

    def getData(self):
        return self.values

class dataSet:
    def __init__(self):
        self.dataList = []

    def getDataList(self):
        return self.dataList

    #Method to get data object for certain value name
    def findData(self,dataName):
        for dat in self.dataList:
            if dataName == dat.getName():
                return dat

        print "Unable to find data Item: ",dataName
        return 0
            

    def parseFile(self,filename):
        inFile = open(filename)
        firstLine = True
        for line in inFile:
            dataVals = (line.strip()).split(",")
            
            if firstLine:
                for element in dataVals:
                    self.dataList.append(data(element))
                    
                firstLine = False

            else:
                for i in range(len(dataVals)):
                    self.dataList[i].addDataPoint(dataVals[i])



#Method to to a simple x vs y plot with optional error bars
def simplePlot(fileData,xName,yName,xError=0,yError=0):
    xDat =  fileData.findData(xName)
    yDat =  fileData.findData(yName)
    xErr = 0
    yErr = 0
    if xError != 0 and yError == 0:
        xErr = fileData.findData(xError)
        plt.errorbar(xDat.getData(),yDat.getData(),xerr=xErr.getData())
	plt.ylim(0,1)
	plt.gca().set_marker('o')
        plt.ylabel(yName)
        plt.xlabel(xName)
        plt.title("Plot of "+yName+" vs. "+xName+" with errors given by "+xError)
        plt.show()
        
    elif xError == 0 and yError != 0:
        yErr = fileData.findData(yError)
        plt.errorbar(xDat.getData(),yDat.getData(),yerr=yErr.getData())
        plt.ylabel(yName)
        plt.xlabel(xName)
        plt.title("Plot of "+yName+" vs. "+xName+" with errors given by "+yError)
        plt.show()

    elif xError != 0 and yError != 0:
        xErr = fileData.findData(xError)
        yErr = fileData.findData(yError)
        plt.errorbar(xDat.getData(),yDat.getData(),yerr=yErr.getData(),xerr=xErr.getData())
	plt.gca().set_marker('o')
        plt.ylabel(yName)
        plt.xlabel(xName)
        plt.title("Plot of "+yName+" vs. "+xName+" with errors given by y: "+yError+" and x: "+xError)
        plt.show()

    elif xError == 0 and yError == 0:
        plt.plot(xDat.getData(),yDat.getData(),'ro')
	plt.ylim(0,1)
        plt.ylabel(yName)
        plt.xlabel(xName)
        plt.title("Plot of "+yName+" vs. "+xName)
        plt.show()

#Method to plot 2 yValues against a Single x value with optional error bars
def doublePlot(xData,y1Data,y2Data,x1Error=0,x2Error=0,y1Error=0,y2Error=0):
    pass

if __name__ == "__main__":
    fileData = dataSet()
    fileData.parseFile("./resultsOverview.csv")
    simplePlot(fileData,"channel","pinChi2")



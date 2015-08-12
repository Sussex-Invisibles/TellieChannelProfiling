from channelPlot import data
from channelPlot import dataSet
import numpy as np
import matplotlib.pyplot as plt


#Method to flag and plot the bad fits
def flagBadFits(dataFile):
    fileData = dataSet()
    fileData.parseFile(dataFile)
    ipw_ChiSq = np.asarray(fileData.findData("ipwChi2").getData())
    pin_ChiSq = np.asarray(fileData.findData("pinChi2").getData())
    meanChiIPW = np.mean(ipw_ChiSq)
    stdChiIPW = np.std(ipw_ChiSq)
    meanChiPIN = np.nanmean(pin_ChiSq)
    stdChiPIN = np.nanstd(pin_ChiSq)
    for i in range(len(ipw_ChiSq)):
	if ipw_ChiSq[i] > meanChiIPW+stdChiIPW:
	    print "Channel %d failed IPW fit test: " %(i+1) 
	if pin_ChiSq[i] > meanChiPIN+stdChiPIN:
	    print "Channel %d failed pin fit test: " %(i+1) 


if __name__=="__main__":
    flagBadFits("./resultsOverview.csv")

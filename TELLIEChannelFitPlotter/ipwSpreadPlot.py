from channelPlot import data
from channelPlot import dataSet
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    fileData = dataSet()
    fileData.parseFile("./resultsOverview.csv")
    ipw_p0 = np.asarray(fileData.findData("ipw_p0").getData())
    ipw_p1 = np.asarray(fileData.findData("ipw_p1").getData())
    ipw_p2 = np.asarray(fileData.findData("ipw_p2").getData())
    ipw_p0_mean = np.mean(ipw_p0)
    ipw_p1_mean = np.mean(ipw_p1)
    ipw_p2_mean = np.mean(ipw_p2)
    
    x = np.linspace(0000,19000,18000)
    total_F = np.zeros((len(ipw_p0),len(x)),dtype=np.float64)
    for i in range(len(ipw_p0)):
        trial_F = ipw_p0[i]+(ipw_p1[i]*x)+(ipw_p2[i]*x**2)
        minIndex = np.argmin(trial_F)
	minY = trial_F[minIndex]
	minX = x[minIndex]
	offset = minX-5000
	shiftUpwards = 0
	if minY>1000:
	    print "Channel %d is above 1000 photons minimum" % (i+1)
	if minY<0:
	    shiftUpwards = -minY
		
	trial_F_shifted = ipw_p0[i]+shiftUpwards+(ipw_p1[i]*(x+offset))+(ipw_p2[i]*(x+offset)**2)
	plt.plot(x,trial_F_shifted,label="Channel %d shifted" %(i+1))
	#plt.plot(x,trial_F,label="Channel %d" % (i+1))
        for j in range(len(x)):
            total_F[i][j] = trial_F[j]

    mean_F = np.mean(total_F,axis=0,dtype=np.float64)
    max_F = np.copy(mean_F) 
    min_F = np.copy(mean_F)
    for i in range(len(ipw_p0)):
       max_F = np.maximum(total_F[i],max_F) 
       min_F = np.minimum(total_F[i],min_F) 
    std_F = np.std(total_F,axis=0,dtype=np.float64)
    sig_above_F = np.add(mean_F,std_F)
    sig_below_F = np.subtract(mean_F,std_F)
    plt.title("Photon Count vs. IPW")
    plt.xlabel("IPW")
    plt.ylabel("Photon Count")
    '''plt.plot(x,mean_F,label="Mean Function")
    plt.plot(x,sig_above_F,label="1 sig above func")
    plt.plot(x,sig_below_F,label="1 sig below func")
    plt.plot(x,max_F,label="Maximum valued func")
    plt.plot(x,min_F,label="Minimum valued func")'''
    #plt.legend(loc="upper right")
    plt.xlim(4300,5000)
    plt.ylim(0,2.5e4)
    plt.axhline(y=1000,linewidth=2,color='r')
    plt.axhline(y=10000,linewidth=2,color='r')
    plt.show()


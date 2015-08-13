''' Script to compare light response of TELLIE channels 
operated at different frequencies. Data has been taken at 
1kHz and 10Hz to match the fire rates in pure calibration 
runs and parsitic calibration runs respectively. 

Author: Ed Leming <e.leming@sussex.ac.uk>
'''
import matplotlib.pyplot as plt
from channelPlot import data
from channelPlot import dataSet
import numpy as np
import optparse

def check_offset(highFile, lowFile, plot=False):
    highData, lowData = dataSet(), dataSet()
    highData.parseFile(highFile)
    lowData.parseFile(lowFile)
    channels = np.asarray(highData.findData("channel").getData())
    low_channels = np.asarray(lowData.findData("channel").getData())
    for channel in channels:
        if np.where(low_channels == channel)[0]:
            cutoff_high = find_parabola_min(highData, np.where(channels == channel)[0])
            cutoff_low = find_parabola_min(lowData, np.where(low_channels == channel)[0]) 
            print channel, cutoff_high, cutoff_low, (cutoff_low - cutoff_high)
            if plot == True:
                plot_curves(highData, lowData, channel)

def find_parabola_min(dataFile, channel_index):
    '''Use differential of parobolic equation to find the dy/dx = 0 point.
    '''
    p1 = dataFile.findData("ipw_p1").getData()[channel_index]
    p2 = dataFile.findData("ipw_p2").getData()[channel_index]
    return -p1/ (2*p2)

def build_fit_line(dataFile, channel , x=None):
    '''Build fit lines for plotting
    '''
    if x == None:
        x = np.linspace(3000, 10000, 1000)
    y = np.zeros(len(x))
    channels = np.asarray(dataFile.findData("channel").getData())
    idx = np.where(channels == channel)[0]
    p0 = dataFile.findData("ipw_p0").getData()[idx]
    p1 = dataFile.findData("ipw_p1").getData()[idx]
    p2 = dataFile.findData("ipw_p2").getData()[idx]
    for i, ent in enumerate(x):
        y[i] = p0 + p1*ent + p2*ent**2
    return x, y
                                               
def plot_curves(highData, lowData, channel):
    '''Plot the two curves for sanity checking
    '''
    low_min = find_parabola_min(lowData, np.where(np.asarray(lowData.findData("channel").getData()) == channel)[0])
    high_min = find_parabola_min(highData, np.where(np.asarray(highData.findData("channel").getData()) == channel)[0])
    if high_min > low_min:
        x = np.arange(high_min-1000,high_min,1)
    else:
        x = np.arange(low_min-1000,low_min,1)
    x, low_line = build_fit_line(lowData, channel, x) 
    x, high_line =build_fit_line(highData, channel, x)
    plt.figure()
    plt.plot(x, high_line, color='Blue', label="1 kHz")
    plt.plot(x, low_line, color='Red', label="10 Hz")
    plt.title("Photon output as a function of IPW: Channel %i" % channel)
    plt.xlabel("IPW (14 bit)")
    plt.ylabel("No. photons")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-H",dest="high",help="High frequency data file to be processed")
    parser.add_option("-l",dest="low",help="Low frequency data file to be processed")
    (options,args) = parser.parse_args()

    if options.high is None:
        raise ValueError("Please pass a file for the high frequency data with -H flag")
    elif options.low is None:
        raise ValueError("Please pass a file for the low frequency data with -l flag")

    check_offset(options.high, options.low, plot=True)

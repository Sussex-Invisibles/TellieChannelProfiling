''' Script to compare light response of TELLIE channels 
operated at different frequencies. Data has been taken at 
1kHz and 10Hz to match the fire rates in pure calibration 
runs and parsitic calibration runs respectively. 

Author: Ed Leming <e.leming@sussex.ac.uk>
'''
import numpy as np
import optparse

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-h",dest="kHz",help="high frequency data file to be processed")
    parser.add_option("-h",dest="kHz",help="high frequency data file to be processed")
    (options,args) = parser.parse_args()

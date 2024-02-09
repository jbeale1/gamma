# Log counts per minute and energy spectrum from Open Gamma board
# 8-Feb-2024 J.Beale

import serial
import numpy as np
import datetime
import os   # os.path.join()

histSize = 4096   # how many bins in peak-level histogram
dRatio = 10       # decimation ratio for short histogram (how many bins stacked together)
readings = 0      # how many lines of data we have received so far
outDir = r"C:/Users/beale/Documents/Scintillator"

# -------------------------------------------------------------------
def showHist(hist):
    shortHist = np.zeros(( 1+int(histSize / dRatio) ))

    for i in range(histSize):
        shortHist[ int(i/dRatio) ] += hist[i]
    
    #print(shortHist)

    # write a file containing energy spectrum, with today's date/time
    outName = datetime.datetime.now().strftime("%y%m%d_%H%M") + "_spec.csv"
    outPath = os.path.join(outDir, outName)
    with open(outPath, 'w') as fout:
        fout.write("counts\n")
        stime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fout.write("# Open Gamma spectrum recorded %s\n" % stime)
        for j in range(len(shortHist)):
            fout.write("%d\n" % shortHist[j])
    

def readCounts(serial_port, baud_rate=115200):
    global readings
    totalCounts = 0
    
    eHist = np.zeros((histSize))
    try:
        ser = serial.Serial(serial_port, baud_rate)
        outName = datetime.datetime.now().strftime("%y%m%d_%H%M") + "_count.csv"
        outPath = os.path.join(outDir, outName)
        fLog = open(outPath, 'w')
        stime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fLog.write("# Open Gamma count start: %s\n" % stime)
        
        while True:
            line = ser.readline().decode('utf-8').strip()
            vals = list(filter(None, line.split(';')))
            counts = len(vals)
            totalCounts += counts
            readings += 1
            for x in vals:
                level = int(x)
                if (level >= histSize):  # presumably not happening but...
                    level = (histSize-1)
                if (level < 0):	 # this would be an odd situation
                    level = 0
                eHist[level] += 1
                # print(level)
                                    
            #print(counts)
            
            if (readings % 60 == 0):                
                time = datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
                print("%s, %d" % (time,totalCounts))
                fLog.write("%d\n" % totalCounts)
                totalCounts = 0
                    
            if (readings % 1800 == 0):                                    
                showHist(eHist)               # show current accumulation
                eHist = np.zeros((histSize))  # reset to zero
                stime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                fLog.write("# time: %s\n" % stime)
                fLog.flush()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if ser.is_open:
            ser.close()
        if fLog.is_open:
            fLog.close()
            
# ---------------------------------------------------------------------            

if __name__ == "__main__":    
    serial_port = 'COM8'   # Pi-Pico device on OpenGammaBoard 
    readCounts(serial_port)


#!/usr/bin/python
from PySide import QtCore,QtNetwork
import time
import sys
import matplotlib.pyplot as plt
def convNum(line):

    numStr = ""
    for c in line:
        if c.encode('hex') != '00':
            numStr += c

    numStr = numStr.rstrip()
    numStr = numStr.strip(" ")
    numstr = numStr.replace('\0','')
    return float(numStr)

if __name__ == "__main__":
    s = QtNetwork.QTcpSocket()

    s.connectToHost('192.168.11.192',2323)
    s.waitForConnected()
    
    #Ready any junk
    s.waitForReadyRead()
    s.readAll()
    
    #Reset device
    s.write("*RST\n")
    s.waitForReadyRead()
    s.readAll()
   

    s.write("SENS:FUNC?\n")
    s.waitForReadyRead()
    print str(s.readLine())

    s.write("SENS:CURR:RANG:AUTO ON\n")
    s.write("\n")
    s.write("SOUR:FUNC VOLT\n")
    s.write("SOUR:VOLT:ILIM 1\n")
    s.write("SOUR:SWE:VOLT:LIN 0, 5, 51, 0.01\n")
    s.write("INIT\n")
    s.write("*OPC?\n")
    s.waitForReadyRead()
    print str(s.readLine())
    

    s.write("TRAC:DATA? 1,51, \"defbuffer1\",SOUR\n")
    s.waitForReadyRead()
    source_str = s.readAll()
   

    s.write("TRAC:DATA? 1,51, \"defbuffer1\",READ\n")
    s.waitForReadyRead()
    read_str = s.readAll()


    volts = []
    for n in source_str.split(','):
        volts.append(convNum(n))

    current = []
    for n in read_str.split(','):
        current.append(convNum(n))

    #print volts
    #print current

    for i in range(len(volts)):
        print (volts[i] / current[i])

    plt.plot(volts,current)
    plt.show()




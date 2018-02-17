import os, sys

def TempProbe(name, serial):
    filePath = '/sys/bus/w1/devices/' + serial + '/w1_slave'
    
    try:
        file = open(filePath)
        filecontent = file.read()
        file.close()

        tempAsString = filecontent.split("\n")[1].split(" ")[9]
        tempConverted = float(tempAsString[2:]) / 1000

        return {"temperature": tempConverted, "raw": filecontent}
    except:
        return 'Couldn\'t read from ' + name + ', serial: ' + serial
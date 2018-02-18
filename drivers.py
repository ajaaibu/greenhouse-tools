import os, sys
import Adafruit_DHT as dht

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

def DHT22(name, pin):
    try:
        h,t = dht.read_retry(dht.DHT22, 4)
        return {"temperature": ('{:3.2f}').format(t), "humidity": ('{:3.2f}').format(h)}
    except:
        return ('Couldn\'t read from %s, pin: %s').format(name, pin)
import os, sys
import Adafruit_DHT as dht

def TempProbe(name, serial):
    filePath = '/sys/bus/w1/devices/%s/w1_slave' % serial
    
    try:
        file = open(filePath)
        filecontent = file.read()
        file.close()

        tempAsString = filecontent.split("\n")[1].split(" ")[9]
        tempConverted = float(tempAsString[2:]) / 1000

        return {"temperature": tempConverted, "raw": filecontent}
    except:
        return 'Couldn\'t read from %s, serial: %s' % (name, serial)

def DHT22(name, pin_no):
    try:
        h,t = dht.read_retry(dht.DHT22, pin_no)
        return {"temperature": ('{0:0.1f}'.format(t)), "humidity": ('{0:0.1f}'.format(h))}
    except:
        return 'Couldn\'t read from %s, pin: %s' % (name, pin_no)
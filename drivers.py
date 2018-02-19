from __future__ import division
import os, sys
import Adafruit_DHT as dht
from subprocess import PIPE, Popen
import psutil

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
        return {"temperature": ('{:3.2f}'.format(t)), "humidity": ('{:3.2f}'.format(h))}
    except:
        return 'Couldn\'t read from %s, pin: %s' % (name, pin_no)

def get_cpu_temperature():
    process = Popen(['vgcencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index("=") + 1:output.rindex("'")])

def PiStats():
    try:
        ram = psutil.virtmem_usage()
        disk = psutil.disk_usage('/')
        return {
            "cpuTemp": get_cpu_temperature(),
            "cpuUsage": psutil.cpu_percent(),
            "ramTotal": ram.total / 2**20,
            "ramUsed": ram.used / 2**20,
            "ramFree": ram.free / 2**20,
            "ramPercentUsed": ram.percent,
            "diskTotal": disk.total / 2**30,
            "diskUsed": disk.used / 2**30
        }
    except:
        return 'Couldn\'t read CPU Stats'
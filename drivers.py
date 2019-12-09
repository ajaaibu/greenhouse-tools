from __future__ import division
import os, sys
import Adafruit_DHT as dht
# from subprocess import PIPE, Popen
import psutil
import time
from gpiozero import DistanceSensor

def TempProbe(name, serial):
    """ Read temperature data from a probe (DS18B20)
    
    Parameters
    ----------
    name: str, required
        Source name, eg: water tank
    serial: str, required
        Serial number of the probe, must be starting with 28-
    """
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

def DHT11(name, pin_no):
    try:
        h,t = dht.read_retry(dht.DHT11, pin_no)
        return {"temperature": ('{:3.2f}'.format(t)), "humidity": ('{:3.2f}'.format(h))}
    except:
        return 'Couldn\'t read from %s, pin: %s' % (name, pin_no)

def DHT22(name, pin_no):
    try:
        h,t = dht.read_retry(dht.DHT22, pin_no)
        return {"temperature": ('{:3.2f}'.format(t)), "humidity": ('{:3.2f}'.format(h))}
    except:
        return 'Couldn\'t read from %s, pin: %s' % (name, pin_no)

def HCSR04(name, pin_tri, pin_echo):
    try:
        sensor = DistanceSensor(echo=pin_echo, trigger=pin_tri, max_distance=1, threshold_distance=0.3)

        return {"distance": sensor.distance, "unit": "meter"}
    except:
        return 'Couln\'t read from Distance Sensor'

def get_cpu_temperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def PiStats():
   try:
        ram = psutil.virtual_memory()
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

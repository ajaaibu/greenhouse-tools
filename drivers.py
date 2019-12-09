from __future__ import division
import os, sys
import Adafruit_DHT as dht
# from subprocess import PIPE, Popen
import psutil
import RPi.GPIO as GPIO
import time

def TempProbe(name: str, serial: str):
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

def DHT11(name: str, pin_no: int):
    try:
        h,t = dht.read_retry(dht.DHT11, pin_no)
        return {"temperature": ('{:3.2f}'.format(t)), "humidity": ('{:3.2f}'.format(h))}
    except:
        return 'Couldn\'t read from %s, pin: %s' % (name, pin_no)

def DHT22(name: str, pin_no: int):
    try:
        h,t = dht.read_retry(dht.DHT22, pin_no)
        return {"temperature": ('{:3.2f}'.format(t)), "humidity": ('{:3.2f}'.format(h))}
    except:
        return 'Couldn\'t read from %s, pin: %s' % (name, pin_no)

def HCSR04(name: str, pin_tri: int, pin_echo: int):
    try:
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(pin_tri, GPIO.OUT)
        GPIO.setup(pin_echo, GPIO.IN)

        GPIO.output(pin_tri, GPIO.LOW)

        print "Waiting for sensor to settle"
        time.sleep(2)
        print "Calculating distance"

        GPIO.output(pin_tri, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(pin_tri, GPIO.LOW)
        GPIO.output(pin_tri, GPIO.LOW)

        while GPIO.input(pin_echo)==0:
                pulse_start_time = time.time()
        while GPIO.input(pin_echo)==1:
                pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        return {"distance": distance, "unit": "cm"}
    finally:
        GPIO.cleanup()

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

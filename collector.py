from drivers import TempProbe, DHT22, DHT11, PiStats, HCSR04
from helpers import log
from models import Readings
from config import config
import datetime, threading, sys

# log data from temperature probes
def read_from_probes(probes):
    for probe in probes:

        data = TempProbe(probe.get('name'), probe.get('serial'))
        if isinstance(data, dict):
            Readings.create(
                sensor = probe.get('name'),
                timestamp = datetime.datetime.now(),
                type = 1,
                value = data.get('temperature')
            )
            log('Temperature reading of %s: %s' % (probe.get('name'),data.get('temperature')))
        elif isinstance(data, str):
            log(data)

def read_from_dht11(dhts):
    for pin in dhts:

        dht_data = DHT11(pin.get('name'), pin.get('pin'))

        if(isinstance(dht_data, dict)):
            Readings.create(
                sensor = pin.get('name') + ' Temperature',
                timestamp = datetime.datetime.now(),
                type = 1,
                value = dht_data.get('temperature')
            )

            Readings.create(
                sensor = pin.get('name') + ' Humidity',
                timestamp = datetime.datetime.now(),
                type = 2,
                value = dht_data.get('humidity')
            )
            log('%s Temperature: %s' % (pin.get('name'), dht_data.get('temperature')))
            log('%s Humidity: %s' % (pin.get('name'), dht_data.get('humidity')))
        elif isinstance(dht_data, str):
            log(dht_data)

def read_from_dht22(dhts):
    for pin in dhts:

        dht_data = DHT22(pin.get('name'), pin.get('pin'))

        if(isinstance(dht_data, dict)):
            Readings.create(
                sensor = pin.get('name') + ' Temperature',
                timestamp = datetime.datetime.now(),
                type = 1,
                value = dht_data.get('temperature')
            )

            Readings.create(
                sensor = pin.get('name') + ' Humidity',
                timestamp = datetime.datetime.now(),
                type = 2,
                value = dht_data.get('humidity')
            )
            log('%s Temperature: %s' % (pin.get('name'), dht_data.get('temperature')))
            log('%s Humidity: %s' % (pin.get('name'), dht_data.get('humidity')))
        elif isinstance(dht_data, str):
            log(dht_data)

def read_cpu():
    cpu_data = PiStats()

    if isinstance(cpu_data, dict):
        Readings.create(
            sensor = 'Pi Temperature',
            timestamp = datetime.datetime.now(),
            type = 1,
            value = cpu_data.get('cpuTemp')
        )

        log('Pi Tempearture: %s' % cpu_data.get('cpuTemp'))

        Readings.create(
            sensor = 'CPU Usage',
            timestamp = datetime.datetime.now(),
            type = 4,
            value = cpu_data.get('cpuUsage')
        )

        log('CPU Usage: %s' % cpu_data.get('cpuUsage'))

        Readings.create(
            sensor = 'RAM Used',
            timestamp = datetime.datetime.now(),
            type = 5,
            value = cpu_data.get('ramUsed')
        )

        log('RAM Used: %s' % cpu_data.get('ramUsed'))
        
    elif isinstance(cpu_data, str):
        log(cpu_data)

def read_from_hcsr04(sensors):
    for sensor in sensors:
        sensor_data = HCSR04(sensor.get('name'), sensor.get('pin_tri'), sensor.get('pin_echo'))

        if(isinstance(sensor_data, dict)):
            Readings.create(
                sensor = sensor.get('name') + ' Distance',
                timestamp = datetime.datetime.now(),
                type = 6,
                value = sensor_data.get('distance')
            )
            log('%s Distance: %s' % (sensor.get('name'), sensor_data.get('distance')))
        elif isinstance(sensor_data, str):
            log(sensor_data)

threads = []

if '--probes' in sys.argv:
    probes_thread = threading.Thread(target=read_from_probes, args=(config.get('DS18B20'),))
    threads.append(probes_thread)
    probes_thread.start()


if '--dht' in sys.argv:
    if config.get('DHT11'):
        dht11_thread = threading.Thread(target=read_from_dht11, args=(config.get('DHT11'),))
        threads.append(dht11_thread)
        dht11_thread.start()

    if config.get('DHT22'):
        dht22_thread = threading.Thread(target=read_from_dht22, args=(config.get('DHT22'),))
        threads.append(dht22_thread)
        dht22_thread.start()

if '--distance' in sys.argv:
    if config.get('HCSR04'):
        distance_thread = threading.Thread(target=read_from_hcsr04, args=(config.get('HCSR04'),))
        threads.append(distance_thread)
        distance_thread.start()


if '--cpu' in sys.argv:
    cpu_thread = threading.Thread(target=read_cpu)
    threads.append(cpu_thread)
    cpu_thread.start()

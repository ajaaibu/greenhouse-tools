from drivers import TempProbe, DHT22, PiStats
from helpers import log
from models import Readings
from config import config
import datetime, threading, sys

# log data from temperature probes
def read_from_probes(probes):
    for probe in probes:

        data = TempProbe(probe.get('name'),probe.get('serial'))
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

def read_from_dht(dhts):
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

threads = []

if '--probes' in sys.argv:
    probes_thread = threading.Thread(target=read_from_probes, args=(config.get('DS18B20'),))
    threads.append(probes_thread)
    probes_thread.start()


if '--dht' in sys.argv:
    dht_thread = threading.Thread(target=read_from_dht, args=(config.get('DHT22'),))
    threads.append(dht_thread)
    dht_thread.start()

if '--cpu' in sys.argv:
    cpu_thread = threading.Thread(target=read_cpu)
    threads.append(cpu_thread)
    cpu_thread.start()

from drivers import TempProbe
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
            log('Temperature reading of ' + probe.get('name') + ': ' + probe.get('temperature'))
        elif isinstance(data, str):
            log(data)

threads = []

if '--probes' in sys.argv:
    probes_thread = threading.Thread(target=read_from_probes, args=(config.get('DS18B20'),))
    threads.append(probes_thread)
    probes_thread.start()
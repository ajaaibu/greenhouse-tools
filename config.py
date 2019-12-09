config = {
    # Mapping of DS18B20 temperature probes.
    # Please set a name, serial number must only contain serial of the probe starting with 28-
    "DS18B20" : [
        {
            'name': 'Water Tank',
            'serial': '28-0114551035aa'
        }
        # {
        #     'name': 'Nutrition Tank',
        #     'serial': '28-041685d1d1ff'
        # }
    ],

    "DHT11": [
        {
            'name': 'House',
            'pin': 14
        }
    ],

    "DHT22": [
    ],

    "HCSR04": [
        {
            'name': 'Water tank',
            'pin_tri': 23,
            'pin_echo': 24
        }
    ]
}

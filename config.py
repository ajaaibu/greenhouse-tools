config = {
    # Mapping of DS18B20 temperature probes.
    # Please set a name, serial number must only contain serial of the probe starting with 28-
    "DS18B20" : [
        {
            'name': 'Water Tank',
            'serial': '28-031685612cff'
        },
        {
            'name': 'Nutrition Tank',
            'serial': '28-041685d1d1ff'
        }
    ],

    "DHT": [
        {
            'name': 'House',
            'pin': 14
        }
    ]
}

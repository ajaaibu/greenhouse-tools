# GreenHouse Data Collection & Sync Tools

This is a collection of python scripts to collect data from different sensors attached to a Raspberry-Pi and then sync it to a central server for remote observations.

## Setup
Believe me, this Readme might be long, but its pretty simple.

### Requirements
- Python
- Pipenv
- MySQL / MariaDB

Make sure you have the above mentioned pre-requisities installed on the Raspberry-Pi and have already created a database. Don't worry about the tables this will create tables for you if it does not already exist.

```sh
git clone repository
cd repository
pipenv install
cp .env.example .env
```

- Update .env file as required
- Update config.py and make sure you have correct mapping to sensors & pins.

## Data collection & Sync Jobs
You have to first switch to the virtualenv at which the requisities for the project are installed.

To switch to virtualenv `cd` into the project root and run `pipenv shell`

Now you should have a shell instance of the virtualenv 

### Data collector
`collector.py` will accept multiple arguments, you have to give atleast one to record a data

#### Argument definitions
- --probes will run the data collection method for temperature reading from DS18B20 mapping

You are free to decide how you run the collector, it is designed to run multiple collection methods in a run, each method will be run in a separate thread

Sample: `python collector.py --probes` will run only data collection from DS18B20.

### Syncing
The sync tool provided with this only makes sure that the data recorded locally on the Raspberry-Pi is pushed to an endpoint. The endpoint is assumed to be protected with http2 basic authentication. 

Below is a sample payload

```json
{
    "system": "Pi-1234",
    "readings": [
        {
            "id": 1,
            "sensor": "Water Tank Temperature",
            "type": 1,
            "timestamp": "2018-02-12 18:30:00",
            "value": "28.43"
        },
        {
            "id": 2,
            "sensor": "Nutrition Tank Temperature",
            "type": 1,
            "timestamp": "2018-02-12 18:31:00",
            "value": "29.01"
        }
    ]
}
```

The endpoint is expected to provide the response in following format after recording the data

```json
[
    {
        "local": 1,
        "cloud": 12
    },
    {
        "local": 2,
        "cloud": 13
    }
]
```
from models import  *
from helpers import model_to_dict, file_is_locked
import json, requests, sys

lock_handle = None

file_path = '/tmp/readings'

if(file_is_locked(file_path)):
    print 'Another instance of the job is already running'
    sys.exit(0)

else:
    print 'No instance is running, continuing to sync'
    json = []
    for reading in Readings.select().where(Readings.dbsync==False).limit(SYNC_LIMIT):
        json.append(reading.to_dict())

    try: 
        r = requests.post(SYNC_URL,json={"system": SYSTEM_ID, "readings": json}, auth=(CLOUD_USERNAME,CLOUD_PASSWORD))

        if r.status_code == requests.codes.ok:

            updated =  r.json()

            for record in updated:
                query = Readings.update(dbsync=True, syncref=record['cloud']).where(Readings.id == record['local'])
                query.execute()
                print 'Updated record', record['local']

        else:
            print 'Got a bad response from server'

    except: 
        print 'DB Syncing failed for some reason'
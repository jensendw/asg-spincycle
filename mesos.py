import requests
import random
import json
import nanotime
#from settings import *

MESOS_MASTERS=['http://mes01mn0001.o1.usw2.origami42.com:5050','http://mes01mn0002.o1.usw2.origami42.com:5050']

def schedule_mesos_agent_maintenance(ip):
    url = random.choice(MESOS_MASTERS) + '/maintenance/schedule'

    headers = {'Content-type': 'application/json'}

    body = {'windows': [
        {
            'machine_ids': [
                {'ip':ip}
            ],
            'unavailability': {
                'start':{'nanoseconds':int(nanotime.now())},
                'duration':{'nanoseconds':3600000000000}
            }
        }
    ]}
    response = requests.post(url, headers=headers, data=json.dumps(body))

    print(response.content)

def set_mesos_agent_maintenance(ip, status):
    #setup the maintenance schedule first
    schedule_mesos_agent_maintenance(ip)

    url = random.choice(MESOS_MASTERS) + '/master/machine/' + status

    headers = {'Content-type': 'application/json'}

    #response = requests.post(url, headers=headers, data=json.dumps([{"ip":ip,"hostname":ip}]))
    response = requests.post(url, headers=headers, data=json.dumps([{"ip":ip}]))

    print(response.content)
        #        'start':{'nanoseconds':int(nanotime.now())},
        #        'duration':{'nanoseconds':3600000000000}


set_mesos_agent_maintenance('172.17.87.52', 'down')

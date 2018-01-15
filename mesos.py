import requests
from settings import *

def set_mesos_agent_maintenance(hostname, ip, status):
    
    requests.post(MESOS_MASTERS, data = {'key':'value'}))

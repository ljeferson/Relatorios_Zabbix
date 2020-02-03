#pip install py-zabbix
from pyzabbix.api import ZabbixAPI
from requests import get
import time
from datetime import datetime, timedelta
import json

zabbix = {}
with open('conf.json', 'r') as confs:
    zabbix = json.loads(confs.read())

timeFrom = "01/01/2020 00:00"
timeTill = "31/01/2020 23:59"

fromTimestamp = time.mktime(datetime.strptime(timeFrom, "%d/%m/%Y %H:%M").timetuple())
tillTimestamp = time.mktime(datetime.strptime(timeTill, "%d/%m/%Y %H:%M").timetuple())


try:
    zapi = ZabbixAPI(url=zabbix['url'], user=zabbix['username'], password=zabbix['password'])
    print ('Auth Ok!')
except Exception as err:
    print('Erro ao conectar ao Zabbix')
    print('Erro: {}'.format(err))


hostgroup = 'SICI'


getHostGroup = zapi.do_request('hostgroup.get',
                            {
                                "output": "extend",
                                "filter": {
                                    "name": [
                                        hostgroup
                                    ],
                                "sortfield": ["name"],
                                "sortorder": "DESC"
                                }
                            }
                        )


print(getHostGroup)
#apiVersion = zapi.do_request('apiinfo.version')


request = zapi.do_request('event.get',
                            {
                                "output": "extend",
                                "select_acknowledges": "extend",
                                "selectTags": "extend",
                                "selectSuppressionData": "extend",
                                "groupids": getHostGroup['result'][0]["groupid"],
                                "severities": [5],
                                "time_from": fromTimestamp,
                                "time_till": tillTimestamp
                            }
                        )

sortedResult = json.loads(json.dumps(request['result'], sort_keys=True))

#print('{}\n{}\n'.formt(request).format(json.dumps(request, indent=4, separators=("", " : "))))
events = 0
hostName = ''
totalOffTime = timedelta()

for ev in sortedResult:
    getR_event = zapi.do_request('event.get', {"output": "extend",
                                               "eventids": ev['r_eventid'],
                                               })
    if(ev['name'] != hostName):
        print('Host: {0} - Tempo off: {1} - eventos: {2}'.format(hostName.split(' ')[0].split(' ')[0], totalOffTime, events) )
        hostName = ev['name']
        events = 0
        totalOffTime = timedelta()


    totalOffTime += datetime.fromtimestamp(int(getR_event['result'][0]['clock'])) - datetime.fromtimestamp(int(ev['clock']))


    #print('{}\n\n'.format(json.dumps(getR_event, indent=4, separators=("", " : "))))

    '''
    print('{0},{1},{2},{3},{4},{5}'.format(events+1,
                        ev['eventid'],
                        ev['name'],
                        datetime.fromtimestamp(int(ev['clock'])),
                        datetime.fromtimestamp(int(getR_event['result'][0]['clock'])),
                        datetime.fromtimestamp(int(getR_event['result'][0]['clock'])) - datetime.fromtimestamp(int(ev['clock']))
                        )
    )
    '''

    events += 1

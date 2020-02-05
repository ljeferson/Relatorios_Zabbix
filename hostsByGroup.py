#pip install py-zabbix
from pyzabbix.api import ZabbixAPI
from requests import get
import time
from datetime import datetime, timedelta
import json

zabbix = {}
with open('conf.json', 'r') as confs:
    zabbix = json.loads(confs.read())

timeFrom = "01/01/2020 00:00:00"
timeTill = "31/01/2020 23:59:59"

fromTimestamp = time.mktime(datetime.strptime(timeFrom, "%d/%m/%Y %H:%M:%S").timetuple())
tillTimestamp = time.mktime(datetime.strptime(timeTill, "%d/%m/%Y %H:%M:%S").timetuple())


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


getHost = zapi.do_request('host.get',
                            {
                                "output": "extend",
                                "selectGroups": "extend",
                                "groupids": getHostGroup['result'][0]["groupid"]
                            }
                        )

#sortedResult = json.loads(json.dumps(request['result'], sort_keys=True))

#print('{}\n{}\n'.formt(request).format(json.dumps(request, indent=4, separators=("", " : "))))
events = 0
hostName = ''
totalOffTime = timedelta()

#Tempo formatado para criação de arquivo
#timeFromFormated = timeFrom.replace('/', '_').replace(':', '_')
#timeTillFormated = timeTill.replace('/', '_').replace(':', '_')

print('{}\n\n'.format(json.dumps(getHost, indent=4, separators=("", " : "))))



with open('hosts.csv', 'w') as arqhosts:
    for host in getHost['result']:
        arqhosts.write('{0};{1}\n'.format(host['host'], host['name']))
        events += 1

print('\nQuantidade de hosts: {}'.format(events))

'''
with open('hosts.csv', 'w') as relatorio:
    for ev in hostGet:
        if(ev['name'] != hostName):
            if(hostName == ''):
                relatorio.write('Host;Tempo Off;Incidentes\n' )
            else:
                relatorio.write('{0};{1};{2}\n'.format(hostName.split(' is')[0], totalOffTime, events))
            hostName = ev['name']
            events = 0
            totalOffTime = timedelta()

        if(ev['r_eventid'] != "0"):
            totalOffTime += datetime.fromtimestamp(int(getR_event['result'][0]['clock'])) - datetime.fromtimestamp(int(ev['clock']))
        else:
            totalOffTime += datetime.fromtimestamp(int(tillTimestamp)) - datetime.fromtimestamp(int(ev['clock']))

        print('{0},{1},{2}'.format(events+1, ev['eventid'], ev['name']), totalOffTime)
        
        print('{0},{1},{2},{3},{4},{5}'.format(events+1,
                            ev['eventid'],
                            ev['name'],
                            datetime.fromtimestamp(int(ev['clock'])),
                            datetime.fromtimestamp(int(getR_event['result'][0]['clock'])),
                            datetime.fromtimestamp(int(getR_event['result'][0]['clock'])) - datetime.fromtimestamp(int(ev['clock']))
                            )
        )
        
        events += 1
        if(sortedResult[-1] == ev):
            relatorio.write('{0};{1};{2}\n'.format(hostName.split(' is')[0], totalOffTime, events))
'''
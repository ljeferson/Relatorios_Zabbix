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

#Tempo formatado para criação de arquivo
timeFromFormated = timeFrom.replace('/', '_').replace(':', '_')
timeTillFormated = timeTill.replace('/', '_').replace(':', '_')

with open('relatorio-{0}_to_{1}.csv'.format(timeFromFormated, timeTillFormated), 'w') as relatorio:
    relatorio.write('Host;Tempo Off;Incidentes\n')
    for host in getHost['result']:
        print('\n{0};{1}'.format(host['host'], host['name']))
        events = 0
        totalOffTime = timedelta()

        getEvents = zapi.do_request('event.get',
                                    {
                                        "output": "extend",
                                        "select_acknowledges": "extend",
                                        "selectTags": "extend",
                                        "selectSuppressionData": "extend",
                                        "hostids": host["hostid"],
                                        "severities": [5],
                                        "time_from": fromTimestamp,
                                        "time_till": tillTimestamp
                                    }
                                )

        for ev in getEvents['result']:
            events += 1
            getR_event = zapi.do_request('event.get', {"output": "extend",
                                                       "eventids": ev['r_eventid'],
                                                       })
            print('{0};{1};{2}'.format(events, ev['name'], datetime.fromtimestamp(int(ev['clock'])) ) )

            if (ev['r_eventid'] != "0"):
                totalOffTime += datetime.fromtimestamp(int(getR_event['result'][0]['clock'])) - datetime.fromtimestamp(int(ev['clock']))
            else:
                totalOffTime += datetime.fromtimestamp(int(tillTimestamp)) - datetime.fromtimestamp(int(ev['clock']))

        print('{0};{1};{2}'.format(host['host'], events, totalOffTime ) )
        relatorio.write('{0};{1};{2}\n'.format(host['host'], totalOffTime,  events))
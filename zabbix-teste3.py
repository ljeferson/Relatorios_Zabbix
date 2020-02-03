from pyzabbix.api import ZabbixAPI
from requests import get
import time
from datetime import datetime, timedelta
import json

 	
from datetime import datetime as indatetime


url = 'http://10.48.0.99/zabbix/api_jsonrpc.php'
username = 'lucas.silva'
password = 'LucasJ26'

timeFrom = "01/1/2020 00:00"
timeTill = "24/1/2020 16:00"

fromTimestamp = time.mktime(datetime.strptime(timeFrom, "%d/%m/%Y %H:%M").timetuple())
tillTimestamp = time.mktime(datetime.strptime(timeTill, "%d/%m/%Y %H:%M").timetuple())


try:
    zapi = ZabbixAPI(url=url, user=username, password=password)
    print ('Auth Ok!')
except Exception as err:
    print('Erro ao conectar ao Zabbix')
    print('Erro: {}'.format(err))


hostname = 'CL-MATEUS-MAIOBAO-14.162'


gethost = zapi.do_request('host.get',
                            {
                                "filter": {
                                    "host": [
                                        hostname
                                    ]
                                }
                            }
                        )


'''
request = zapi.do_request('problem.get',
                            {
                                "output": "extend",
                                #"selectAcknowledges": "extend",
                                "selectTags": "extend",
                                "selectSuppressionData": "extend",
                                "hostids": gethost['result'][0]["hostid"],
                                "recent": "false",
                                "sortfield": ["eventid"],
                                "sortorder": "DESC"
                                #"time_from": fromTimestamp,
                                #"time_till": tillTimestamp
                            }
                        )
'''

#apiVersion = zapi.do_request('apiinfo.version')

request = zapi.do_request('event.get',
                            {
                                "output": "extend",
                                "select_acknowledges": "extend",
                                "selectTags": "extend",
                                "selectSuppressionData": "extend",
                                "hostids": gethost['result'][0]["hostid"],
                                "sortfield": ["clock", "eventid"],
                                "sortorder": "DESC",
                                "limit": 10,
                                "severities": [5]
                                #"time_from": fromTimestamp,
                                #"time_till": tillTimestamp
                            }
                        )

incidentes = 0
# datetime(year, month, day, hour, minute, second, microsecond)
totalOffTime = timedelta()

print("Incedente: {0} \nTempo off: {1}\n\n\n".format(incidentes, totalOffTime))


#print(request)
#print('{}\n\n'.format(json.dumps(request, indent=4, separators=("", " : "))))
for event in request['result']:
    getR_event = zapi.do_request('event.get', {"output": "extend",
                                            "eventids": event['r_eventid'],
                                            })
    clock = datetime.fromtimestamp(int(event['clock']))
    r_clock = datetime.fromtimestamp(int(getR_event['result'][0]['clock']))
    offTime = (r_clock, r_clock - clock)[1]


    #print("{}\n".format(offTime))
    print('Hora do evento: {0} \nHora da Recuperação: {1} \nTempo fora: {2}'.format(clock, r_clock, offTime))
    #print('{}\n\n'.format(json.dumps(getR_event['result'][0], indent=4, separators=("", " : "))))
    print('Evento id({0}), nome ({1}), hora({2}), id de recuperação({3}), hora de recuperação({4})\n\n'.format(event['eventid'],
                                                                                    event['name'],
                                                                                    event['clock'],
                                                                                    event['r_eventid'],
                                                                                    getR_event['result'][0]['clock'],
                                                                                    )
    )
    incidentes += 1
    totalOffTime += offTime


print("Total de incidentes: {0} \nTotal de tempo off: {1}".format(incidentes, totalOffTime))
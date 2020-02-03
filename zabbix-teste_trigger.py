from pyzabbix import ZabbixAPI
from requests import get
import time
import datetime
import json


url = 'http://10.48.0.99/zabbix/api_jsonrpc.php'
username = 'lucas.silva'
password = 'LucasJ26'

timeFrom = "19/1/2020 09:00"
timeTill = "24/1/2020 16:00"

fromTimestamp = time.mktime(datetime.datetime.strptime(timeFrom, "%d/%m/%Y %H:%M").timetuple())
tillTimestamp = time.mktime(datetime.datetime.strptime(timeTill, "%d/%m/%Y %H:%M").timetuple())


try:
    zapi = ZabbixAPI(url, timeout=4)
    zapi.login(username,password)
    print ('Auth Ok!')
except Exception as err:
    print('Erro ao conectar ao Zabbix')
    print('Erro: {}'.format(err))

#f  = {  'name' : args.I  }
#items = zapi.item.get(host='EQTPI-SE-CHESF-DIR-SE-ELISEU-MARTINS-RADIO', output='extend' )
host = zapi.host.get(filter={"host": 'EQTPI-SE-CHESF-DIR-SE-ELISEU-MARTINS-RADIO'} )

#items = zapi.item.get(host=gethost)
#print(items)

#print(host)

triggers = zapi.trigger.get(host='EQTPI-SE-CHESF-DIR-SE-ELISEU-MARTINS-RADIO',
                            #only_true=1,
                            skipDependent=1,
                            monitored=1,
                            active=1,
                            output='extend',
                            expandDescription=1,
                            expandExpression=1,
                            #selectHosts=['EQTPI-SE-CHESF-DIR-SE-ELISEU-MARTINS-RADIO'],
                            )

#print(triggers)

print('time_from: {}\n'.format(fromTimestamp))
print('time_till: {}\n\n\n'.format(tillTimestamp))

for trigger in triggers:
    print('Trigger ID: {}\n'.format(trigger['triggerid']))

    problems = zapi.problem.get(
    applicationids=trigger['triggerid'],
    #time_from=fromTimestamp,
    #time_till=tillTimestamp,
    #selectFunctions= "extend",
    output= "extend",
    selectAcknowledges= "extend",
    selectTags = "extend",
    selectSuppressionData = "extend",
    recent = "true",
    #sortfield = ["eventid"],
    #sortorder="DESC"
    )

    #print('{}\n\n\n'.format(json.dumps(trigger, indent=4, separators=("", " : "))))
    #print('Hora do incidente: {}'.format(datetime.datetime.fromtimestamp(problems[0]['clock'])))
    print('{}\n\n\n'.format(problems))
    '''
    for problem in problems:
        print('{}\n\n\n'.format(json.dumps(problem, indent=4, separators=("", " : "))))
    '''

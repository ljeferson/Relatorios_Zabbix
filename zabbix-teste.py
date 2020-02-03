from pyzabbix import ZabbixAPI
from requests import get
import time
import datetime


url = 'http://10.48.0.99/zabbix/api_jsonrpc.php'
username = 'lucas.silva'
password = 'LucasJ26'

timeFrom = "21/1/2020 09:00"
timeTill = "21/1/2020 16:00"

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
gethost = 'EQTPI-SE-UNIAO-MODEM-OI'
items = zapi.item.get(host=gethost, output='extend' )
#items = zapi.item.get(host=gethost)
#print(items)

for item in items:
    print('{}\n\n\n'.format(item['hostid']))


    values = zapi.problem.get(hostids=item['hostid'],
    #time_from=fromTimestamp,
    #time_till=tillTimestamp,
    #sortorder="DESC"
    )

    #print(values)


    for historyValue in values:
            #currentDate = datetime.datetime.fromtimestamp(int(historyValue['clock'])).strftime('%d/%m/%Y %H:%M:%S')

            #print ("{} {} Value: {}".format(historyValue['clock'], currentDate, historyValue['value']))
            print("\n\n{}".format(historyValue))

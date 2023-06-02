
import json

import time

import os

import requests

 

cookies = {

 '_gid': 'GA1.2.1261081693.1685670498',

'_ga': 'GA1.2.598386974.1685670497',

'koa:sess': 'eyJ1c2VySWQiOjM1MzYzNywiX2V4cGlyZSI6MTcxMTU5MDg5MzAzNywiX21heEFnZSI6MjU5MjAwMDAwMDB9',

'koa:sess.sig': '_I8IeLXlrniJHTakhb6jpua33JI',

'_ga_CZFVKMNT9J': 'GS1.1.1685670496.1.1.1685670916.0.0.0'

}

 

_COOKIES = ';'.join(map(lambda x:'='.join(x),cookies.items()))

_TOTAL_BUDGET = 5

_PROXY = None

 

def process(proxy = None) -> str:

 _HOST = "glados.rocks"

 _ORIGIN_URL =f"https://{_HOST}"

 _USER_AGENT = "Mozilla/5.0(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/91.0.4472.114 Safari/537.36"

 

 checkin_url =f"{_ORIGIN_URL}/api/user/checkin"

 status_url =f"{_ORIGIN_URL}/api/user/status"

 referer_url =f"{_ORIGIN_URL}/console/checkin"

 traffic_url =f"{_ORIGIN_URL}/api/user/traffic"

 payload = {'token':'glados.network'}

 

 checkin =requests.post(checkin_url,

 headers={'cookie': _COOKIES,

  'referer': referer_url,

 'origin':_ORIGIN_URL,

 'user-agent':_USER_AGENT,

  'content-type':'application/json;charset=UTF-8'},

 data=json.dumps(payload),

 proxies=proxy)

 msg = checkin.json()['message']

 if msg =='\u6ca1\u6709\u6743\u9650':

     return checkin.close() or'Failed due to expired cookies!'

 

 status = requests.get(status_url,

 headers={'cookie': _COOKIES,

  'referer': referer_url,

 'origin': _ORIGIN_URL,

 'user-agent': _USER_AGENT},

 proxies=proxy)

 surplus =str(status.json()['data']['leftDays']).split('.')[0]

 vip_level =status.json()['data']['vip']

 

 traffic =requests.get(traffic_url,

 headers={'cookie': _COOKIES,

  'referer': referer_url,

 'origin':_ORIGIN_URL,

 'user-agent':_USER_AGENT,

 'content-type':'application/json;charset=UTF-8'},

 proxies=proxy)

 used_gb =traffic.json()["data"]["today"] / 1024**3

 

 logMsg = (

 '--------------------\n' +

 'GLaDOS CheckIn\n' +

 'Msg: ' + msg + '\n' +

 'Surplus: ' + surplus + 'Day\n' +

 'Usage: ' + '%.3f' % used_gb +

 '/%.1f' % _TOTAL_BUDGET + 'GB\n' +

 '--------------------'

 )

 checkin.close()

 status.close()

 traffic.close()

 

 return logMsg

 

 

timeOfDay = time.strftime("%Y-%m-%d %H:%M", time.localtime())

logFilePath = os.getcwd() + '/log.txt'

logFile = open(logFilePath,mode='a')

try:

 logMsg = process()

except:

 try:logMsg = process(_PROXY)

 except:logMsg = "Failed dueto network factors"

writeMsg = (

 '[' + timeOfDay + ']' + '\n' +

 logMsg + '\n'

 )

logFile.write(writeMsg)

print(writeMsg)

logFile.close()

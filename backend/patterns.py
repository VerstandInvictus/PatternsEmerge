import cgitb
import pprint
from bs4 import BeautifulSoup
import operator
from itertools import izip
import pymongo
from flask import Flask, json, Response, request
from flask_cors import CORS
from flask_compress import Compress
import os
import arrow
import mdcore

cgitb.enable()

timeformat = "YYYY-MM-DD HH:mm:ss ZZ"
user_agent = (
    'User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')

client = pymongo.MongoClient()
tradeDb = client.patternsemerge


app = Flask(__name__)
# development CORS convenience headers
CORS(app, headers=['Content-Type'], supports_credentials=True)
# live app headers
# CORS(app)
Compress(app)

logfile = os.path.join("logs", "patterns.log")

def logWrite(item):
    datestr = arrow.utcnow().to("US/Pacific").format(timeformat) + ": "
    with open(logfile, "a") as log:
        logstr = datestr + item + "\n"
        log.write(logstr)
    return logstr


def jsonWrapper(inputStructure, isCursor=1):
    if not request.is_xhr:
        indent = 4
    else:
        indent = None
    if isCursor == 1:
        outval = list(inputStructure)
    else:
        outval = inputStructure
    return Response(
        json.dumps(outval, indent=indent),
        mimetype='application/json')


def extractOrdersFromTable(soup):
    trows = list()
    fieldNames = list()
    for head in soup.find_all('th'):
        fieldNames.append(head.button.text)
    for row in soup.find_all('tr')[1:]:
        rlist = dict()
        for col, name in zip(row.find_all('td'), fieldNames):
            rlist[name] = col.text
        if rlist['Status'] == 'Filled':
            trows.append(rlist)
    return trows


def assembleTrades(trows):
    sorted_rows = sorted(trows, key=operator.itemgetter('Updated'))
    a = iter(sorted_rows)
    trades = list()
    for trade in izip(a, a):
        tdict = dict()
        tdict['entry'] = float(trade[0]['Avg. Fill'])
        tdict['exit'] = float(trade[1]['Avg. Fill'])
        if trade[0]['Side'] == 'Sell':
            tdict['total'] = tdict['entry'] - tdict['exit']
            tdict['direction'] = 'Short'
        elif trade[0]['Side'] == 'Buy':
            tdict['total'] = tdict['exit'] - tdict['entry']
            tdict['direction'] = 'Long'
        tdict['entryTime'] = trade[0]['Updated'].split(' ')[0]
        tdict['exitTime'] = trade[1]['Updated'].split(' ')[0]
        tdict['date'] = ' '.join(trade[0]['Updated'].split(' ')[1:])
        trades.append(tdict)
    return trades


@app.route('/update/<strategy>')
def updateTrades(strategy):
    logger = mdcore.mdLogger(os.path.join('logs', 'mdcore.log'))
    md = mdcore.marketdelta(logger, strategy)
    ordertable = md.getOrderList()
    md.exit()
    ordersoup = BeautifulSoup(ordertable, 'html.parser')
    rows = extractOrdersFromTable(ordersoup)
    trades = (assembleTrades(rows))
    pprint.pprint(trades)
    tradeDb.strategy.insert_many(trades)


@app.route('/list/<strategy>')
def listTrades(strategy):
    logWrite("requested fridged teardowns")
    return jsonWrapper(tradeDb.strategy.find(
        filter={}
    )), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

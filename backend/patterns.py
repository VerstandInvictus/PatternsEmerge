import cgitb
import pprint
from bs4 import BeautifulSoup
import operator
from itertools import izip
import pymongo
from flask import Flask, json, Response, request
from flask_cors import CORS
import os
import arrow
import mdcore
from copy import deepcopy
import config

cgitb.enable()

timeformat = "YYYY-MM-DD HH:mm:ss ZZ"

client = pymongo.MongoClient()
tradeDb = client.patternsemerge


app = Flask(__name__)
# development CORS convenience headers
CORS(app, headers=['Content-Type'], supports_credentials=True)
# live app headers
# CORS(app)

logdir = os.path.join("/", "var", "repos", "patterns", "PatternsEmerge",
                      "backend", "logs")

logfile = os.path.join(logdir, "patterns.log")
mdlog = os.path.join(logdir, "mdcore.log")

print logdir


def logWrite(item):
    datestr = arrow.utcnow().to("US/Pacific").format(timeformat) + ": "
    with open(logfile, "a+") as log:
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
    if not soup.find_all(text="There are no orders to display."):
        for head in soup.find_all('th'):
            fieldNames.append(head.button.text)
        for row in soup.find_all('tr')[1:]:
            rlist = dict()
            for col, name in zip(row.find_all('td'), fieldNames):
                rlist[name] = col.text
            if rlist['Status'] == 'Filled':
                trows.append(rlist)
        return trows
    else:
        return None


def assembleTrades(trows):
    splitrows = list()
    trades = list()
    for order in trows:
        order['Copy'] = '0'
        if int(order['Qty']) > 1:
            for i in range(1, int(order['Qty'])):
                splitorder = deepcopy(order)
                splitorder['Qty'] = '1'
                splitorder['Order #'] += str(i)
                splitrows.append(splitorder)
            order['Qty'] = '1'
            splitrows.append(order)
        else:
            splitrows.append(order)
    sorted_rows = sorted(splitrows, key=operator.itemgetter('Updated'))
    while len(sorted_rows) > 0:
        enter = sorted_rows.pop(0)
        if enter['Side'] == "Sell":
            match = "Buy"
        elif enter['Side'] == "Buy":
            match = "Sell"
        for i, order in enumerate(sorted_rows):
            if order['Side'] == match:
                trexit = sorted_rows.pop(i)
                break
        tdict = dict()
        tdict['entry'] = float(enter['Avg. Fill'])
        tdict['exit'] = float(trexit['Avg. Fill'])
        if enter['Side'] == 'Sell':
            tdict['total'] = tdict['entry'] - tdict['exit']
            tdict['direction'] = 'Short'
        elif enter['Side'] == 'Buy':
            tdict['total'] = tdict['exit'] - tdict['entry']
            tdict['direction'] = 'Long'
        tdict['entryTime'] = enter['Updated'].split(' ')[0]
        tdict['exitTime'] = trexit['Updated'].split(' ')[0]
        tdict['date'] = ' '.join(enter['Updated'].split(' ')[1:])
        tdict['_id'] = '-'.join((enter['Order #'], trexit['Order #']))
        trades.append(tdict)
    return trades


@app.route('/')
def restateAssumptions():
    return 'First: Restate your assumptions.'


@app.route('/update/<strategy>')
def updateTrades(strategy):
    logger = mdcore.mdLogger(mdlog)
    md = mdcore.marketdelta(logger, strategy)
    ordertable = md.getOrderList()
    md.exit()
    ordersoup = BeautifulSoup(ordertable, 'html.parser')
    rows = extractOrdersFromTable(ordersoup)
    if not rows:
        logWrite("No trades found.")
        return "No trades found."
    trades = (assembleTrades(rows))
    for trade in trades:
        res = tradeDb[strategy].replace_one(
            {"_id": trade['_id']}, trade, True)
        logWrite("wrote trade to DB: {0}".format(trade))
        logWrite("response from Mongo: {0}".format(res))
    return jsonWrapper(trades, isCursor=0), 200


@app.route('/list/<strategy>')
def listTrades(strategy):
    tout = list()
    trades = tradeDb[strategy].find(
        filter={}
    )
    for t in trades:
        t['total'] *= config.mdMultipliers[strategy]
        tout.append(t)
    return jsonWrapper(tout, isCursor=0), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

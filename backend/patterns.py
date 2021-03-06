from __future__ import division
import cgitb
from bs4 import BeautifulSoup
import operator
import pymongo
from flask import Flask, json, Response, request
from flask_cors import CORS
import os
import arrow
import mdcore
import gradients
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


def pipsToDollars(strategy, pips):
    return (pips * config.mdMultipliers[strategy]) - config.mdFees[strategy]


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


@app.route('/list/<strategy>/<theme>')
def listTrades(strategy, theme):
    tout = list()
    trades = list(tradeDb[strategy].find(
        filter={}
    ))
    maxt = pipsToDollars(strategy, max([t['total'] for t in trades]))
    mint = pipsToDollars(strategy, min([t['total'] for t in trades]))
    for t in trades:
        t['total'] = pipsToDollars(strategy, t['total'])
        t['datetime'] = arrow.get(
            t['date'] + ' 2016 ' + t['entryTime'],
            'MMM D YYYY H:mm'
        ).timestamp
        t['color'] = gradients.findColor(mint, maxt, t['total'], theme)
        tout.append(t)
    return jsonWrapper(sorted(tout, key=lambda x: x['datetime']),
                       isCursor=0), 200


@app.route('/oapl/<strategy>/<theme>')
def listOapl(strategy, theme):
    retlist = list()
    retlist.append(
        {
            "date": "Jul 11",
            "total": 0,
        }
    )
    trades = list(tradeDb[strategy].find(
        filter={}
    ))
    for t in trades:
        t['datetime'] = arrow.get(
            t['date'] + ' 2016 ' + t['entryTime'],
            'MMM D YYYY H:mm'
        ).timestamp
    trades = sorted(trades, key=lambda x: x['datetime'])
    for t in trades:
        found = 0
        t['total'] = pipsToDollars(strategy, t['total'])
        for i, day in enumerate(retlist):
            if day['date'] == t['date']:
                retlist[i]['total'] += t['total']
                found = 1
                break
        if found == 0:
            retlist.append(
                {
                    "date": t['date'],
                    "total": t['total'] + retlist[-1]['total'],
                }
            )
    maxt = max([d['total'] for d in retlist])
    mint = min([d['total'] for d in retlist])
    for day in retlist:
        day['color'] = gradients.findColor(mint, maxt, day['total'], theme)
    return jsonWrapper(retlist, isCursor=0), 200


@app.route('/totals/<strategy>/<theme>')
def genTotals(strategy, theme):
    totals = dict()
    trades = list(tradeDb[strategy].find(
        filter={}
    ))
    for t in trades:
        t['total'] = pipsToDollars(strategy, t['total'])
    wintrades = [x for x in trades if x['total'] > 0]
    wins = [x['total'] for x in wintrades]
    losetrades = [x for x in trades if x['total'] <= 0]
    loses = [x['total'] for x in losetrades]
    shorts = [x for x in trades if x['direction'] == "Short"]
    longs = [x for x in trades if x['direction'] == "Long"]
    shortwins = [x for x in shorts if x in wintrades]
    longwins = [x for x in longs if x in wintrades]
    totals['won'] = [len(wins), "none"]
    totals['lost'] = [len(loses), "none"]
    best = max([x['total'] for x in trades])
    totals['best'] = [best, gradients.findColor(-150, 300, best, theme)]
    worst = min([x['total'] for x in trades])
    totals['worst'] = [abs(worst), gradients.findColor(
        -150, 300, worst, theme)]
    avgwin = sum(wins) / len(wins)
    totals['avgwin'] = [int(avgwin), gradients.findColor(
        worst, best, avgwin, theme)]
    avgloss = sum(loses) / len(loses)
    totals['avgloss'] = [abs(int(avgloss)), gradients.findColor(
        worst, best, avgloss, theme)]
    shortwr = len(shortwins) / len(shorts)
    totals['shortwr'] = [int(shortwr * 100), gradients.findColor(
        0, 1, shortwr, theme)]
    longwr = len(longwins) / len(longs)
    totals['longwr'] = [int(longwr * 100), gradients.findColor(
        0, 1, longwr, theme)]
    winrate = len(wins) / len(trades)
    totals['winrate'] = [int(winrate * 100), gradients.findColor(
        0, 1, winrate, theme)]
    roi = int(((sum(wins) + sum(loses)) / 2500) * 100)
    totals['roi'] = [roi, gradients.findColor(0, 100, roi, theme)]
    rredge = int(avgwin + avgloss)
    totals['rredge'] = [rredge, gradients.findColor(
        worst, best, rredge, theme)]
    expect = int(winrate * avgwin + ((1 - winrate) * avgloss))
    totals['expect'] = [expect, gradients.findColor(
        avgloss, avgwin, expect, theme)]
    monthly = int(expect * 5 * 4)
    totals['monthly'] = [monthly, gradients.findColor(
        -500, 1500, monthly, theme)]
    balance = int(2500 + sum(wins) + sum(loses))
    totals['balance'] = [balance, gradients.findColor(
        0, 5000, balance, theme)]
    return jsonWrapper(totals, isCursor=0), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

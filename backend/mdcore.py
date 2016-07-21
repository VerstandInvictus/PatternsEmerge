import codecs
import datetime
import config
import requests
import cookielib
import mechanize
import re
import os
import unidecode
import hashlib
import urllib2
from werkzeug import urls
from bs4 import BeautifulSoup
from math import ceil
import pprint
from time import sleep

user_agent = (
    'User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')


class mdLogger:
    def __init__(self, logfile):
        self.logfile = logfile

    def logEntry(self, entry, level):
        with codecs.open(self.logfile, mode='a', encoding='utf-8') as log:
            log.write(entry + '\n')
        if 'progress' in level:
            print unidecode.unidecode(entry)


class marketdelta:
    def __init__(self, logobj):
        self.logger = logobj
        self.user = config.mdUser
        self.password = config.mdPass
        self.br = self.loginToMD()

    def loginToMD(self):
        br = mechanize.Browser(factory=mechanize.RobustFactory())
        br.set_handle_robots(False)
        br.addheaders = [user_agent]
        resp = br.open("https://app.marketdelta.com/signon")
        br._factory.is_html = True
        br.select_form(nr=0)
        br.form['email'] = self.user
        br.form['password'] = self.password
        br.submit()
        print "logged in"
        return br

    def readPage(self):
        self.br.open('https://app.marketdelta.com/trading')
        soup = BeautifulSoup(self.br.response().read())
        return soup

if __name__ == "__main__":
    logger = mdLogger('junk.log')
    md = marketdelta(logger)
    soup = md.readPage()
    pprint.pprint(soup)

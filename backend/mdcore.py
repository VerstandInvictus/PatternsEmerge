import codecs
import config
import unidecode
from pyvirtualdisplay import Display
from time import sleep
from selenium import webdriver, common

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36' \
             ' (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'


class mdLogger:
    def __init__(self, logfile):
        self.logfile = logfile

    def logEntry(self, entry, level):
        with codecs.open(self.logfile, mode='a+', encoding='utf-8') as log:
            log.write(entry + '\n')
        if 'progress' in level:
            print unidecode.unidecode(entry)


class marketdelta:
    def __init__(self, logobj, strategy):
        self.logger = logobj
        self.user = config.mdUsers[strategy]
        self.password = config.mdPasses[strategy]
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.profile = webdriver.FirefoxProfile()
        self.br = self.loginToMD()

    def loginToMD(self):
        self.profile.set_preference("general.useragent.override", user_agent)
        browser = webdriver.Firefox(self.profile)
        browser.implicitly_wait(15)
        browser.get('https://app.marketdelta.com/signon')
        emailfield = browser.find_element_by_id('email')
        emailfield.send_keys(self.user)
        pwfield = browser.find_element_by_name('password')
        pwfield.send_keys(self.password)
        submitbutton = browser.find_element_by_xpath(
            '//*[@id="frame-content"]/form/div[3]/div/input')
        submitbutton.click()
        sleep(15)  # give it time to load the order list
        self.logger.logEntry("Logged in successfully", 'info')
        return browser

    def getOrderList(self):
        try:
            orderlist = self.br.find_element_by_class_name('watchlist')
            otable = orderlist.get_attribute('innerHTML')
            self.logger.logEntry("Got order list", 'info')
        except common.exceptions.UnexpectedAlertPresentException:
            self.logger.logEntry('No orders to get', 'info')
            otable = "<th></th><tr><td></td></tr>"
        return otable

    def exit(self):
        self.br.quit()
        self.display.stop()
        self.logger.logEntry("Quit FF and Xvfb", 'info')

if __name__ == '__main__':
    exit()

from bs4 import BeautifulSoup
from slackclient import SlackClient
from random import randint
from operator import itemgetter
from datetime import datetime

import json
with open("config.json") as ifile:
    settings = json.load(ifile)
TOKEN = settings["slack-token"]
MAIN = settings["main-channel"]
ERROR = settings["error-channel"]
STATUS = settings["status-channel"]

class AmazonLookup():

    def __init__(self,asin,prime,price,single):
        self.single = single
        self.metadata=[]
        self.asin = asin
        self.lprice = 0
        self.flag = 0
        self.count=0
        self.msgcount=0
        self.prime=prime
        if price:
            self.a_price = float(price)
        if prime:
            self.stat_url = "https://www.amazon.in/gp/offer-listing/" + asin + "/ref=olp_prime_new?ie=UTF8&condition=new&shipPromoFilter=1"
        else:
            self.stat_url = "https://www.amazon.in/gp/offer-listing/" + asin + "/ref=olp_tab_new?ie=UTF8&condition=new"
        global TOKEN
        self.sc = SlackClient(TOKEN)

    def setHeader(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
                          + str(randint(0, 10)) + '_' + str(randint(10, 20)) +
                          '_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          + str(randint(20, 70)) + '.0.2171.95 Safari/537.36'}

    def bfInfo(self,par):
        try:
            if len(self.metadata)>0:
                if par:
                    text = '[' + str(self.metadata[0][0]) + '] ' + '[' + str(self.metadata[0][1]) + '] ' + " ".join(self.title.split(" ")[:4]) + self.stat_url
                else:
                    if self.prime:
                        text = str(self.count)+" "+str(self.msgcount)+" "+'[' + str(self.metadata[0][0]) + '] '+'[ PRIME ] ' + '[' + "".join(self.metadata[0][1]) + '] ' + " ".join(self.title.split(" ")[:4])
                    else:
                        text = str(self.count)+" "+str(self.msgcount)+" "+'[' + str(self.metadata[0][0]) + '] ' + '[' + "".join(self.metadata[0][1]) + '] ' + " ".join(self.title.split(" ")[:4])
                return text
            return str(self.count)+" "+str(self.msgcount)+" "+'[ NOT IN STOCK ] ' + " ".join(self.title.split(" ")[:4])
        except Exception as e:
            return "Either Asin is wrong or you are being blocked by amazon"


    def setPrice(self,price):
        self.a_price = price

    def clearFlag(self):
        self.flag = 0

    def sendAlert(self,status=False,error=None):
        global ERROR,MAIN
        if(status):
            stat_string = str(datetime.now())+" "+self.bfInfo(True)
            self.sc.api_call('chat.postMessage', channel='#'+str(STATUS),
                                      text=stat_string, username='zen',
                                      icon_emoji=':robot_face:')
        else:
            try:
                if (error != None):
                    self.sc.api_call('chat.postMessage', channel='#'+str(ERROR),
                                          text=error, username='zen',
                                          icon_emoji=':robot_face:')
                elif self.flag == 0:
                    self.sc.api_call('chat.postMessage', channel='#'+str(MAIN),
                                          text=self.bfInfo(True), username='zen',
                                          icon_emoji=':robot_face:')
                    self.msgcount+=1
                    if(self.single):
                        self.flag = 1

            except Exception as e:
                pass
            return

    def check(self):
        if(datetime.now().minute%60==0):
            self.sendAlert(True)
        if self.a_price==None:
            if len(self.sellers) != 0:
                if len(self.metadata) != 0:
                    self.sendAlert()
                    return True
                else:
                    self.flag = 0
                    return False
        else:
            if len(self.sellers) != 0:
                if self.lprice <= self.a_price:
                    self.sendAlert()
                    return True
                else:
                    self.flag = 0
                    return False
            else:
                return False

    def getInfo(self,response):
        try:
            done = True
            self.metadata=[]
            while done:
                    soup = BeautifulSoup(response.content, "html5lib")
                    self.sellers = soup.findAll("div", {'class': 'a-row a-spacing-mini olpOffer'})
                    self.title = soup.findAll("h1", {'class': 'a-size-large a-spacing-none'})[0].contents[-1].strip(" ")
                    for elem in self.sellers:
                        pric = elem.find_all('span', {'style': 'text-decoration: inherit; white-space: nowrap;'})[0].contents[-1].replace(",", "")
                        sel = elem.find_all('h3', {'class': 'a-spacing-none olpSellerName'})[0].contents[-2].contents[-2].contents[0]
                        self.metadata.append((float(pric), sel))
                    self.metadata = sorted(self.metadata, key=itemgetter(0))
                    if len(self.metadata)>0:
                        self.lprice = self.metadata[0][0]
                        self.lseller = self.metadata[0][1]
                    self.count += 1
                    done = False
        except Exception as e:
            self.sendAlert(status=False,error=e)

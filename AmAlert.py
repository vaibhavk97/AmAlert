from scraper import AmazonLookup
import time
from requests_futures.sessions import FuturesSession
import json
from random import randint

with open("config.json") as ifile:
    settings = json.load(ifile)
delay = settings["fail-delay"]
num_work = settings["workers"]
session = FuturesSession(max_workers=num_work)

print("""

  ______   __       __   ______   __        ________  _______  ________ 
 /      \ |  \     /  \ /      \ |  \      |        \|       \|        
|  $$$$$$\| $$\   /  $$|  $$$$$$\| $$      | $$$$$$$$| $$$$$$$\$$$$$$$$
| $$__| $$| $$$\ /  $$$| $$__| $$| $$      | $$__    | $$__| $$  | $$   
| $$    $$| $$$$\  $$$$| $$    $$| $$      | $$  \   | $$    $$  | $$   
| $$$$$$$$| $$\$$ $$ $$| $$$$$$$$| $$      | $$$$$   | $$$$$$$\  | $$   
| $$  | $$| $$ \$$$| $$| $$  | $$| $$_____ | $$_____ | $$  | $$  | $$   
| $$  | $$| $$  \$ | $$| $$  | $$| $$     \| $$     \| $$  | $$  | $$   
 \$$   \$$ \$$      \$$ \$$   \$$ \$$$$$$$$ \$$$$$$$$ \$$   \$$   \$$   

                            AMAZON ALERT SYSTEM
""")

count = 1

def setHeader():
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
                      + str(randint(0, 10)) + '_' + str(randint(10, 20)) +
                      '_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                      + str(randint(20, 70)) + '.0.2171.95 Safari/537.36'}
    return header['User-Agent']


def loadfile():
    with open("data.json") as datfile:
        datadict = json.load(datfile)
    return datadict

def updatedata():
    global count
    dataframe = []
    chead = {'User-Agent': setHeader(), 'Accept': '*/*', 'Accept-Language': 'en-GB,en;q=0.5',
                     'Accept-Encoding': 'gzip, deflate', 'Connection': 'close'}
    for elem in products:
        dataframe.append(session.get(elem.stat_url,headers=chead))
    for i,elem in enumerate(products):
        print("                           No of requests sent : "+str(count), end="\r")
        count += 1
        elem.getInfo(dataframe[i].result())

def main():
    global products
    products = []
    prod_dict = loadfile()
    for elem in (prod_dict.keys()):
        data = prod_dict[elem]
        if (data["alert_price"]):
            products.append(AmazonLookup(elem, data["check_prime"], data["alert_price"], bool(data["single_alert"])))
        else:
            products.append(AmazonLookup(elem, data["check_prime"], None, bool(data["single_alert"])))
    with open("output.txt","w") as ofile:
        while True:
            updatedata()
            ofile.seek(0)
            ofile.truncate()
            for elem in products:
                elem.check()
                ofile.write(elem.bfInfo(False)+"\n")
            ofile.flush()
            time.sleep(delay)

if __name__ == "__main__":
    main()




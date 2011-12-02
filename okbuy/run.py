#!/usr/bin/python
import urllib2,sgmllib,string,re,json 
from datetime import datetime
from config import *
from common.mongo import CPriceTrendDao
#from common.common import *

class OkbuyParser(sgmllib.SGMLParser):
    "customized letao listpage parser"
    def parse(self, s):
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.commodities = []
        self.url = ""
        self.price = ""
    
    def start_b(self, attributes):
        for name, value in attributes:
            if name == "productid":
                self.commodities.append(value)

    def end_b(self):
        return

    def get_commodities(self):
        data = urllib2.urlopen("http://www.okbuy.com/product/ajax_find_listprice/%s" % (','.join(self.commodities))).read()
        res = json.loads(data)
        return res 
#http://www.okbuy.com/product/search?&per_page=1
def parse_page(url, identifier = "default"):
    try:
        page = urllib2.urlopen(url).read()
        okbuyparser = OkbuyParser()
        okbuyparser.parse(page)
        print "page[%s, %d]" % (url, len(okbuyparser.get_commodities()))
        res = okbuyparser.get_commodities()
        for key, value in res.items():
            #CPriceTrendDao.insert(md5sum(url), url, int(string.atof(value)*100), datetime.now(), "okbuy")
            CPriceTrendDao.insert(int(key),  int(string.atof(value)*100), datetime.now(), "okbuy")
    except BaseException as e:
        print e
        log.error(e)
        return

def start():
    i = 0
    while i < settings["page_num"]:
        parse_page("http://www.okbuy.com/product/search?&per_page=%d" % (i*100))
        i += 1

#start()
if __name__ == '__main__':
    parse_page("http://www.okbuy.com/product/search?&per_page=0")

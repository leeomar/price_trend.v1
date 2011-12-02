#!/usr/bin/python
import urllib2, sgmllib, string, re 
from datetime import datetime
from config import *
from common.mongo import CPriceTrendDao

class LetaoParser(sgmllib.SGMLParser):
    "customized letao listpage parser"
    def parse(self, s):
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.commodities = []
        self.inside_prodlist = 0
        self.inside_item = 0
        self.inside_pinfo = 0
        self.url = ""
        self.price = ""
    
    def start_div(self, attributes):
        for name, value in attributes:
            if name == "id" and value == "prodlist":
                self.inside_prodlist = 1

    def end_div(self):
        self.inside_prodlist = 0

    def start_a(self, attributes):
        if self.inside_prodlist:
            for name, value in attributes:
                if name == "href":
                    self.url = "%s%s" % (settings['basic_url'], re.match("^/[\w|-]+", value).group(0))
                    #self.url = "%s%s" % (settings['basic_url'], value)
                    self.inside_item = 1

    def end_a(self):
        self.inside_item = 0

    def start_i(self, attributes):
        if self.inside_prodlist and self.inside_item:
            for name, value in attributes:
                if name == "class" and value == "ltprice":
                    self.inside_pinfo = 1
    
    def end_i(self):
        self.inside_pinfo = 0

    def handle_data(self, data):
        if self.inside_pinfo:
            self.price = int(string.atof(''.join(re.findall('(\d+)', data)))*100)
            self.commodities.append((self.url, self.price))

    def get_commodities(self):
        return self.commodities

# http://www.letao.com/shoe-p259
def parse_page(url, identifier = "default"):
    try:
        page = urllib2.urlopen(url).read()
        letaoparser = LetaoParser()
        letaoparser.parse(page)
        print "page[%s, %d]" % (url, len(letaoparser.get_commodities()))
        for item in letaoparser.get_commodities():
            #CPriceTrendDao.insert(md5sum(item[0]), item[0], item[1], datetime.now(), "letao")
            r = re.search('-(\d+)-', item[0])
            CPriceTrendDao.insert(int(r.group(1)), item[1],  datetime.now(), "letao")
    except BaseException as e:
        #print e
        log.error(e)
        return

def start():
    i = 0
    while i < settings["page_num"]:
        parse_page("http://www.letao.com/shoe-p%d" % i)
        i += 1

if __name__ == '__main__':
    parse_page("http://www.letao.com/shoe-p8")
#start()

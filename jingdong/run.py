#/usr/bin/python2
from datetime import datetime
import urllib, urllib2, re, os, threading, string
from common.mongo import CPriceTrendDao
# from common.common import *
from config import *

def categorylist(url):
    res = urllib2.Request(url)
    s = urllib2.urlopen(res).read()
    url_list = re.findall('products/(\d+-\d+-(\d+)).html', s)
    
    l = [i[0] for i in url_list if not re.match('0+', i[1])]
    category_num = len(l)
    num_per_worker = len(l) / settings['thread_num']

    #multi thread 
    threads = []
    start = 0
    i = 0
    while start < category_num:
        end = start + num_per_worker
        if end > category_num:
            end = category_num
        
        threads.append(threading.Thread(target=workthread, args=(l[start:end], "worker_%d" % i)))
        start = end
        i += 1 

    log.info("start %d worker" % i)
    #start all thread
    for t in threads:
        t.start()

    #wait all subthread
    for t in threads:
        t.join()
 
    log.info("main work done")

def workthread(categorys, identifier="default_worker"):
    for item in categorys:
        itemlist(item, identifier)
    log.info("%s process %d categorys" % (identifier, len(categorys)))

def itemlist(category, identifier="default_worker"):
    item_basic_url = '%s/products/%s-0-0-0-0-0-0-0-1-1-%s' % (settings['url_domain'], category, '%d.html')
    i = 1
    while True:
        u = item_basic_url % i
        try:
            res = urllib2.Request(u)
            s = urllib2.urlopen(res).read()
        except:
            #@TODO consider end conditions
            log.debug("%s, fail fetch [%s]" % (identifier, u))
            i += 1
            continue

        l = re.findall('<li sku=\'(\d+)\' onclick', s)
        if 0 == len(l):
            log.warn("%s, fail get any sku from [%s]" % (identifier, u))
            break
        else:
            i +=1
            for ii in l:
                getprice(ii, identifier)
            log.info("%s, get %d sku from [%s]" % (identifier, len(l), u))
    log.info("%s done" % identifier)

def getprice(item, identifier="default_worker"):
    try:
        t1 = datetime.now()
        url = 'http://price.360buyimg.com/gp%s,3.png' % item.strip()
        data = urllib2.urlopen(url).read()
        tmp_file = "%s%s.tmp.png" % (settings['tmp_png_path'], identifier)
        f = file(tmp_file, "wb")
        f.write(data)
        f.close()

        t2 = datetime.now()
        log.info("%s, download %s, used %s" % (identifier, url, str(t2 - t1)))
        t1 = t2

        s = os.popen('gocr %s' % tmp_file).read()
        ss = re.sub('o', '0', s)
        price = re.findall('(\d+)', ss)
        t2 = datetime.now()
        log.info("%s, getprice used %s" % (identifier, str(t2-t1)))    

        #save to mongo
        comm_url = settings['comm_basic_url'] % item
        price = int(string.atof(''.join(price)))
        #CPriceTrendDao.insert(md5sum(comm_url), comm_url, price, datetime.now(), "360buy")
        CPriceTrendDao.insert(int(item), price, datetime.now(), '360buy')
        return price
    except BaseException as e:
        #print e 
        log.warn("%s %s" % (identifier, e))
        return '0' 

def start():
    categorylist(settings['basic_url'])
    print 'DONE'

if __name__ == '__main__':
    getprice('516026')

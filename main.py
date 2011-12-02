#! /usr/bin/python

import sys, getopt
from jingdong.run import start as start_jingdong
from letao.run import start as start_letao
from okbuy.run import start as start_okbuy

def usage():
    print "Usage: --[help|site] [site_idenfier]"
    print "\t--help: print help information"
    print "\t-s, --site [site_idenfier]"
    print "\t\tletao : downloads letao"
    print "\t\t360buy: downloads 360buy"
    print "\t\tokbuy : downloads okbuy"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(2)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:",\
            ["help", "site"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    cmd = None
    for o, a in opts:
        if o == "--help":
            usage()
            sys.exit()
        if o in ("-s", "--site"):
            cmd = a 
    if cmd not in ['360buy', 'letao', 'okbuy']:
        print 'illeage param: ', cmd 
        usage()
        sys.exit()
    
    reload(sys)
    sys.setdefaultencoding('utf-8')

    lf = {  '360buy': lambda: start_jingdong,
            'letao' : lambda: start_letao,
            'okbuy' : lambda: start_okbuy,}
    lf[cmd]()()

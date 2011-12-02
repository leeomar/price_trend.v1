#/usr/bin/python2
# -*- coding: utf-8 -*-
import logging, os

settings = { 
    'basic_url' :   'http://www.360buy.com/allSort.aspx',
    'url_domain':   'http://www.360buy.com',
    'comm_basic_url'    :   'http://www.360buy.com/product/%s.html',
    'tmp_png_path'      :   '/tmp/',
    'thread_num' : 3,
}

# logger config
log_file = "log/360buy_log"
log = logging.getLogger()
hdlr = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
log.addHandler(hdlr)
log.setLevel(logging.DEBUG)

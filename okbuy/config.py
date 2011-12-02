#/usr/bin/python2
# -*- coding: utf-8 -*-
import logging, os
settings = {
    'basic_url'     :   'http://www.okbuy.com',
    'thread_num'    :   3,
    'page_num'      :   210, 
}

# logger config
log_file = "log/okbuy_log"
log = logging.getLogger()
hdlr = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
log.addHandler(hdlr)
log.setLevel(logging.DEBUG)

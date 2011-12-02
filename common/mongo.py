#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo.connection import Connection
from pymongo import objectid
from datetime import datetime
import string

client = Connection('127.0.0.1', 27017).price_trend_db
dbs = {
    '360buy': [client.price_360buy, client.price_360buy_all],
    'okbuy': [client.price_okbuy, client.price_okbuy_all],
    'letao': [client.price_letao, client.price_letao_all],
}
class CPriceTrendDao:
    @staticmethod
    #def insert(key, url, price, insert_time, shop):
    def insert(key, price, insert_time, shop):
        if not dbs.has_key(shop):
            return 'error'
        db = dbs[shop][0]
        db_all =  dbs[shop][1]
        #obj = db.price_trend.find_one({'key': key})
        obj = db.find_one({'key': key})
        if obj is not None:
            price_item = {'price': price, 'datetime': insert_time}
            db.update({'key': key}, {'$push': {'data' : price_item}}, upsert = True)
            db_all.update({'key': key}, {'$push': {'data' : price_item}}, upsert = True)
        else:
            item = {'key': key, 'data': [{'price': price, 'datetime': insert_time}], 'shop': shop}
            db.insert(item)
            db_all.insert(item)
    
    @staticmethod    
    def query(key):    
        return db.price_trend.find_one({'key': key})         

    @staticmethod
    def clear(remainRecordNum):
        '''
            数据清理定期进行, 清理2类数据:
            1. 时间大于指定时间, 默认30天
            2. 清理过于密集的点, 历史价格无变化,持平的话,只需要保留2个时间点
            3. 价格历史默认保留10个点
            @todo:优化查询 
        '''
        curTime = datetime.now()
        all_commodity = db.price_trend.find()
        print all_commodity.count()
        for item in all_commodity:
            print item
            i = len(item['data']) - 1
            result = []
            result_num = 0
            while i >= 0:
                '''保留最近的5个点 + 历史3个点'''
                if result_num > 8:
                    break
                if result_num < 5:
                    print i, result_num
                    result.insert(0, item['data'][i])    
                    result_num += 1
                else:
                    '''合并价格'''    
                    if item['data'][i]['price'] != result[0]['price']: 
                        result.insert(0, item['data'][i])
                        result_num += 1
                    elif i > 0 and item['data'][i-1]['price'] != item['data'][i]['price']:
                        result.insert(0, item['data'][i])
                        result_num += 1
                i -= 1
            del item['data'][:]
            item['data'] = result
            db.price_trend.update({'_id': item['_id']}, item)

    @staticmethod
    def update_jingdong():
        k = 1
        all_commodity = db.price_trend.find()
        for item in all_commodity:
            item['shop'] = '360buy'
            data = []
            #print item
            for i in item['data']:
                try:
                    data.append({'price': int(string.atof(i['price'])), 'datetime': i['datetime'] })
                except BaseException as e:
                    print e
                    continue
            item['data'] = data
            #print item
            db.price_trend.update({'_id': item['_id']}, item)
            k += 1
        print k 
 
if __name__ == '__main__':
    CPriceTrendDao.insert('12345', '55400', datetime.now(), 'okbuy')

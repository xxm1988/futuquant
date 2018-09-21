#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created by cmathxcai
# import talib
import time
import math
import datetime
import os
import sys

import numpy as np
import pandas as pd
from futuquant import OpenQuoteContext
from futuquant import *

# from futuquant import OpenHKTradeContext, OpenUSTradeContext

# result_f = '../data/result/anxin_result'
# result_fp = open(result_f, 'w')

def get_filesize(file_path):
    # file_path = str(file_path, 'utf-8')
    fsize = os.path.getsize(file_path)
    fsize = fsize / float(1024)
    return round(fsize,2)

class Stock(object):
    """
    A simple MACD strategy
    """
    # API parameter setting
    # api_svr_ip = '119.29.141.202'   # 账户登录的牛牛客户端PC的IP, 本机默认为127.0.0.1
    # api_svr_ip = '10.27.11.57'
    # api_svr_port = 11111            # 富途牛牛端口，默认为11111Cai19900925.cai

    def __init__(self, svr_ip, svr_port):
        """
        Constructor
        """
        self.quote_ctx = OpenQuoteContext(host=svr_ip, port=svr_port)

    # def strategy(self, price_data):
    #     global w_fp
    #     for i in xrange(40, len(price_data)):
    #         ratio = (price_data[i][3] - price_data[i - 40][3]) / price_data[i - 40][3]
    #         if ratio <= -0.35:
    #             result_fp.write('[%s]%.4f\t[%s]%.4f\t%.4f, ' %(price_data[i - 40][1].split(' ')[0], price_data[i - 40][3], price_data[i][1].split(' ')[0], price_data[i][3], ratio))
    #             return True
    #     return False

    def parse_stock_data(self, stock, database_f, start_day, ktype):
        """
        handle stock data for trading signal, and make order
        """
        # global result_fp
        self.stock = stock
        self.database_f = database_f
        # 读取历史数据，使用sma方式计算均线准确度和数据长度无关，但是在使用ema方式计算均线时建议将历史数据窗口适当放大，结果会更加准确
        # today = datetime.datetime.today()
        # pre_day = (today - datetime.timedelta(days=self.observation)).strftime('%Y-%m-%d')
        # _, prices = self.quote_ctx.get_history_kline(self.stock, start=start_day, end=end_day, ktype=ktype, autype='qfq')#qfq,hfq,none
        # _, prices = self.quote_ctx.get_history_kline(self.stock, start=start_day, ktype=ktype, autype='AuType.QFQ')  # qfq,hfq,none
        import datetime
        starttime = datetime.datetime.now()
        _, prices = self.quote_ctx.get_history_kline(self.stock, '2000-01-01', '2018-09-13', KLType.K_DAY, AuType.QFQ)
        endtime = datetime.datetime.now()
        print((endtime - starttime).seconds)
        # print list(prices)
        # try:
            # print prices
            # prices = prices.drop_duplicates(['time_key'])
            # if self.strategy(prices.as_matrix()):
            #     result_fp.write('rubbish stock:%s\n' %stock)
            # print type(prices)
        # print(prices)
        # print(prices.as_matrix())
        try:
            pd.DataFrame(prices).to_csv(self.database_f, sep='\t')
        except:
            sys.stderr.write('stock[%s] is delisting.\n' %self.stock)
            sys.stderr.write(prices)

if __name__ == "__main__":
    qqq_list = ['.IXIC', 'QQQ', 'AAPL', 'AMZN', 'MSFT', 'GOOGL', 'FB', 'CSCO', 'INTC', 'CMCSA', 'NVDA', 'PEP', 'NFLX', 'AMGN', 'ADBE',
                'TXN']
    dji_list = ['.DJI', 'DIA', 'BA', 'UNH', 'GS', 'AAPL', 'MSFT', 'MMM', 'HD', 'MCD', 'IBM', 'V', 'CAT', 'JNJ', 'UTX', 'TRV', 'CVX',
                'JPM', 'NKE', 'AXP', 'WMT', 'WBA', 'KO', 'V', 'PG', 'VZ', 'DWDP', 'CSCO', 'XOM', 'MRK', 'DIS', 'PFE']
    spy_100_list = ['.INX', 'SPY', 'AAPL', 'AMZN', 'MSFT', 'GOOGL', 'FB', 'JPM', 'JNJ', 'BRK.B', 'XOM', 'BAC', 'V', 'WMT', 'WFC', 'UNH',
                    'PFE', 'HD', 'T', 'VZ', 'MA', 'CVX', 'CSCO', 'INTC', 'PG', 'BA', 'KO', 'ORCL', 'MRK', 'C', 'NVDA',
                    'CMCSA', 'DIS', 'PEP', 'NFLX', 'ABBV', 'IBM', 'NKE', 'AMGN', 'MDT', 'ADBE', 'MCD', 'MMM', 'PM',
                    'HON', 'ABT', 'UNP', 'CRM', 'LLY', 'ACN', 'MO', 'GE', 'UTX', 'UPS', 'COST', 'PYPL', 'QCOM', 'TXN',
                    'AVGO', 'BMY', 'TMO', 'GILD', 'RAI', 'AXP', 'LMT', 'LOW', 'USB', 'GS', 'CAT', 'MS', 'FOXA', 'SLB',
                    'COP', 'FOX', 'NEE', 'TWX', 'CVS', 'BLK', 'SBUX', 'DHR', 'CHTR', 'EL', 'KHC', 'TJX', 'BIIB', 'SCHW',
                    'ANTM', 'WBA', 'BDX', 'PNC', 'EOG', 'FDX', 'AET', 'AMT', 'ADP', 'AGN', 'CSX', 'SYK', 'MDLZ', 'CB']

    # svr_ip = '10.27.11.160'
    # svr_ip = '10.96.209.47'
    svr_ip = '127.0.0.1'
    svr_port = 11111
    # # 1. get all stock info
    # quote_ctx = OpenQuoteContext(svr_ip, svr_port)
    # ret_code, ret_data = quote_ctx.get_stock_basicinfo('US', stock_type='STOCK')
    # print ret_data
    # print type(ret_data)
    # pd.DataFrame(ret_data).to_csv('../data/US/stock_info.US', sep='\t', encoding='utf-8')

    # # 2. get all plate info
    # quote_ctx = OpenQuoteContext(svr_ip, svr_port)
    # ret_code, ret_data = quote_ctx.get_plate_list('US', 'ALL')#'ALL', 'INDUSTRY', 'REGION', 'CONCEPT'
    # pd.DataFrame(ret_data).to_csv('../data/basic_info.us/plate.all.info', sep='\t', encoding='utf-8')

    # # 3. get all plate and stock info
    # quote_ctx = OpenQuoteContext(svr_ip, svr_port)
    # with open('../data/basic_info.us/plate.industry.info', 'r') as r_fp:
    #     lines = 0
    #     for line in r_fp:
    #         lines += 1
    #         if lines == 1:
    #             continue
    #         plate_code = line.split('\t')[1]
    #         ret_code, ret_data = quote_ctx.get_plate_stock(plate_code)
    #         try:
    #             time.sleep(5)
    #             pd.DataFrame(ret_data).to_csv('../data/basic_info.us/industry_stock/%s' %plate_code, sep='\t', encoding='utf-8')
    #         except:
    #             print ret_data
    #             sys.stderr.write('error occurs in %s\n' %plate_code)

    # stock_list = []
    # lines = 0
    # with open('../data/US/stock_info.US', 'r') as r_fp:
    #     for line in r_fp:
    #         lines += 1
    #         if lines == 1:
    #             continue
    #         stock_list.append(line.split('\t')[1])

    stock_list = qqq_list + dji_list + spy_100_list

    # # stock_list = ['SZ.000024']
    stock_info = Stock(svr_ip, svr_port)
    sys.stdout.write('all stocks:%d\n' %len(stock_list))
    cnt = 0
    for _stock in stock_list:
        # print _stock
        time.sleep(1)
        database_f = 'd:/tmp/US/%s.DAY' %_stock
        # file_size = get_filesize(database_f)
        # print(file_size)
        cnt += 1
        # sys.stdout.write('%d-st file size:%.2f\n' %(cnt, file_size))
        # if file_size <= 10:
        if not os.path.exists(database_f):
            print(_stock)
            stock_info.parse_stock_data("US." + _stock, database_f, '2000-01-01', 'K_DAY')
    # result_fp.close()
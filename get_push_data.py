# -*- coding: utf-8 -*-
"""
Examples for use the python functions: get push data
"""

import time
from datetime import datetime
from futuquant import *
from futuquant.examples.learn import check_all_get_push
from collect_stock import load_stock_code
import logging

#设置dataframe结构的显示------pandas display设置
# pd.set_option('display.height', 1000)
# pd.set_option('display.max_rows', None) # pandas.set_option() 可以设置pandas相关的参数，从而改变默认参数。 打印pandas数据事，默认是输出100行，多的话会输出....省略号。
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
# pd.set_option('colheader_justify', 'right') #value显示居右

class StockQuoteTest(StockQuoteHandlerBase):
    """
    获得报价推送数据
    """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(StockQuoteTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            logger.debug("StockQuoteTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("StockQuoteTest : %s" % content)
        return RET_OK, content


class CurKlineTest(CurKlineHandlerBase):
    """ kline push"""
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(CurKlineTest, self).on_recv_rsp(rsp_pb)
        if ret_code == RET_OK:
            print("CurKlineTest : %s\n" % content)
        return RET_OK, content


class RTDataTest(RTDataHandlerBase):
    """ 获取分时推送数据 """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(RTDataTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("RTDataTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("RTDataTest :%s \n" % content)
        return RET_OK, content


class TickerTest1(TickerHandlerBase):
    """ 获取逐笔推送数据 """

    def __init__(self):
        self.time_gap = 0
        self.has_set_time_gap = False

    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        now = time.time() * 1000
        ret_code, content = super(TickerTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("TickerTest: error, msg: %s" % content)
            return RET_ERROR, content

        # first_ticker_time = content.at[0, 'time']  # type: str
        first_ticker_time = int(content[0]['time'])  # type: int
        recv_time = int(content[0]['recv_time'])
        time_gap = now - first_ticker_time
        if not self.has_set_time_gap:
            self.time_gap = time_gap
            self.has_set_time_gap = True
            logger.info('time gap: {}'.format(self.time_gap))

        delay = time_gap - self.time_gap
        tick_delay = recv_time - first_ticker_time
        # print("TickerTest\n", content)
        logger.info('Get tick: ClientTime={}; TickTime={}; RecvTime={}; Delay={}; TickDelay={};'.format(now, first_ticker_time, recv_time, delay, tick_delay))
        return RET_OK, content

class TickerTest(TickerHandlerBase):
    """ 获取逐笔推送数据 """

    def __init__(self):
        self.time_gap = 0
        self.has_set_time_gap = False

    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        now = time.time() * 1000
        ret_code, content = super(TickerTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("TickerTest: error, msg: %s" % content)
            return RET_ERROR, content

        print("TickerTest\n", content)
        return RET_OK, content


class OrderBookTest(OrderBookHandlerBase):
    """ 获得摆盘推送数据 """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(OrderBookTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("OrderBookTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("OrderBookTest\n", content)
        return RET_OK, content


class BrokerTest(BrokerHandlerBase):
    """ 获取经纪队列推送数据 """
    def on_recv_rsp(self, rsp_str):
        """数据响应回调函数"""
        ret_code, content = super(BrokerTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("BrokerTest: error, msg: %s " % content)
            return RET_ERROR, content
        print("BrokerTest bid \n", content[0])
        print("BrokerTest ask \n", content[1])
        return RET_OK, content


# class HeartBeatTest(HeartBeatHandlerBase):
#     """ 心跳的推送 """
#     def on_recv_rsp(self, rsp_pb):
#         """数据响应回调函数"""
#         ret_code, time = super(HeartBeatTest, self).on_recv_rsp(rsp_pb)
#         if ret_code == RET_OK:
#             print("heart beat server time = ", time)
#         return ret_code, time


def test_rt(quote_ctx):
    handler = RTDataTest()
    # quote_ctx.set_handler(handler)
    code_list = ['US.OPNT']  # 'HK.02318']
    sub_type_list = [SubType.RT_DATA]  # SubType.BROKER]
    print(quote_ctx.subscribe(code_list, sub_type_list))
    print(quote_ctx.get_rt_data('US.OPNT'))
    # for code in code_list:
    #     for kltype in sub_type_list:
    #         err, data = quote_ctx.get_cur_kline(code, 1000, kltype, AuType.QFQ)
    #         print(code, kltype, err)
    #         print(data)

def test_kl(quote_ctx):
    code_list = ['HK.00700', 'SZ.002024', 'SZ.300676', 'SZ.000026']
    sub_type_list = [SubType.K_1M, SubType.RT_DATA]
    quote_ctx.set_handler(CurKlineTest())
    quote_ctx.set_handler(RTDataTest())
    print(quote_ctx.subscribe(code_list, sub_type_list))


def test_ticker(quote_ctx):
    # quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1',port=11111)
    # quote_ctx.start()
    # 设置异步数据监听
    handler = TickerTest()
    quote_ctx.set_handler(handler)
    codes = ['HK.00700'] # load_stock_code('stock1.csv')
    # quote_ctx._net_mgr._on_read(None)
    ret, data = quote_ctx.subscribe(codes[:500], SubType.TICKER)
    print('sub: ', ret, data)
    # for code in codes:
        # 订阅股票

        # 调用待测接口
        # ret_code, ret_data = quote_ctx.get_rt_ticker(code)
        # print(ret_code)
        # print(ret_data)

def test_trade_date(quote_ctx):
    err, data = quote_ctx.get_trading_days(Market.US, '2018-5-1', '2018-7-3');
    print(err)
    print(data)
    quote_ctx.close()


def test_hist_kl(quote_ctx):
    codes = ['HK.00700']
    dates = ['2019-12-1']
    fields = KL_FIELD.ALL_REAL
    kl_type = KLType.K_MON
    ex_right = AuType.QFQ
    no_data_mode = KLNoDataMode.BACKWARD
    err, data = quote_ctx.get_multi_points_history_kline(codes, dates, fields, kl_type, ex_right, no_data_mode)
    quote_ctx.close()
    print(err, data)
    
def test_quote(quote_ctx):
    codes = ['HK.800000']
    handler = StockQuoteTest()
    quote_ctx.set_handler(handler)
    quote_ctx.subscribe(codes, SubType.QUOTE)
    # ret, data = quote_ctx.get_stock_quote(codes[0])
    # print(ret, data)
    # err, data = quote_ctx.get_stock_quote(codes)
    # print(err)
    # print(data)


def run_once():
    import datetime
    import time

    run_time = datetime.time(8, 49)
    while True:
        now = datetime.datetime.now()
        if now.hour == run_time.hour and now.minute >= run_time.minute:
            break
        time.sleep(10)

    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.start()
    test_kl(quote_ctx)

def test_check_all_get_push():
    check_all_get_push.quote_test()


def test_sub_many(quote_ctx):
    handler = TickerTest()
    quote_ctx.set_handler(handler)
    ret, data = quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK)
    codes = [code for code in data['code']]
    ret, data = quote_ctx.subscribe(codes, SubType.TICKER)
    print(ret, data)

def test_user_code(quote_ctx):
    codes = ['HK.00700']
    quote_ctx.set_handler(StockQuoteTest())
    quote_ctx.set_handler(OrderBookTest())
    quote_ctx.subscribe(codes, [SubType.QUOTE, SubType.ORDER_BOOK])


if __name__ =="__main__":
    logger.setLevel(logging.DEBUG)
    SysConfig.set_all_thread_daemon(True)
    # run_once()
    # test_check_all_get_push()
    # sys.exit(0)
    # 实例化行情上下文对象
    # quote_ctx = OpenQuoteContext(host='193.112.189.131', port=12345)
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # print(quote_ctx.subscribe('US.AAPL', SubType.ORDER_BOOK))
    # quote_ctx = OpenQuoteContext(host='172.18.10.194', port=11211)
    # quote_ctx.set_handler(StockQuoteTest())
    # quote_ctx.set_handler(CurKlineTest())
    # quote_ctx.set_handler(RTDataTest())
    # quote_ctx.set_handler(TickerTest())
    # quote_ctx.set_handler(OrderBookTest())
    # quote_ctx.set_handler(BrokerTest())
    # quote_ctx.set_handler(HeartBeatTest())
    quote_ctx.start()
    # quote_ctx.close()
    # test_user_code(quote_ctx)
    # trd_ctx = OpenHKTradeContext(host='193.112.189.131', port=12345)
    # print(trd_ctx.get_acc_list())
    # test_sub_many(quote_ctx)
    # test_kl(quote_ctx)
    # test_quote(quote_ctx)
    # test_rt(quote_ctx)
    # test_ticker(quote_ctx)
    # time.sleep(5)
    # quote_ctx.close()
    # logger.debug('closed')

    # test_trade_date(quote_ctx)
    # test_hist_kl(quote_ctx)

    # 获取推送数据
    # print(quote_ctx.get_global_state())

    print(quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK))
    # print(quote_ctx.get_cur_kline('HK.00700', 10, SubType.K_DAY, AuType.QFQ))
    # print(quote_ctx.get_rt_data('HK.00700'))
    # print(quote_ctx.get_rt_ticker('HK.00700', 10))
    # print(quote_ctx.get_referencestock_list(1, SecurityReferenceType.NONE))

    # print(quote_ctx.get_stock_quote(['HK.00700']))
    # print(quote_ctx.query_subscription())
    # print(quote_ctx.get_broker_queue('HK.00700'))
    # print(quote_ctx.get_order_book('HK.00700'))
    # print(quote_ctx.get_history_kline('HK.917', start='2010-06-20', end='2017-06-22'))

    # print(quote_ctx.get_multiple_history_kline(['HK.00700'], '2017-06-20', '2017-06-25', KL_FIELD.ALL, KLType.K_DAY, AuType.QFQ))
    # print(quote_ctx.get_multi_points_history_kline(['HK.00700'], ['2017-06-21', '2017-06-25'], KL_FIELD.ALL))
    # print(quote_ctx.get_autype_list(["HK.00700"]))

    # print(quote_ctx.get_trading_days(Market.HK, '2018-11-01', '2018-11-20'))
    # print(quote_ctx.get_suspension_info(['SZ.300104'], '2010-02-01', '2018-05-20'))

    # print(quote_ctx.get_market_snapshot('HK.00839'))
    # print(quote_ctx.get_market_snapshot(code_list))

    # print(quote_ctx.get_plate_list(Market.HK, Plate.ALL))
    # print(quote_ctx.get_plate_stock('HK.BK1001'))

    # sleep(10)
    # quote_ctx.close()
    # trd_ctx.close()

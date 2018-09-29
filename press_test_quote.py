

from futuquant import *
import pandas as pd
import numpy as np
import os
import time
from time import sleep
import collect_stock


def test_tick(code_list, ip, host):

    quote_context = OpenQuoteContext(host=ip, port=host)
    quote_context.start()

    while True:
        ret, data = quote_context.subscribe(code_list, SubType.TICKER)
        if ret != RET_OK:
            print(data)
            break
        count = 0
        for x in code_list:
            print(quote_context.get_rt_ticker(x))
            count = count + 1
            if count >= 10:
                break
        sleep(2)
        quote_context.unsubscribe(code_list, SubType.TICKER)
        print("loop sub")
        sleep(2)
    quote_context.close()


def test_kline(code_list, ip, host):

    quote_context = OpenQuoteContext(host=ip, port=host)
    quote_context.start()

    while True:
        ret, data = quote_context.subscribe(code_list, SubType.K_DAY)
        if ret != RET_OK:
            print(data)
            break
        for x in code_list:
            print(quote_context.get_cur_kline(x, 1000))
        sleep(10)
        quote_context.unsubscribe(code_list, SubType.TICKER)
        break

    quote_context.close()


def test1():

    """
    for x in range(10):
        codes = code_list[int(x * sub_cout/10): int((x+1) * sub_cout/10)]

        ret, data = quote_context.subscribe(codes, SubType.K_DAY)
        if ret != RET_OK:
            print(data)
            sleep(3)

        print("loop: {}".format(x))
        sleep(3)
        for x in codes:
            print(quote_context.get_cur_kline(x, 1000))

    print(codes_error)
    """

class CurKlineTest(CurKlineHandlerBase):
    """ kline push"""
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(CurKlineTest, self).on_recv_rsp(rsp_pb)
        if ret_code == RET_OK:
            print("CurKlineTest : %s\n" % content)
        return RET_OK, content


class TickerTest(TickerHandlerBase):
    """ 获取逐笔推送数据 """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(TickerTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("TickerTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("TickerTest\n", content)
        return RET_OK, content

def test_sub():
    filename = time.strftime("%Y-%m-%d", time.localtime()) + '.csv'

    symbols = pd.read_csv('2018-06-06.csv', usecols=['code', 'name'])
    symbol_code = symbols['code'].values.tolist()
    symbol_name = symbols['name'].values.tolist()
    hk_symbols = collect_stock.load_stock_code('stock1.csv')
    sub_cout = 100
    # code_list = symbol_code[:sub_cout]
    code_list = hk_symbols[:sub_cout]
    # ip = "193.112.189.131"
    ip = "127.0.0.1"
    # host = 21112
    host = 21111
    # test_kline(code_list, ip , host)

    #################################################################
    quote_context = OpenQuoteContext(host=ip, port=host)
    count = 0
    while True:
        count += 1
        ret, data = quote_context.subscribe(code_list, [SubType.K_1M])
        print('Sub: ', ret, data, count)
        sleep(3)
        ret, data = quote_context.unsubscribe(code_list, [SubType.K_1M])
        print('Unsub: ', ret, data)
        sleep(2)



def main():

    filename = time.strftime("%Y-%m-%d", time.localtime()) + '.csv'
    symbols = pd.read_csv('2018-06-06.csv', usecols=['code', 'name'])
    symbol_code = symbols['code'].values.tolist()
    symbol_name = symbols['name'].values.tolist()


    sub_cout = 100
    code_list = symbol_code[0:sub_cout]
    hk_symbols = collect_stock.load_stock_code('stock1.csv')
    # ip = "193.112.189.131"
    ip = "127.0.0.1"
    port = 11111

    # test_kline(code_list, ip , host)

    #################################################################
    quote_context = OpenQuoteContext(host=ip, port=port)
    quote_context.set_handler(TickerTest())
    quote_context.set_handler(CurKlineTest())
    quote_context.start()
    codes_error = []
    ret, data = quote_context.subscribe(hk_symbols[:sub_cout], SubType.TICKER)
    print("sub: {} {}".format(ret, data))
    if ret != RET_OK:
        # print("code={} erro:{}".format(code, data))
        # codes_error.append(code)
        quote_context.close()
        #break
    # print("code= {} sub ret={} data={}".format(code, ret, data))
    # ret, data = quote_context.get_cur_kline(code, 1000, SubType.K_1M)
    # print("code= {} get ret={} data={}".format(code, ret, data))


if __name__ == "__main__":
    main()


# -*- coding: utf-8 -*-
from multiprocessing import freeze_support, Pool

from futuquant import *
import os
from app import quote_ctx

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

def test_rt(quote_ctx):
    handler = RTDataTest()
    quote_ctx.set_handler(handler)
    code_list = ['HK_FUTURE.999010']
    sub_type_list = [SubType.RT_DATA]
    print(quote_ctx.subscribe(code_list, sub_type_list))

def gk(i):
    a = quote_ctx.get_history_kline(i, start='2000-01-01', end='2018-08-03')
    if a[0] == -1:
        print(os.getpid(), i, 'no data', a[1])
    else:
        print(os.getpid(), i, 'ok', len(a[1]))


if __name__ == '__main__':
    sl = quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK)[1].code.tolist()
    # sl = ['HK.00002', 'HK.00181']
    print('total; ', len(sl))
    # freeze_support()
    test_rt(quote_ctx)
    pool = Pool(1)
    pool.map(gk, sl)
    pool.close()
    pool.join()

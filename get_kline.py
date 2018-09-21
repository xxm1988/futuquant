from futuquant import *
import logging
import time
import pandas

pandas.set_option('display.width', 1000)

class GetCurKline(object):
    #获取实时K线 get_cur_kline 和 CurKlineHandlerBase

    def test1(self):
        quote_ctx = OpenQuoteContext(host='127.0.0.1',port=11111)
        quote_ctx.start()
        # 设置异步数据监听
        handler = CurKlineTest()
        quote_ctx.set_handler(handler)
        #待测数据
        codes = ['HK.00939']    #'HK.00700', 'US.AAPL', 'SH.601318', 'SZ.000001'
        kTypes = [SubType.K_1M,SubType.K_DAY,SubType.K_15M,SubType.K_60M,SubType.K_WEEK, SubType.K_MON]  # [SubType.K_MON]
        # 订阅股票
        quote_ctx.subscribe(codes, kTypes)


class CurKlineTest(CurKlineHandlerBase):
    '''获取实时K线 get_cur_kline 和 CurKlineHandlerBase'''
    def on_recv_rsp(self, rsp_pb):
        # logger.info(rsp_pb)
        ret_code, ret_data = super(CurKlineTest, self).on_recv_rsp(rsp_pb)
        # 打印,记录日志
        logger.info('CurKlineTest')
        logger.info(ret_code)
        logger.info(ret_data)
        return RET_OK, ret_data

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    gck = GetCurKline()
    gck.test1()
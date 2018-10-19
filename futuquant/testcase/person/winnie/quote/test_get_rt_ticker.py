from futuquant import *
import pandas
import sys
import datetime
import unittest
import random

f = open('test_new_protocol.txt','a')

class GetTrTicker(unittest.TestCase):
    '''
    测试类:获取逐笔
    '''

    # 各类型股票获取逐笔的测试步骤和校验
    def step_check_base1(self, casename, code, num = random.randint(0,1000)):
        '''
        各市场各股票获取逐笔并校验是否正确
        :param casename:
        :param code:
        :param num:
        :return:
        '''
        ret_code_sub, ret_data_sub = quote_ctx.subscribe(code, SubType.TICKER)
        ret_code, ret_data = quote_ctx.get_rt_ticker(code, num)
        print(casename,file=f, flush=True)
        print(ret_data, file=f, flush=True)
        '''
        校验点：
        1、请求成功
        2、交易时间len(ret_data)>0
        3、返回的股票与code一致
        4、price >0
        5、volume、turnover>0
        6、sequence无重复项
        '''
        #校验点1、请求成功
        self.assertEqual(ret_code, RET_OK)
        #校验点6、sequence无重复项
        sequence_list = ret_data['sequence'].tolist()
        sequence_set = set(sequence_list)   #set自动去重
        self.assertEqual(len(sequence_list), len(sequence_set))

    #港股
    def test_get_rt_ticker_hk_stock(self):
        '''
        测试点：获取某一港股正股的逐笔
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK.01810'
        self.step_check_base1(casename,code)

    def test_get_rt_ticker_hk_wrt(self):
        '''
        测试点：获取某一港股涡轮的逐笔
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK.28552'
        self.step_check_base1(casename,code)

    def test_get_rt_ticker_hk_futrue(self):
        '''
        测试点：获取港股期货的逐笔
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK_FUTURE.999010'
        self.step_check_base1(casename,code)

    #美股
    def test_get_rt_ticker_us_stock(self):
        '''
        测试点：获取某一美股正股的逐笔
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'US.PDD'
        self.step_check_base1(casename, code)

    def test_get_rt_ticker_us_drvt(self):
        '''
        测试点：获取某一美股期权的逐笔
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'US.DIS181123P110000'
        self.step_check_base1(casename,code)

    #A股
    def test_get_rt_ticker_sh_stock(self):
        '''
        测试点：获取某一A股(SH)正股的报价
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'SH.603131'
        self.step_check_base1(casename, code)

    def test_get_rt_ticker_sz_stock(self):
        '''
        测试点：获取某一A股(SZ)正股的报价
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'SZ.300710'
        self.step_check_base1(casename, code)

    #code是无逐笔的股票，指数无逐笔
    def test_get_rt_ticker_idx(self):
        casename = sys._getframe().f_code.co_name
        code = 'HK.800000'
        num = 100
        ret_code_sub, ret_data_sub = quote_ctx.subscribe(code, SubType.TICKER)
        ret_code, ret_data = quote_ctx.get_rt_ticker(code, num)
        print(casename, file=f, flush=True)
        print(ret_data, file=f, flush=True)
        #校验
        self.assertEqual(ret_code, RET_OK)
        self.assertEqual(len(ret_data), 0)

    #入参错误步骤和校验
    def step_check_base2(self, casename, code, num = random.randint(0,1000)):
        # 执行步骤
        ret_code_sub, ret_data_sub = quote_ctx.subscribe(code, SubType.TICKER)
        ret_code, ret_data = quote_ctx.get_rt_ticker(code,num)
        print(ret_data, file=f, flush=True)
        # 校验
        self.assertEqual(ret_code, RET_ERROR)

    #code入参错误
    def test_get_rt_ticker_err_code(self):
        '''
        测试点：code入参错误
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = ['HK.00700']
        self.step_check_base2(casename, code)

    # num入参错误
    def test_get_rt_ticker_err_num(self):
        '''
        测试点：num入参错误
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK.00434'
        num = -2
        self.step_check_base2(casename,code,num)

    #code正确，但未执行订阅
    def test_get_rt_ticker_err_no_sub(self):
        '''
        测试点：未订阅
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'US.CI'
        #执行步骤
        ret_code, ret_data = quote_ctx.get_rt_ticker(code)
        print(ret_data, file=f, flush=True)
        #校验
        self.assertEqual(ret_code,RET_ERROR)


class AsyncTicker(unittest.TestCase):
    '''
    实时逐笔推送测试类
    '''

    def step_base(self, code_list, casename=sys._getframe().f_code.co_name ):
        '''
        基本测试步骤
        :param code_list:待订阅的股票代码列表
        :return:
        '''
        #打印日志：测试用例名
        print(casename, file=f, flush=True)
        #设置监听
        handler = TickerTest()
        quote_ctx.set_handler(handler)
        #订阅逐笔
        quote_ctx.subscribe(code_list, SubType.TICKER)

    def test_asyncTicker_hk_stock(self):
        #1、测试点：订阅港股正股实时逐笔
        self.step_base(code_list= ['HK.00700'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_hk_wrrant(self):
        # 1、测试点：订阅港股涡轮实时逐笔

        #获取涡轮代码
        codes_warrant = 'HK.28070'
        #执行测试步骤
        self.step_base(code_list=codes_warrant, casename=sys._getframe().f_code.co_name )

        # 2、校验
        # 不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_hk_future_stock(self):
        #1、测试点：订阅港股期货实时逐笔
        self.step_base(code_list= ['HK_FUTURE.999010'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_hk_idx(self):
        #1、测试点：订阅港股指数实时逐笔
        self.step_base(code_list= ['HK.800000'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_hk_etf(self):
        #1、测试点：订阅港股基金实时逐笔
        self.step_base(code_list= ['HK.02800'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_hk_bond(self):
        #1、测试点：订阅港股债券实时逐笔
        self.step_base(code_list= ['HK.04231'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_us_stock(self):
        #1、测试点：订阅美股正股实时逐笔
        self.step_base(code_list= ['US.AAPL'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_us_idx(self):
        #1、测试点：订阅美股指数实时逐笔
        self.step_base(code_list= ['US..IXIC'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_us_etf(self):
        #1、测试点：订阅美股指数实时逐笔
        self.step_base(code_list= ['US.YINN'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_us_drvt(self):
        #1、测试点：订阅美股期权实时逐笔

        #获取期权代码
        codes = []
        drvt_call_ret_code, drvt_call_ret_data = quote_ctx.get_option_chain(code='US.GOOG',
                                                                                 option_type=OptionType.CALL,
                                                                                 option_cond_type=OptionCondType.ALL)
        drvt_put_ret_code, drvt_put_ret_data = quote_ctx.get_option_chain(code='US.GOOG',
                                                                                 option_type=OptionType.PUT,
                                                                                 option_cond_type=OptionCondType.ALL)
        if drvt_put_ret_code==RET_OK and drvt_call_ret_code==RET_OK:
            codes.append(drvt_call_ret_data['code'].tolist()[0])
            codes.append(drvt_put_ret_data['code'].tolist()[0])
        else:
            codes = ['US.DIS180907P95000', 'US.DIS180907C111000']

        #执行测试步骤
        self.step_base(code_list= codes, casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_cn_stock(self):
        #1、测试点：订阅A股正股实时逐笔
        self.step_base(code_list= ['SZ.000001' ,'SH.601318'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_cn_idx(self):
        #1、测试点：订阅A股指数实时逐笔
        self.step_base(code_list= ['SH.000001' ,'SZ.399001'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_cn_etf(self):
        #1、测试点：订阅A股指基金实时逐笔
        self.step_base(code_list= ['SH.501053' ,'SZ.164824'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验


class TickerTest(TickerHandlerBase):

    def on_recv_rsp(self, rsp_str):
        '''
        回调
        :param rsp_str:
        :return:
        '''
        ret_code, ret_data = super(TickerTest, self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了逐笔信息
        print(ret_data, file=f, flush=True)

        return RET_OK, ret_data


if __name__ == '__main__':
    quote_ctx = OpenQuoteContext('127.0.0.1',11122)
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    unittest.main()


# f = open('get_rt_triker2.txt','a')

# class TickerTest(TickerHandlerBase):
#     def on_recv_rsp(self, rsp_str):
#         ret_code, data = super(TickerTest, self).on_recv_rsp(rsp_str)
#         if ret_code != RET_OK:
#             print("TickerTest: error, msg: %s" % data)
#             return RET_ERROR, data
#         # print(datetime.datetime.now().strftime('%c'), file=f, flush=True)
#         # print(data, file=f, flush=True)
#         print(data)
#         return RET_OK, data
#
#
# class SysNotifyTest(SysNotifyHandlerBase):
#     def on_recv_rsp(self, rsp_pb):
#         ret_code, content = super(SysNotifyTest, self).on_recv_rsp(rsp_pb)
#         notify_type, sub_type, msg = content
#         if ret_code != RET_OK:
#             logger.debug("SysNotifyTest: error, msg: %s" % msg)
#             return RET_ERROR, content
#
#         now = datetime.datetime.now()
#         now.strftime('%c')
#         # print(now, file=f, flush=True)
#         # print(msg, file=f, flush=True)
#         print(now)
#         print(msg)
#         return ret_code, content
#
#
# if __name__ == '__main__':
#     # output = sys.stdout
#     # outputfile = open('get_rt_triker1.txt', 'a')
#     # sys.stdout = outputfile
#     pandas.set_option('max_columns', 100)
#     pandas.set_option('display.width', 1000)
#     quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11112)
#     ret_code, ret_data = quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK)
#     code_list = list(ret_data['code'])
#     del code_list[800:]  # 截取股票
#     quote_ctx.set_handler(TickerTest())
#     quote_ctx.set_handler(SysNotifyTest())
#     print(quote_ctx.subscribe(code_list, SubType.TICKER))  # SH.600119
#     quote_ctx.start()







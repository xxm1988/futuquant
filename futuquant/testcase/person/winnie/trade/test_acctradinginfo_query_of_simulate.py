# -*- coding:utf-8 -*-
from futuquant import *
from futuquant.testcase.person.winnie.trade.tradeBase import *
import pandas
import unittest


class AcctradinginfoQuery(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.quote_ctx = OpenQuoteContext('127.0.0.1', 11112)
        self.trade_ctx_hk = OpenHKTradeContext('127.0.0.1', 11111)
        self.trade_ctx_us = OpenUSTradeContext('127.0.0.1', 11111)
        self.trade_ctx_cn = OpenCNTradeContext('127.0.0.1', 11111)
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    # 以下为有效入参用例
    # 港股
    def test_acctradinginfo_query_hk_normal(self):
        # 测试点：港股普通订单
        order_type = OrderType.NORMAL
        code = 'HK.00700'
        price = 0.1
        order_id = None
        # 获取最新价格
        ret_code_ms, ret_data_ms = self.quote_ctx.get_market_snapshot(code)
        if ret_code_ms == RET_OK:
            price = ret_data_ms['last_price'][0]
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_OK)
        keys = ['max_cash_buy', 'max_cash_and_margin_buy', 'max_position_sell', 'max_sell_short', 'max_buy_back']
        for k in keys:
            self.assertTrue(ret_data[k][0] != '')
        print(ret_data)

    def test_acctradinginfo_query_hk_absolute_limit(self):
        # 测试点：港股限价单
        order_type = OrderType.ABSOLUTE_LIMIT
        code = 'HK.00434'
        price = 1.2
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_hk_auction(self):
        # 测试点：港股竞价单
        order_type = OrderType.AUCTION
        code = 'HK.01810'
        price = 1.2
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_hk_auction_limit(self):
        # 测试点：港股竞价限价单
        order_type = OrderType.AUCTION_LIMIT
        code = 'HK.01632'
        price = 1.2
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_hk_special_limit(self):
        # 测试点：港股特别限价单
        order_type = OrderType.SPECIAL_LIMIT
        code = 'HK.01632'
        price = 1.2
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_hk_normal_order_id(self):
        # 测试点：港股普通订单
        order_type = OrderType.NORMAL
        code = 'HK.00700'
        price = 0.1
        order_id = None
        # 获取最新价格
        ret_code_ms, ret_data_ms = self.quote_ctx.get_market_snapshot(code)
        if ret_code_ms == RET_OK:
            price = ret_data_ms['last_price'][0]
        adjust_limit = random.random()
        # 下单
        ret_code_po,ret_data_po = self.trade_ctx_hk.place_order(200,100,'HK.00700',trd_side=TrdSide.BUY,
                                                                adjust_limit=adjust_limit,trd_env=TrdEnv.SIMULATE)
        order_id = ret_data_po['order_id'][0]
        ret_code, ret_data = self.trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.REAL,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_OK)
        keys = ['max_cash_buy', 'max_cash_and_margin_buy', 'max_position_sell', 'max_sell_short', 'max_buy_back']
        for k in keys:
            self.assertTrue(ret_data[k][0] != '')
        print(ret_data)

    def test_acctradinginfo_query_hk_warrant_normal(self):
        # 测试点：港股涡轮普通订单
        order_type = OrderType.NORMAL
        code = 'HK.58354'
        price = 0.8
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_OK)
        keys = ['max_cash_buy', 'max_cash_and_margin_buy', 'max_position_sell', 'max_sell_short', 'max_buy_back']
        for k in keys:
            self.assertTrue(ret_data[k][0] != '')
        print(ret_data)

    # 美股
    def test_acctradinginfo_query_us_normal(self):
        # 测试点：美股普通订单
        order_type = OrderType.NORMAL
        code = 'US.VIPS'
        price = 5.7
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_us.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_OK)
        keys = ['max_cash_buy', 'max_cash_and_margin_buy', 'max_position_sell', 'max_sell_short', 'max_buy_back']
        for k in keys:
            self.assertTrue(ret_data[k][0] != '')
        print(ret_data)

    def test_acctradinginfo_query_us_market(self):
        # 测试点：美股市价单
        order_type = OrderType.MARKET
        code = 'US.QD'
        price = 4.8
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_us.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_us_absolute_limit(self):
        # 测试点：美股限价单
        order_type = OrderType.ABSOLUTE_LIMIT
        code = 'US.JD'
        price = 24
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_us.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_us_auction(self):
        # 测试点：美股竞价单
        order_type = OrderType.AUCTION
        code = 'US.PDD'
        price = 21
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_us.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_us_auction_limit(self):
        # 测试点：美股竞价限价单
        order_type = OrderType.AUCTION_LIMIT
        code = 'US.LFC'
        price = 11.5
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_us.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_us_special_limit(self):
        # 测试点：美股特别限价单
        order_type = OrderType.SPECIAL_LIMIT
        code = 'US.QD'
        price = 4.8
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_us.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_us_normal_order_id(self):
        # 测试点：美股普通订单
        order_type = OrderType.NORMAL
        code = 'US.AAPL'
        price = 0.1
        order_id = None
        # 获取最新价格
        ret_code_ms, ret_data_ms = self.quote_ctx.get_market_snapshot(code)
        if ret_code_ms == RET_OK:
            price = ret_data_ms['last_price'][0]
        adjust_limit = random.random()
        # 下单
        ret_code_po,ret_data_po = self.trade_ctx_us.place_order(price,100,code,trd_side=TrdSide.BUY,
                                                                adjust_limit=adjust_limit,trd_env=TrdEnv.SIMULATE)
        order_id = ret_data_po['order_id'][0]
        ret_code, ret_data = self.trade_ctx_us.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_OK)
        keys = ['max_cash_buy', 'max_cash_and_margin_buy', 'max_position_sell', 'max_sell_short', 'max_buy_back']
        for k in keys:
            self.assertTrue(ret_data[k][0] != '')
        print(ret_data)

    # A股
    def test_acctradinginfo_query_cn_normal(self):
        # 测试点：A股普通订单
        order_type = OrderType.NORMAL
        code = 'US.VIPS'
        price = 5.7
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_cn.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_OK)
        keys = ['max_cash_buy', 'max_cash_and_margin_buy', 'max_position_sell', 'max_sell_short', 'max_buy_back']
        for k in keys:
            self.assertTrue(ret_data[k][0] != '')
        print(ret_data)

    def test_acctradinginfo_query_cn_absolute_limit(self):
        # 测试点：A股限价单
        order_type = OrderType.ABSOLUTE_LIMIT
        code = 'US.JD'
        price = 24
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_cn.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_cn_auction(self):
        # 测试点：A股竞价单
        order_type = OrderType.AUCTION
        code = 'US.PDD'
        price = 21
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_cn.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_cn_auction_limit(self):
        # 测试点：A股竞价限价单
        order_type = OrderType.AUCTION_LIMIT
        code = 'US.LFC'
        price = 11.5
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_cn.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_cn_special_limit(self):
        # 测试点：A股特别限价单
        order_type = OrderType.SPECIAL_LIMIT
        code = 'US.QD'
        price = 4.8
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_cn.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_cn_normal_order_id(self):
        # 测试点：A股普通订单
        order_type = OrderType.NORMAL
        code = 'US.AAPL'
        price = 0.1
        order_id = None
        # 获取最新价格
        ret_code_ms, ret_data_ms = self.quote_ctx.get_market_snapshot(code)
        if ret_code_ms == RET_OK:
            price = ret_data_ms['last_price'][0]
        adjust_limit = random.random()
        # 下单
        ret_code_po,ret_data_po = self.trade_ctx_cn.place_order(price,100,code,trd_side=TrdSide.BUY,
                                                                adjust_limit=adjust_limit,trd_env=TrdEnv.SIMULATE)
        order_id = ret_data_po['order_id'][0]
        ret_code, ret_data = self.trade_ctx_cn.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_OK)
        keys = ['max_cash_buy', 'max_cash_and_margin_buy', 'max_position_sell', 'max_sell_short', 'max_buy_back']
        for k in keys:
            self.assertTrue(ret_data[k][0] != '')
        print(ret_data)

    # 入参错误用例
    def test_acctradinginfo_query_err_code(self):
        order_type = OrderType.NORMAL
        code = 'hk.00700'
        price = 0.1
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_err_price1(self):
        order_type = OrderType.NORMAL
        code = 'HK.00700'
        price = 0
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_err_price2(self):
        order_type = OrderType.NORMAL
        code = 'HK.00700'
        price = -1
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_err_orderid(self):
        order_type = OrderType.NORMAL
        code = 'HK.00700'
        price = 100
        order_id = '12345'
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=1)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)

    def test_acctradinginfo_query_err_account(self):
        order_type = OrderType.NORMAL
        code = 'HK.00700'
        price = 100
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = self.trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=10)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data)


if __name__ == '__main__':
    unittest.main()
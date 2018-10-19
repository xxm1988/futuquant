#-*-coding:utf-8-*-
from futuquant import *
import pandas
import unittest


class GetOrderDetail(unittest.TestCase):
    def __init__(self):
        # 显式调用父类的构造函数
        unittest.TestCase.__init__(self)
        # 保证登录openD的账号有A股LV2权限
        self.quote_ctx = OpenQuoteContext('127.0.0.1',11112)
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    # 以下为有效入参的用例
    def test_get_order_detail_hk_stock(self):
        code = 'HK.00700'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_hk_warrrant(self):
        code = 'HK.62246'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_hk_idx(self):
        code = 'HK.800000'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_hk_future(self):
        code = 'HK_FUTURE.999010'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_us_stock(self):
        code = 'US.AAPL'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_us_idx(self):
        code = 'US..DJI'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_us_etf(self):
        code = 'US.BOM'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_us_option(self):
        code = 'US.AAPL181109C240000'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_cn_idx(self):
        code = 'SZ.800100'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_cn_stock1(self):
        code = 'SH.000001'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 不是空值

    def test_get_order_detail_cn_stock2(self):
        code = 'SZ.000001'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 不是空值

    def test_get_order_detail_cn_stock3(self):
        code = 'SZ.300104'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 不是空值

    # 以下为无效入参的用例
    def test_get_order_detail_wrong_market(self):
        code = 'hk.00700'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data)  # 打印错误提示信息

    def test_get_order_detail_wrong_code1(self):
        code = 'HK.0070'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data)  # 打印错误提示信息

    def test_get_order_detail_wrong_code2(self):
        code = 'SZ.3001040'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data)  # 打印错误提示信息

    def test_get_order_detail_wrong_code3(self):
        code = ''
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data)  # 打印错误提示信息

    def test_get_order_detail_stopped_code(self):
        code = 'US.UWTIF'
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data)  # 打印错误提示信息

    def test_get_order_detail_wrong_type(self):
        code = ['SZ.300104','SZ.002356']
        self.quote_ctx.subscribe(code, SubType.ORDERDETAIL)
        ret_code,ret_data = self.quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data)  # 打印错误提示信息


class OrderDetailTest(OrderDetailHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(OrderDetailTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("OrderDetailTest: error, msg: %s" % data)
            return RET_ERROR, data

        print("OrderDetailTest ", data)  # OrderDetailTest自己的处理逻辑
        return RET_OK, data


if __name__ == '__main__':
    # 低频接口测试
    unittest.main()
    # 高频接口测试
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    handler = OrderDetailTest()
    quote_ctx.set_handler(handler)
    quote_ctx.subscribe(['SH.600030'], [SubType.ORDERDETAIL])
    time.sleep(15)
    quote_ctx.close()

# encoding: UTF-8

'''
    实盘策略范例，接口用法见注释及范例代码
'''
import talib
import sqlite3
import platform
from sqlalchemy import create_engine
from futuquant.examples.TinyQuant.TinyStrateBase import *

class SaveTickData():
    def __init__(self,stock_code):
        self.stock_code  = stock_code
        self.code_suffix = stock_code.split('.')[1]
        if platform.system() == "Windows":
            self.sqlitedb_order = sqlite3.connect(u"F:\\StockData\\stock_order.db")
            self.sqlitedb_tick  = sqlite3.connect(u"F:\\StockData\\stock_tick.db")
        else:
            self.sqlitedb_order = sqlite3.connect(u"/data/ft_hist_data/tick_data/stock_order.db")
            self.sqlitedb_tick  = sqlite3.connect(u"/data/ft_hist_data/tick_data/stock_tick.db")

    def __del__(self):
        self.sqlitedb_conn.close()

    def exe_sql(self,sql_cmd,db='tick'):
        if db == "tick":
            cu = self.sqlitedb_tick.cursor()
        else:
            cu = self.sqlitedb_order.cursor()
        cu.execute(sql_cmd)
        return cu.fetchall()

    def exe_sql_many(self,sql_cmd,insertDataList,db='tick'):
        if db == "tick":
            cu = self.sqlitedb_tick.cursor()
        else:
            cu = self.sqlitedb_order.cursor()
        cu.executemany(sql_cmd,insertDataList)
        return cu.fetchall()

    def create_tick_table(self):
        sql_cmd_create = """create TABLE IF NOT EXISTS  tick_data_%s (
                            [date_key] DATE DEFAULT CURRENT_DATE,
                            [time] TIME DEFAULT CURRENT_TIME,
                            [code] TEXT,
                            [price] FLOAT,
                            [volume] FLOAT,
                            [turnover] FLOAT,
                            [ticker_direction] TEXT,
                            [sequence] TEXT pirmary key,
                            [type] TEXT ) """  % self.code_suffix
        self.exe_sql(sql_cmd_create)
        self.sqlitedb_tick.commit()

    def save_data_to_db(self,df):
        sql_cmd = """ replace into stock_list_new(time,code,price,volume,turnover,ticker_direction,sequence,type) values(?,?,?,?,?,?,?,?) """
        insertItemList = []
        for row in df.itertuples():
            insertItemList.append((row['time'],row['code'],row['price'],row['volume'],row['turnover'],row['ticker_direction'],row['sequence'],row['type'] ))

        result = self.exe_sql_many(sql_cmd,insertItemList)
        self.sqlitedb_tick.commit()
        return result


class TinyStrateSaveTick(TinyStrateBase):
    """策略名称, setting.json中作为该策略配置的key"""
    name = 'tiny_strate_sample'

    """策略需要用到行情数据的股票池"""
    symbol_pools = ['HK.00700', 'HK.00001']

    def __init__(self):
       super(TinyStrateSaveTick, self).__init__()

       """请在setting.json中配置参数"""
       self.param1 = None
       self.param2 = None

    def on_init_strate(self):
        """策略加载完配置后的回调
        1. 可修改symbol_pools 或策略内部其它变量的初始化
        2. 此时还不能调用futu api的接口
        """

    def on_start(self):
        """策略启动完成后的回调
        1. 框架已经完成初始化， 可调用任意的futu api接口
        2. 修改symbol_pools无效, 不会有动态的行情数据回调
        """
        self.log("on_start param1=%s param2=%s" %(self.param1, self.param2))

        """交易接口测试
        ret, data = self.buy(4.60, 1000, 'HK.03883')
        if 0 == ret:
            order_id = data
            ret, data = self.get_tiny_trade_order(order_id)
            if 0 == ret:
                str_info = ''
                for key in data.__dict__.keys():
                    str_info += "%s='%s' " % (key, data.__dict__[key])
                print str_info

        ret, data = self.sell(11.4, 1000, 'HK.01357')
        if 0 == ret:
            order_id = data
            self.cancel_order(order_id)
        """

    def on_quote_changed(self, tiny_quote):
        """报价、摆盘实时数据变化时，会触发该回调"""
        # TinyQuoteData
        data = tiny_quote
        symbol = data.symbol
        str_dt = data.datetime.strftime("%Y%m%d %H:%M:%S")

        # 得到日k数据的ArrayManager(vnpy)对象
        am = self.get_kl_day_am(data.symbol)
        array_high = am.high
        array_low = am.low
        array_open = am.open
        array_close = am.close
        array_vol = am.volume

        n = 5
        ma_high = self.sma(array_high, n)
        ma_low = self.sma(array_low, n)
        ma_open = self.sma(array_open, n)
        ma_close = self.sma(array_close, n)
        ma_vol = self.sma(array_vol, n)

        str_log = "on_quote_changed symbol=%s dt=%s sma(%s) open=%s high=%s close=%s low=%s vol=%s" % (
                    symbol, str_dt, n, ma_open, ma_high, ma_close, ma_low, ma_vol)
        self.log(str_log)

    def on_bar_min1(self, tiny_bar):
        """每一分钟触发一次回调"""
        bar = tiny_bar
        symbol = bar.symbol
        str_dt = bar.datetime.strftime("%Y%m%d %H:%M:%S")

        # 得到分k数据的ArrayManager(vnpy)对象
        am = self.get_kl_min1_am(symbol)
        array_high = am.high
        array_low = am.low
        array_open = am.open
        array_close = am.close
        array_vol = am.volume

        n = 5
        ma_high = self.ema(array_high, n)
        ma_low = self.ema(array_low, n)
        ma_open = self.ema(array_open, n)
        ma_close = self.ema(array_close, n)
        ma_vol = self.ema(array_vol, n)

        str_log = "on_bar_min1 symbol=%s dt=%s ema(%s) open=%s high=%s close=%s low=%s vol=%s" % (
            symbol, str_dt, n, ma_open, ma_high, ma_close, ma_low, ma_vol)
        self.log(str_log)

    def on_bar_day(self, tiny_bar):
        """收盘时会触发一次日k回调"""
        bar = tiny_bar
        symbol = bar.symbol
        str_dt = bar.datetime.strftime("%Y%m%d %H:%M:%S")
        str_log = "on_bar_day symbol=%s dt=%s  open=%s high=%s close=%s low=%s vol=%s" % (
            symbol, str_dt, bar.open, bar.high, bar.close, bar.low, bar.volume)
        self.log(str_log)

    def on_before_trading(self, date_time):
        """开盘时触发一次回调, 脚本挂机切换交易日时，港股会在09:30:00回调"""
        str_log = "on_before_trading - %s" % date_time.strftime('%Y-%m-%d %H:%M:%S')
        self.log(str_log)

    def on_after_trading(self, date_time):
        """收盘时触发一次回调, 脚本挂机时，港股会在16:00:00回调"""
        str_log = "on_after_trading - %s" % date_time.strftime('%Y-%m-%d %H:%M:%S')
        self.log(str_log)

    def sma(self, np_array, n, array=False):
        """简单均线"""
        if n < 2:
            result = np_array
        else:
            result = talib.SMA(np_array, n)
        if array:
            return result
        return result[-1]

    def ema(self, np_array, n, array=False):
        """移动均线"""
        if n < 2:
            result = np_array
        else:
            result = talib.EMA(np_array, n)
        if array:
            return result
        return result[-1]


# encoding: UTF-8

'''
    实盘策略范例，接口用法见注释及范例代码
'''
import talib
import sqlite3
import platform
import multiprocessing
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

'askPrice1', 'askPrice2', 'askPrice3', 'askPrice4', 'askPrice5', 'askVolume1', 'askVolume2', 'askVolume3', 'askVolume4', 'askVolume5', 'bidPrice1', 'bidPrice2', 'bidPrice3', 'bidPrice4', 'bidPrice5', 'bidVolume1', 'bidVolume2', 'bidVolume3', 'bidVolume4', 'bidVolume5', 'date', 'datetime', 'highPrice', 'lastPrice', 'lowPrice', 'openPrice', 'preClosePrice', 'priceSpread', 'symbol', 'time', 'volume'

    def create_order_table(self):
        sql_cmd_create = """create TABLE IF NOT EXISTS  order_data_%s (
                            [date_key] DATE DEFAULT CURRENT_DATE,
                            [time] TIME DEFAULT CURRENT_TIME,
                            [code] TEXT,
                            [askPrice1] FLOAT,
                            [askPrice2] FLOAT,
                            [askPrice3] FLOAT,
                            [askPrice4] FLOAT,
                            [askPrice5] FLOAT,
                            [askVolume1] FLOAT,
                            [askVolume2] FLOAT,
                            [askVolume3] FLOAT,
                            [askVolume4] FLOAT,
                            [askVolume5] FLOAT,
                            [bidPrice1] FLOAT,
                            [bidPrice2] FLOAT,
                            [bidPrice3] FLOAT,
                            [bidPrice4] FLOAT,
                            [bidPrice5] FLOAT,
                            [bidVolume1] FLOAT,
                            [bidVolume2] FLOAT,
                            [bidVolume3] FLOAT,
                            [bidVolume4] FLOAT,
                            [bidVolume5] FLOAT,
                            [highPrice] FLOAT,
                            [lowPrice] FLOAT,
                            [lastPrice] FLOAT,
                            [openPrice] FLOAT,
                            [preClosePrice] FLOAT,
                            [priceSpread] FLOAT,
                            [volume] FLOAT ) """  % self.code_suffix
        self.exe_sql(sql_cmd_create)
        self.sqlitedb_tick.commit()

    def save_data_tick(self,df):
        sql_cmd = """ replace into stock_list_new(time,code,price,volume,turnover,ticker_direction,sequence,type) values(?,?,?,?,?,?,?,?) """
        insertItemList = []
        for row in df.itertuples():
            insertItemList.append((row['time'],row['code'],row['price'],row['volume'],row['turnover'],row['ticker_direction'],row['sequence'],row['type'] ))

        result = self.exe_sql_many(sql_cmd,insertItemList)
        self.sqlitedb_tick.commit()
        return result

    def save_data_order(self,data_list):
        sql_cmd = """ insert into stock_list_new(date_key,time,code,askPrice1,askPrice2,askPrice3,askPrice4,askPrice5,askVolume1,askVolume2,askVolume3,askVolume4,askVolume5,bidPrice1,bidPrice2,bidPrice3,bidPrice4,bidPrice5,bidVolume1,bidVolume2,bidVolume3,bidVolume4,bidVolume5,highPrice,lowPrice,lastPrice,openPrice,preClosePrice,priceSpread,volume) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
        insertItemList = []
        for row in data_list:
            insertItemList.append((row['date'],row['time'],row['code'],row['askPrice1'],row['askPrice2'],row['askPrice3'],row['askPrice4'],row['askPrice5'],row['askVolume1'],row['askVolume2'],row['askVolume3'],row['askVolume4'],row['askVolume5'],row['bidPrice1'],row['bidPrice2'],row['bidPrice3'],row['bidPrice4'],row['bidPrice5'],row['bidVolume1'],row['bidVolume2'],row['bidVolume3'],row['bidVolume4'],row['bidVolume5'],row['highPrice'],row['lowPrice'],row['lastPrice'],row['openPrice'],row['preClosePrice'],row['priceSpread'],row['volume']))

        result = self.exe_sql_many(sql_cmd,insertItemList)
        self.sqlitedb_tick.commit()
        return result

    def save_queue_data(self,symbol,data_queue):
        last_time = time.time()
        data_list = []
        while True:
            print("[%s] data_queue size is %s " % (symbol,data_queue.qsize()))
            tiny_quote = data_queue.get()
            data_list.append(tiny_quote)
            now_time = time.time()
            save_flag = False
            if len(data_list) > 10:
                self.save_data_order(data_list)
                data_list = []
                save_flag = True
                print("[%s] save data length [%s]" % (symbol,len(data_list)))
            elif now_time - last_time > 5 and len(data_list) > 0:
                self.save_data_order(data_list)
                data_list = []
                save_flag = True
                last_time = now_time
                print("[%s] timeout save data length [%s]" % (symbol,len(data_list)))
            if not save_flag:
                time.sleep(1)



class TinyStrateSaveTick(TinyStrateBase):
    """策略名称, setting.json中作为该策略配置的key"""
    name = 'tiny_strate_sample'

    """策略需要用到行情数据的股票池"""
    symbol_pools = ['HK.00700','HK.80000','HK.59972','HK.59828','HK.66115','HK.66490']

    def __init__(self):
        super(TinyStrateSaveTick, self).__init__()

        """请在setting.json中配置参数"""
        self.param1 = None
        self.param2 = None
        self.data_queue_dict = {}
        self.pool = multiprocessing.Pool(processes = 1 )

    def on_init_strate(self):
        """策略加载完配置后的回调
        1. 可修改symbol_pools 或策略内部其它变量的初始化
        2. 此时还不能调用futu api的接口
        """
        for symbol in TinyStrateSaveTick.symbol_pools:
            self.data_queue_dict[symbol.split('.')[1]] = multiprocessing.Manager().Queue()
            stdObj = SaveTickData(symbol.split('.')[1])
            self.pool.apply_async(stdObj.save_queue_data,(symbol,self.data_queue_dict[symbol.split('.')[1]]))

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
        symbol = tiny_quote.symbol
        self.log("get data from {%s}" % symbol)
        self.data_queue_dict[symbol.split('.')[1]].put(tiny_quote)


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


# encoding: UTF-8

'''
记录正股对应窝轮跳价时，正股的委比和盘口情况
备注：修改setting.json文件ip和port

PS:
1、目前只能订阅1个窝轮
2、只能是发行经纪商是高盛、摩通的窝轮
3、只能订阅个股窝轮，因为恒指窝轮对应的正股为恒生指数，没有买卖量等盘口数据
'''

from futuquant.examples.TinyQuant.TinyStrateBase import *
from futuquant.examples.TinyQuant.TinyQuantFrame import *
from futuquant.quote.open_quote_context import *
from futuquant.trade.open_trade_context import *
import datetime
import pandas as pd
from sqlalchemy import create_engine, text
import pymysql


class TinyStrateRec(TinyStrateBase):
    name = 'TinyStrateRec'

    def __init__(self):
        super(TinyStrateRec, self).__init__()
        """请在setting.json中配置参数"""

    def on_init_strate(self):
        """策略加载完配置"""

    def on_quote_changed(self, tiny_quote):
        """报价、摆盘实时数据变化时，会触发该回调"""
        print(tiny_quote)


if __name__ == '__main__':
    my_strate = TinyStrateRec()
    frame = TinyQuantFrame(my_strate)
    frame.run()

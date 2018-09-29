# -*- coding: utf-8 -*-

from futuquant import *
from time import sleep
from futuquant.common.ft_logger import logger
from futuquant.common.utils import ProtobufMap
import multiprocessing as mp
from threading import Thread, RLock
from google.protobuf import json_format
import csv
import urllib
import os.path
import traceback
import threading
import os
import signal
import codecs
from multiprocessing import Lock
import random
import logging


class MiscUtils(object):
    @staticmethod
    def get_current_datetime():
        return '{date:%Y-%m-%d %H:%M:%S}'.format(date=datetime.now())

    @staticmethod
    def get_short_datetime():
        return '{date:%m%d_%H%M%S}'.format(date=datetime.now())

    @staticmethod
    def get_date():
        return '{date:%Y-%m-%d}'.format(date=datetime.now())

    @staticmethod
    def get_time():
        return '{date:%H:%M:%S}'.format(date=datetime.now())


    @staticmethod
    def dump_list_dict_to_file(filename,data):
        keys = data[0].keys()
        with open(filename, 'wb') as output_file:
            output_file.write(u'\ufeff'.encode('utf8'))  # BOM
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
            #{k: v.encode('utf8') for k, v in data.items()}

    @staticmethod
    def get_config():
        configFile = codecs.open("./config.json","r",'utf-8')
        fetcherConfig = json.loads(configFile.read(1024))

class CbbcMonitor:
    future_code = ['HK_FUTURE.999010','HK_FUTURE.999011']
    context = None
    hsif = 0

    def __init__(self, ip, port, data_path, parent_code):
        self._ip = ip
        self._port = port
        self._data_path = data_path
        self._mp_handle = None
        self._mp_manage = mp.Manager()
        self._ns_share = self._mp_manage.Namespace()
        self._exit_event = mp.Event()
        self._score_list = self._mp_manage.Value('score_list', [])
        self._value_lock = Lock()
        self._parent_code = parent_code


    def start(self):
        self._mp_handle = mp.Process(target=self.score_monitor_fun,
                             args=(self._ip, self._port,self._data_path,self._parent_code,
                                   self._exit_event,self._ns_share,self._score_list,
                                   None,self._value_lock))
        self._mp_handle.start()
        print("---monitor process started---")

        return

    def mp_terminate(self):
        pass

    def set_exit(self):
        self._exit_event.set()

    def get_score_result(self):
        pass

    @classmethod
    def score_monitor_fun(cls,ip,port,data_path,parent_code,exit_event,ns_share,score_list,stock_utils,value_lock):
        score_code_list = []
        last_subscription_list = []
        write_count = 0

        min_price = 0.015
        max_price = 0.20
        vol = 5000000
        max_stock = 80
        bull_list = []
        bear_list = []
        cbbc_list = []
        stock_codes = []
        warrant_file = "{}/cbbc_all_list.json".format(data_path)
        cbbc_file = "{}/cbbc_only_list.json".format(data_path)

        def get_bull():
            '''每次换一半,来用测试取消订阅'''
            nonlocal bull_list
            random.shuffle(bull_list)
            return bull_list[0:int(len(bull_list) / 2)]

        def get_bear():
            nonlocal bear_list
            random.shuffle(bear_list)
            return bear_list[0:int(len(bear_list) / 2)]

        def load_list():
            nonlocal cbbc_list
            nonlocal stock_codes
            nonlocal cbbc_file
            nonlocal warrant_file

            try:
                if len(stock_codes) == 0:
                    with open(warrant_file,'r') as handle:
                        stock_codes = json.load(handle)
                        handle.close()

                if len(cbbc_list) == 0:
                    with open(cbbc_file,'r') as handle:
                        cbbc_list = json.load(handle)
                        handle.close()
            except:
                return False

            return True

        def pick_list():
            nonlocal bull_list
            nonlocal bear_list
            nonlocal cbbc_list
            nonlocal min_price
            nonlocal max_price
            nonlocal vol

            selected_codes = []
            new_bull_list = []
            new_bear_list = []

            for row in cbbc_list:
                if (row['suspension'] is False and row['wrt_code'] == 'HK.800000') and \
                        (row['wrt_type'] == 'BULL' or row['wrt_type'] == 'BEAR'):
                    if row['last_price'] > min_price and row['last_price'] < max_price and row['volume'] > vol:
                        # print(row['code'], row['wrt_type'], row['volume'])
                        selected_codes.append(row)

            sorted_codes = sorted(selected_codes, key=lambda k: k['volume'], reverse=True)

            for v in sorted_codes:
                if len(new_bull_list) >= max_stock and len(new_bear_list) >= max_stock:
                    break

                if v['wrt_type'] == 'BULL':
                    if len(new_bull_list) >= max_stock:
                        continue
                    new_bull_list.append(v)
                elif v['wrt_type'] == 'BEAR':
                    if len(new_bear_list) >= max_stock:
                        continue
                    new_bear_list.append(v)

            bull_list = new_bull_list
            bear_list = new_bear_list

        def get_push_type(proto_id):

            if proto_id == ProtoId.Qot_UpdateBasicQot:
                return 'QUOTE'

            if proto_id == ProtoId.Qot_UpdateTicker:
                return 'TICKER'

            if proto_id == ProtoId.Qot_UpdateOrderBook:
                return 'OBOOK'

            if proto_id == ProtoId.Qot_UpdateBroker:
                return 'BROKER'

            return str(proto_id)

        def get_stock_code(stock_market,stock_code):
            for k,v in MKT_MAP.items():
                if v == int(stock_market):
                    return k+'.'+stock_code

        def get_time_from_datetime(date_time):
            date_parts = date_time.split(" ")

            if len(date_parts) != 2:
                return None

            return date_parts[1]


        def on_quote_data(stock_info,rsp_pb,quote_type):

            nonlocal write_count
            if rsp_pb.retType != 0:
                return

            stock_quote = stock_info['stock_quote']
            stock_code = stock_info['code']


            #if write_count % 50 == 0:
            # print("{} {} {} {} {}".format(MiscUtils.get_current_datetime(), stock_quote['time'], stock_code,CbbcMonitor.hsif, quote_type))

            if write_count % 500 == 0:
                print("收到 {} 个推送数据".format(write_count))

            if quote_type == 'QUOTE':
                stock_quote['time'] = get_time_from_datetime(rsp_pb.s2c.basicQotList[0].updateTime)
                stock_quote['curPrice'] = rsp_pb.s2c.basicQotList[0].curPrice
                if stock_code in CbbcMonitor.future_code:
                    CbbcMonitor.hsif = rsp_pb.s2c.basicQotList[0].curPrice
                    # if write_count % 50 == 0:
                    #     print("{} {} {} {} {}".format(MiscUtils.get_current_datetime(), stock_quote['time'], stock_code, CbbcMonitor.hsif, quote_type))
            elif quote_type == 'TICKER':
                stock_quote['time'] = get_time_from_datetime(rsp_pb.s2c.tickerList[0].time)
                if stock_code in CbbcMonitor.future_code:
                    CbbcMonitor.hsif = rsp_pb.s2c.tickerList[0].price
                    #print("{} {} {} {} {}".format(MiscUtils.get_current_datetime(), stock_quote['time'], stock_code, CbbcMonitor.hsif, quote_type))
            elif quote_type == 'BROKER':
                bid_broker = []
                ask_broker = []
                [ask_broker.append([v.id,v.pos]) for v in rsp_pb.s2c.brokerAskList]
                [bid_broker.append([v.id,v.pos]) for v in rsp_pb.s2c.brokerBidList]
                stock_quote['ask_broker'] = ask_broker
                stock_quote['bid_broker'] = bid_broker
            elif quote_type == 'OBOOK':
                ask = []
                bid = []
                [ask.append((v.price,v.volume,v.orederCount)) for v in rsp_pb.s2c.orderBookAskList]
                [bid.append((v.price,v.volume,v.orederCount)) for v in rsp_pb.s2c.orderBookBidList]
                stock_quote['ask'] = ask
                stock_quote['bid'] = bid


        def save_push_data(market,code,data,proto_id,rsp_pb):
            nonlocal score_code_list
            nonlocal write_count
            quote_type = get_push_type(proto_id)
            write_count += 1
            stock_code = get_stock_code(market, code)
            stock_data = bytes(data.replace("\n",""), "utf-8").decode("unicode_escape")
            stock_data = str(time.time()) + '|' + quote_type + '|' + stock_data + '\n'

            for stock_info in score_code_list:
                if stock_code in stock_info['code']:
                    on_quote_data(stock_info, rsp_pb, get_push_type(proto_id))
                    # if stock_info['quote_handle'] is not None:
                    #     # handle = stock_info['quote_handle']
                    #     # handle.write(stock_data)
                    #     # '''100次写一次磁盘'''
                    #     # if write_count % 100 == 0:
                    #     #     handle.flush()
                    #     #     print("data write count: {}".format(write_count))
                    # break

            return RET_OK

        class ProcessQuoteHandle(StockQuoteHandlerBase):
            _proto_id = ProtoId.Qot_UpdateBasicQot

            def on_recv_rsp(self, rsp_pb):
                """基本报价 数据响应回调函数"""
                try:
                    stock_code = rsp_pb.s2c.basicQotList[0].security.code
                    stock_market = rsp_pb.s2c.basicQotList[0].security.market

                    if stock_code == '800000' or stock_code == '800100':
                        rsp_pb.s2c.basicQotList[0].amplitude = 0
                        rsp_pb.s2c.basicQotList[0].listTime = ''

                    stock_string = json_format.MessageToJson(rsp_pb, indent=0)

                    return save_push_data(stock_market,stock_code,stock_string,self._proto_id,rsp_pb)
                except AttributeError:
                    pass
                except:
                    traceback.print_exc()
                    pass

        class ProcessTickerHandle(TickerHandlerBase):
            _proto_id = ProtoId.Qot_UpdateTicker

            def on_recv_rsp(self, rsp_pb):
                """每笔成交 数据响应回调函数"""
                try:
                    stock_code = rsp_pb.s2c.security.code
                    stock_market = rsp_pb.s2c.security.market
                    stock_string = json_format.MessageToJson(rsp_pb, indent=0)

                    return save_push_data(stock_market,stock_code,stock_string,self._proto_id,rsp_pb)
                except AttributeError:
                    pass
                except:
                    traceback.print_exc()
                    pass

        class ProcessOrderBookHandle(OrderBookHandlerBase):
            _proto_id = ProtoId.Qot_UpdateOrderBook

            def on_recv_rsp(self, rsp_pb):
                """摆盘数据 数据响应回调函数"""
                try:
                    stock_code = rsp_pb.s2c.security.code
                    stock_market = rsp_pb.s2c.security.market
                    stock_string = json_format.MessageToJson(rsp_pb, indent=0)

                    return save_push_data(stock_market,stock_code,stock_string,self._proto_id,rsp_pb)
                except AttributeError:
                    pass
                except:
                    traceback.print_exc()
                    pass

        class ProcessBrokerHandle(BrokerHandlerBase):
            _proto_id = ProtoId.Qot_UpdateBroker

            def on_recv_rsp(self, rsp_pb):
                """经纪商 数据响应回调函数"""
                try:
                    stock_code = rsp_pb.s2c.security.code
                    stock_market = rsp_pb.s2c.security.market

                    for bd in rsp_pb.s2c.brokerBidList:
                        bd.name = ''

                    for bd in rsp_pb.s2c.brokerAskList:
                        bd.name = ''

                    stock_string = json_format.MessageToJson(rsp_pb, indent=0)

                    return save_push_data(stock_market,stock_code,stock_string,self._proto_id,rsp_pb)
                except AttributeError:
                    pass
                except:
                    traceback.print_exc()
                    pass

        def connect_server(ip,port):
            quote_ctx = OpenQuoteContext(ip, port)
            quote_ctx.set_handler(ProcessTickerHandle())
            quote_ctx.set_handler(ProcessQuoteHandle())
            quote_ctx.set_handler(ProcessOrderBookHandle())
            quote_ctx.set_handler(ProcessBrokerHandle())
            quote_ctx.start()
            return quote_ctx

        def sync_subscription_list():
            nonlocal score_code_list
            subscription_list = []

            bull_list = get_bull()
            bear_list = get_bear()
            subscription_list = bull_list + bear_list

            if len(subscription_list) == 0:
                return False

            subscription_list.append({
                'code': parent_code,'last_price': 0,'volume': 0,'suspension': False,
                'wrt_valid': True,'wrt_street_ratio': 0,'wrt_type': 'HSI','wrt_strike_price': 0,
                'wrt_recovery_price':0,'wrt_conversion_ratio': 1,'lot_size': 1,'price_spread': 1
            })

            new_code_list = []

            for v in subscription_list:
                found = False
                for stock_info in score_code_list:
                    if stock_info['code'] == v['code']:
                        found = True
                        stock_info['last_price'] = v['last_price']
                        stock_info['volume'] = v['volume']
                        stock_info['suspension'] = v['suspension']
                        stock_info['wrt_valid'] = v['wrt_valid']
                        stock_info['wrt_street_ratio'] = v['wrt_street_ratio']
                        stock_info['lot_size'] = v['lot_size']
                        stock_info['price_spread'] = v['price_spread']
                        break

                if found == False:
                    is_bull = True if v['wrt_type'] == 'BULL' else False
                    exchange_rate = round(v['wrt_conversion_ratio']/1000,0)
                    score_instance = None
                    broker_instance = None
                    quote_handle = None

                    stock_quote = {'code': v['code'],'time': None,'curPrice': None,'ask': None,'bid': None,
                                   'ask_broker': None,'bid_broker': None}

                    score_code_list.append({
                        'code': v['code'],
                        'last_price': v['last_price'],
                        'volume': v['volume'],
                        'suspension': v['suspension'],
                        'wrt_valid': v['wrt_valid'],
                        'wrt_street_ratio': v['wrt_street_ratio'],
                        'wrt_type': v['wrt_type'],
                        'wrt_strike_price': v['wrt_strike_price'],
                        'wrt_recovery_price': v['wrt_recovery_price'],
                        'wrt_conversion_ratio': v['wrt_conversion_ratio'],
                        'lot_size': v['lot_size'],
                        'price_spread': v['price_spread'],
                        'stock_quote': stock_quote,
                    })

            for v in score_code_list:
                for stock_info in subscription_list:
                    if stock_info['code'] == v['code']:
                        new_code_list.append(v)
                        break

            score_code_list = new_code_list

            return True

        def sync_score_monitor(ctx):
            nonlocal last_subscription_list
            nonlocal score_code_list

            if sync_subscription_list() == False:
                return

            type_list = [SubType.TICKER,SubType.QUOTE,SubType.ORDER_BOOK,SubType.BROKER]
            subscriptionRes = ctx.query_subscription()
            print(subscriptionRes)

            total_used = subscriptionRes[1]['total_used']
            own_used = subscriptionRes[1]['own_used']
            remain = subscriptionRes[1]['remain']

            new_subscrption_list = []
            subscription_to_add = []

            '''重新订阅之前所有订阅的数据'''
            if len(last_subscription_list) == 0:
                if subscriptionRes[0] == 0:
                    for sub_type in type_list:
                        if sub_type in subscriptionRes[1]['sub_list'].keys():
                            print("{} {}".format(sub_type, subscriptionRes[1]['sub_list'][sub_type]))
                            ctx.subscribe(subscriptionRes[1]['sub_list'][sub_type], [sub_type],False)


            for v in score_code_list:
                if v['code'] not in last_subscription_list:
                    subscription_to_add.append(v['code'])            #本次要订阅的代码
                new_subscrption_list.append(v['code'])              #最新订阅的代码


            t = time.time()

            unsubscripe_list = []
            subscripe_list = []

            '''如果已经订阅,但是不在最后的列表中,则反订阅'''
            for sub_type in type_list:
                if sub_type in subscriptionRes[1]['sub_list'].keys():
                    for v in subscriptionRes[1]['sub_list'][sub_type]:
                        if v not in new_subscrption_list:
                            #print("unsubscribe -----{} {}-----".format(v,sub_type))
                            #ret, data = ctx.unsubscribe(v, sub_type)
                            unsubscripe_list.append([v,sub_type])

                        if v in CbbcMonitor.future_code and sub_type in [SubType.BROKER,SubType.ORDER_BOOK]:
                            #print("unsubscribe -----{} {}-----".format(v,sub_type))
                            #ret, data = ctx.unsubscribe(v, sub_type)
                            unsubscripe_list.append([v,sub_type])

            if len(unsubscripe_list) > 0:
                print("unsubscripe {}".format(len(unsubscripe_list)))
                print(unsubscripe_list)
                for i in range(len(unsubscripe_list)):
                    '''这里调用可能会导致API卡死'''
                    ret,data = ctx.unsubscribe(unsubscripe_list[i][0], unsubscripe_list[i][1])
                    if (i + 1) % 10 == 0:
                        print("取消 {} 个订阅, 共 {} 个要取消订阅, sleep 1 秒,可能导致API卡死!".format(i+1,len(unsubscripe_list)))
                        sleep(1)

            '''如果有需要新订阅的,则加入'''
            if len(subscription_to_add) > 0:
                print("-----{} subscription_to_add-----".format(len(subscription_to_add)))
                print(subscription_to_add)
                ret, data = ctx.subscribe(subscription_to_add,type_list,False)
                sleep(1)
                print("-----{} subscription_to_add=====".format(len(subscription_to_add)))

            subscriptionRes = ctx.query_subscription()
            print(subscriptionRes)
            print(time.time() - t)

            '''再检查一次. 如果已订阅的列表里没有,则订阅'''
            for v in new_subscrption_list:
                for sub_type in type_list:
                    if sub_type in subscriptionRes[1]['sub_list'].keys():
                        if v not in subscriptionRes[1]['sub_list'][sub_type]:
                            if v not in CbbcMonitor.future_code:
                                #print("subscribe -----{} {}-----".format(v,sub_type))
                                #ret, data = ctx.subscribe(v, sub_type)
                                subscripe_list.append([v,sub_type])

                            if v in CbbcMonitor.future_code and sub_type in [SubType.QUOTE,SubType.TICKER]:
                                #print("subscribe -----{} {}-----".format(v,sub_type))
                                #ret, data = ctx.subscribe(v, sub_type)
                                subscripe_list.append([v,sub_type])

            if len(subscripe_list) > 0:
                print("subscripe {}".format(len(subscripe_list)))
                print(subscripe_list)
                for v in subscripe_list:
                    ret,data = ctx.subscribe(v[0], v[1], False)

            last_subscription_list = new_subscrption_list

            return

        """多进程处理罗辑"""
        ctx = connect_server(ip,port)

        sleep_count = 0
        while not exit_event.is_set():
            if sleep_count % 65 == 0:
                load_list()
                pick_list()
                # try:
                sync_score_monitor(ctx)
                print("等 65 秒后取消订阅一半推送")
                #except:
                #    pass
            sleep(1)
            sleep_count +=1

        # stock_utils.set_exit()
        # stock_utils.mp_terminate()
        print("===exit monitor prrocess===")

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    server_ip = "127.0.0.1"
    server_port = 11111
    data_path = "./trade_data/" + MiscUtils.get_date()

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    score_monitor = CbbcMonitor(server_ip, server_port, data_path, 'HK_FUTURE.999010')
    score_monitor.start()

    sleep_count = 0
    while True:
        sleep_count += 1
        sleep(10)

    sleep(30)
    print("exit main process")
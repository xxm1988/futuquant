from futuquant import *
import futuquant as ft

class TradeOrderHandler(TradeOrderHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret, data = super().on_recv_rsp(rsp_pb)
        logger.info(f'{ret}, {data}')


class TradeDealHandler(TradeDealHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret, data = super().on_recv_rsp(rsp_pb)
        logger.info(f'{ret}, {data}')

def trade1():
    trade_ctx = OpenHKTradeContext()
    trade_ctx.set_handler(TradeOrderHandler())
    trade_ctx.set_handler(TradeDealHandlerBase())
    trade_ctx.start()
    ret, data = trade_ctx.unlock_trade('123123')
    print(ret, data)
    ret, data = trade_ctx.acctradinginfo_query(OrderType.NORMAL, '00700', 100, 0)
    print(ret, data)
    # print(ret, data)
    # ret, data = trade_ctx.modify_order(ModifyOrderOp.ENABLE, data.at[0, 'order_id'], 0, 0)
    # ret, data = trade_ctx.order_list_query('8536846713393711549')
    # print(ret, data)
    # trade_ctx.close()


if __name__ == '__main__':
    print(ft.__version__)
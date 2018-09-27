from futuquant import *
import collect_stock
import threading
import time

log_delay = open('log/CntDly.log', 'w')

vTicker = [0] * 2001
vBasic = [0] * 2001
vObook = [0] * 2001


def print_time(sleep_time):
    time.sleep(sleep_time * 60)

    print('Ticker Delay : '.format(), file=log_delay)
    for i, value in enumerate(vTicker):
        print('{:.6f}s : {}'.format(0.000010 * i, value), file=log_delay)

    print('Basic Delay : '.format(), file=log_delay)
    for i, value in enumerate(vBasic):
        print('{:.6f}s : {}'.format(0.000010 * i, value), file=log_delay)

    print('OrderBook Delay : '.format(), file=log_delay)
    for i, value in enumerate(vObook):
        print('{:.6f}s : {}'.format(0.000010 * i, value), file=log_delay)

    log_delay.close()


class TickHandlerReal(TickerHandlerBase):
    def __init__(self):
        super().__init__()

    def on_recv_rsp(self, rsp_pb):
        ret, data = super().parse_rsp_pb(rsp_pb)

        if ret != RET_OK:
            return
        else:
            for tick in data:
                # self.handle_tick(tick)
                now = datetime.now().timestamp()
                opend_recv_time = tick['recv_timestamp']

                nDelayTime = now - opend_recv_time
                if (0.020000 <= nDelayTime):
                    vTicker[-1] += 1
                else:
                    vTicker[int(nDelayTime / 0.000010)] += 1
        return ret, data

    # def handle_tick(self, tick):
    #     now = datetime.now().timestamp()
    #     opend_recv_time = tick['recv_timestamp']
    #
    #     nDelayTime = now - opend_recv_time
    #     if(0.020000 <= nDelayTime):
    #         vTicker[-1] += 1
    #     else:
    #         vTicker[int(nDelayTime/0.000010)] += 1


class QuoteHandlerReal(StockQuoteHandlerBase):
    def __init__(self):
        super().__init__()

    def on_recv_rsp(self, rsp_pb):
        ret, data = super().parse_rsp_pb(rsp_pb)

        if ret != RET_OK:
            return
        else:
            for quote in data:
                # self.handle_quote(quote)
                now = datetime.now().timestamp()
                opend_recv_time = quote['recv_timestamp']

                nDelayTime = now - opend_recv_time
                if (0.020000 <= nDelayTime):
                    vBasic[-1] += 1
                else:
                    vBasic[int(nDelayTime / 0.000010)] += 1
        return ret, data

    # def handle_quote(self, quote):
    #     now = datetime.now().timestamp()
    #     opend_recv_time = quote['recv_timestamp']
    #
    #     nDelayTime = now - opend_recv_time
    #     if (0.020000 <= nDelayTime):
    #         vBasic[-1] += 1
    #     else:
    #         vBasic[int(nDelayTime / 0.000010)] += 1


class OBookHandlerReal(OrderBookHandlerBase):
    def __init__(self):
        super().__init__()

    def on_recv_rsp(self, rsp_pb):
        ret, data = super().parse_rsp_pb(rsp_pb)

        if ret != RET_OK:
            return
        else:
            # self.handle_obook(data)
            now = datetime.now().timestamp()
            opend_recv_time = data['recv_timestamp']

            nDelayTime = now - opend_recv_time
            if (0.020000 <= nDelayTime):
                vObook[-1] += 1
            else:
                vObook[int(nDelayTime / 0.000010)] += 1

        return ret, data

    # def handle_obook(self, obook):
    #
    #     now = datetime.now().timestamp()
    #     opend_recv_time = obook['recv_timestamp']
    #
    #     nDelayTime = now - opend_recv_time
    #     if (0.020000 <= nDelayTime):
    #         vObook[-1] += 1
    #     else:
    #         vObook[int(nDelayTime / 0.000010)] += 1


def test_tick():
    codes = collect_stock.load_stock_code('stock-hk.csv')

    ip = '127.0.0.1'
    port = 8100
    quote_ctx = OpenQuoteContext(ip, port)

    ret, data = quote_ctx.get_global_state()
    if ret != RET_OK:
        return

    lastLocalSvrTimeDiff = data['lastLocalSvrTimeDiff']
    str_diff = 'lastLocalSvrTimeDiff={}'.format(lastLocalSvrTimeDiff)

    # 单位：分钟
    sleep_time = 5
    t = threading.Thread(target=print_time, args=(sleep_time, ))
    t.start()

    quote_ctx.set_handler(TickHandlerReal())
    quote_ctx.set_handler(QuoteHandlerReal())
    quote_ctx.set_handler(OBookHandlerReal())
    quote_ctx.start()

    code_sub = codes[:100]
    print(quote_ctx.subscribe(code_sub, [SubType.TICKER, SubType.QUOTE, SubType.ORDER_BOOK], False))


if __name__ == "__main__":

    test_tick()
    while True:
        time.sleep(0.2)
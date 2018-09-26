from futuquant import *
import pandas
import sys
import datetime


class TickerTest(TickerHandlerBase):
        def on_recv_rsp(self, rsp_str):
                ret_code, data = super(TickerTest, self).on_recv_rsp(rsp_str)
                if ret_code != RET_OK:
                        print("TickerTest: error, msg: %s" % data)
                        return RET_ERROR, data
                # with open('get_rt_triker1.txt', 'at') as f:
                output = sys.stdout
                outputfile = open('get_rt_triker1.txt', 'a')
                sys.stdout = outputfile
                print(data)
                sys.stdout = output
                return RET_OK, data


class SysNotifyTest(SysNotifyHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, content = super(SysNotifyTest, self).on_recv_rsp(rsp_pb)
        notify_type, sub_type, msg = content
        if ret_code != RET_OK:
            logger.debug("SysNotifyTest: error, msg: %s" % msg)
            return RET_ERROR, content
        with open('get_rt_triker2.txt', 'a') as f:
            now = datetime.datetime.now()
            now.strftime('%c')
            print(now, file=f)
            print(msg, file=f)

        return ret_code, content


if __name__ == '__main__':
    # output = sys.stdout
    # outputfile = open('get_rt_triker1.txt', 'a')
    # sys.stdout = outputfile
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.subscribe(['HK.00700'], SubType.TICKER)  # SH.600119
    quote_ctx.start()

    quote_ctx.set_handler(TickerTest())
    quote_ctx.set_handler(SysNotifyTest())





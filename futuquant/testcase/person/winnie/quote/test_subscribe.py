# -*- coding:utf-8 -*-
from futuquant import *


def test_subscribe():
    # SysConfig.set_all_thread_daemon(False)
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11112)
    print(quote_ctx.subscribe(['HK.00001'], SubType.TICKER))
    print(quote_ctx.subscribe(['HK.00002'], SubType.TICKER))
    print(quote_ctx.query_subscription())
    quote_ctx.close()


if __name__ == '__main__':
    test_subscribe()

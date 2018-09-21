from futuquant import *
import futuquant

print(futuquant.__file__)

quote_ctx = OpenQuoteContext()
trd_ctx = OpenHKTradeContext()

class StockQuoteHandler(StockQuoteHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret, data = super().on_recv_rsp(rsp_pb)
        print(ret, data)
        # d = trd_ctx.position_list_query()
        # print(d)


def main():
    # print(trd_ctx.unlock_trade('xxx'))
    quote_ctx.set_handler(StockQuoteHandler())
    quote_ctx.subscribe('HK_FUTURE.999010', [SubType.QUOTE])


if __name__ == '__main__':
    main()
    # pass
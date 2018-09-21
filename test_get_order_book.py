from futuquant import *

def test1(quote_ctx:OpenQuoteContext):
    quote_ctx.subscribe('US.PPDF', [SubType.ORDER_BOOK])
    ret, data = quote_ctx.get_order_book('US.PPDF')
    print(ret, data)


if __name__ == '__main__':
    quote_ctx = OpenQuoteContext('172.18.10.58', 11113)
    test1(quote_ctx)
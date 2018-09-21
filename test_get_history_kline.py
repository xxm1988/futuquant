from futuquant import *

def test1(quote_ctx: OpenQuoteContext):
    for au_type in (AuType.QFQ, AuType.HFQ, AuType.NONE):
        ret, data = quote_ctx.get_history_kline("HK.00152", "2014-01-01", "2014-03-01", ktype=KLType.K_MON, autype=au_type)
        print(data)

if __name__ == '__main__':
    quote_ctx = OpenQuoteContext('127.18.10.58', 11113)
    test1(quote_ctx)
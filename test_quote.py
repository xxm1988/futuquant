from futuquant import *
from apscheduler.schedulers.blocking import BlockingScheduler

def work():
    quote_ctx = OpenQuoteContext()
    ret, data = quote_ctx.get_stock_basicinfo(Market.SH, SecurityType.BOND)
    for idx, row in data.iterrows():
        if row['delisting'] == True:
            print(row)
    quote_ctx.close()


if __name__ == '__main__':
    work()
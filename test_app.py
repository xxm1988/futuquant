from futuquant.examples.app.tq_south_etf.TinyStrateSouthETF import TinyStrateSouthETF
from futuquant.examples.TinyQuant.TinyQuantFrame import TinyQuantFrame


if __name__ == '__main__':
    my_strate = TinyStrateSouthETF()
    frame = TinyQuantFrame(my_strate)
    frame.run()
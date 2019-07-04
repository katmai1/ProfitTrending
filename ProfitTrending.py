import ccxt
from talib import abstract
from pandas import DataFrame


class ProfitTrending:

    def __init__(self, exchange="binance", symbol="BTC/USDT"):
        self.exchange = exchange
        self.symbol = symbol
        self.ex = getattr(ccxt, exchange)({ 'enableRateLimit': True })

    def update_ohlcv(self, timeframe):
        data = self.ex.fetch_ohlcv(self.symbol, timeframe)
        df = DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df.set_index('timestamp', inplace=True, drop=True)
        self.data = df

    # ─── TA ─────────────────────────────────────────────────────────────────────────

    def _get_func(self, func_name):
        return abstract.Function(func_name)

    def ema(self, period):
        funcion = self._get_func('ema')
        result = funcion(self.data, timeperiod=period)
        return list(result)[-1]


if __name__ == "__main__":
    pt = ProfitTrending()
    pt.update_ohlcv("30m")
    
    refMA = pt.ema(5)
    fastMA = pt.ema(34)
    slowMA = pt.ema(55)

    print(refMA)
    print(fastMA)
    print(slowMA)
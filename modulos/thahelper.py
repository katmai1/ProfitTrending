import ccxt
import json

from talib import abstract
from pandas import DataFrame


class TAHelperReduced:

    def __init__(self, exchange, market):
        self.exchange = exchange
        self.market = market
        self.ex = getattr(ccxt, exchange)({ 'enableRateLimit': True })

    def update_ohlcv(self, timeframe="30m"):
        data = self.ex.fetch_ohlcv(self.market, timeframe)
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

    def trending(self, timeframe):
        self.update_ohlcv(timeframe)
        refMA = self.ema(5)
        fastMA = self.ema(34)
        slowMA = self.ema(55)
        if refMA > fastMA and refMA > slowMA:
            return "Bullish"
        elif refMA < fastMA and refMA < slowMA:
            return "Bearish"
        elif refMA > fastMA and refMA < slowMA:
            return "PossibleBull"
        elif refMA < fastMA and refMA > slowMA:
            return "PossibleBear"
        else:
            return "Desconocido"
    
    def get_markets_list(self, quote="BTC"):
        lista_markets = []
        self.ex.load_markets()
        for market in self.ex.symbols:
            if market.split("/")[1] == quote:
                lista_markets.append(market)
        return lista_markets

import miniaudio
from time import sleep
from datetime import datetime
import random
import requests

from .thahelper import TAHelperReduced


class ProfitTrending:

    def __init__(self, config):
        self.config = config
        self.ta = TAHelperReduced(config['exchange'], config['symbol'])
        self.trend_base = self.ta.trending(config['timeframe'])

    # ─── PROPIEDADES ────────────────────────────────────────────────────────────────

    @property
    def trend_profit(self):
        conv = { "Bearish": "Bullish", "Bullish": "Bearish", "PossibleBear": "PossibleBull", "PossibleBull": "PossibleBear"}
        try:
            return conv[self.trend_base]
        except Exception as e:
            print(f" [!] Error: {e}")
            return "Desconocido"

    # ─── METODOS ────────────────────────────────────────────────────────────────────

    # trend parser, comprueba si el trend ha cambiado
    def run(self):
        new_trend_base = self.ta.trending(self.config['timeframe'])
        if new_trend_base != self.trend_base:
            self.log(f"Nuevo trend base: '{new_trend_base}'")
            self.trend_base = new_trend_base
            self.log(f"Nuevo trend profit: {self.trend_profit}")
            self.set_estrategia()

    # canvia la estrategia
    def set_estrategia(self):
        estrategia = self.config['estrategias'][self.trend_profit]
        self.log(f"Aplicando estrategia '{estrategia}'")
        # TODO: funcion CURL
        self.send_api(estrategia)

    def send_api(self, estrategia):
        dominio = f"http://{self.config['ip']}:{self.config['port']}"
        endpoint = f"/settingsapi/config/switch?configName={estrategia}"
        licencia = f"?license={self.config['license']}"
        url = dominio + endpoint + licencia
        data = { "Accept": "*/*" }
        r = requests.post(url=url, data=data)
        print(r.text())


    # imprime mensajes de log
    def log(self, mensaje):
        fecha = str(datetime.utcnow()).split(" ")[0]
        hora = str(datetime.utcnow()).split(" ")[1].split(".")[0]
        print(f"[{fecha}][{hora}] {str(mensaje)}")

    # ─── METODOS PRUEBAS ────────────────────────────────────────────────────────────

    def debug_compare_markets(self):
        base = "BTC/USDT"
        print(f"[{base}]: " + self.get_trend_by_market(base))
        #
        lista_markets = self.ta.get_markets_list()
        for x in range(0, 20):
            aleatorio = random.randint(0, len(lista_markets)-1)
            symbol = lista_markets[aleatorio]
            print(f"[{x}][{symbol}]: " + self.get_trend_by_market(symbol))
            sleep(1)

    # checkea toda la lista de markets
    def check_all(self):
        ta = TAHelperReduced(self.config['exchange'], "")
        lista_bull = []
        lista_bear = []
        lista_markets = ta.get_markets_list()
        for  market in lista_markets:
            ta.market = market
            trend = ta.trending(self.config['timeframe'])
            if "Bullish" == trend:
                lista_bull.append(market)
            if "Bear" == trend:
                lista_bear.append(market)
            sleep(1)
        return lista_bull, lista_bear

    def get_trend_by_market(self, market):
        ta = TAHelperReduced(self.config['exchange'], market)
        return ta.trending(self.config['timeframe'])

    def notificacion(self):
        stream = miniaudio.stream_file("/home/user/dev/scalpbot/notify.mp3")
        device = miniaudio.PlaybackDevice()
        device.start(stream)
        sleep(2)
        device.close()
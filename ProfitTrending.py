from sys import exit
from time import sleep
import json

from modulos.profit_class import ProfitTrending


# main
if __name__ == "__main__":
    
    # lee config
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
            pt = ProfitTrending(config)
    except Exception as e:
        print("Error al cargar config.json")
        exit(e)

    # info
    print("\n###########################################\n")
    pt.log("Iniciando ProfitTrending")
    print(f" [i] Exchange: {config['exchange'].capitalize()}")
    print(f" [i] Trending de {config['symbol']}: {pt.trend_base}")
    print("    * Este trending es el del moneda que usamos como base para tradear")
    print()
    print(f" [i] Trending para el ProfitTrailer: {pt.trend_profit}")
    print("    * Este es el equivalente en los markets que vamos a usar")
    print("\n-------------------------------------------------------\n")
    
    # asignando estrategia segun la tendencia actual
    pt.set_estrategia()

    # calcula segundos a esperar segun el timeframe
    t = { "m": 60, "h": 3600, "d": 86400 }
    numero = config['timeframe'][:-1]
    letra = config['timeframe'][-1]
    segundos_total = int(numero) * t[letra]
    pausa = segundos_total * 0.25
    
    # bucle principal
    while True:
        try:
            pt.run()          
            sleep(pausa)
        
        except KeyboardInterrupt:
            exit("Saliendo...")
        
        except Exception as e:
            print(f"\n[!] Error: {e}")

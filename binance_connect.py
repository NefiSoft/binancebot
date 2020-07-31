import binance
from binance.client import Client
from operator import attrgetter


# api_key = "xpfCtik1Ldw1iUTmAZblHEMjP2v0yFEbtE2zV7NDgBmvKkRcetYoOndAiXV1us7N"
# api_secret = "xoJbePrFLzGuiaiKuWO23kMZeRZgeXYOD0jS2aEuOfm73Uch001DKjaHmkPYNTtG"
# client = Client(api_key, api_secret)

def try_connect(api_key: str, api_secret: str):
    client = Client(api_key, api_secret)
    try:
        client.get_account()
        return True
    except:
        return False


def get_account_info(hide_small, api_key, api_secret):
    all_coins = []
    client = Client(api_key,api_secret)
    info = client.get_account()
    prices = client.get_all_tickers()
    for coin in info['balances']:
        if float(coin['free']) + float(coin['locked']) > 0:
            was_finded = False
            amount_in_usdt = 0.0
            for component in prices:
                if component['symbol'] == coin['asset'] + 'USDT':
                    amount_in_usdt = float(component['price']) * (float(coin['free']) + float(coin['locked']))
                    was_finded = True
            if not was_finded:
                btc_price = 0.0
                for component in prices:
                    if component['symbol'] == 'BTCUSDT':
                        btc_price = float(component['price'])
                for component in prices:
                    if component['symbol'] == coin['asset'] + 'BTC':
                        amount_in_usdt = float(component['price']) * (
                                float(coin['free']) + float(coin['locked'])) * btc_price
            if (not hide_small) or (hide_small and amount_in_usdt > 0.01):
                coins = dict(asset=coin['asset'], free=coin['free'], locked=coin['locked'], inUSDT=amount_in_usdt)
                all_coins.append(coins)

            def coins_sorting(key):
                return -key['inUSDT']

    return sorted(all_coins, key=coins_sorting)

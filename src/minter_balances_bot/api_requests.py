import requests

class MinterApi:
    # find out the number of BIP coins in the delegations by wallet
    def get_delegations(self, wallet: str) -> float:
        return round(float(requests.get(f'https://explorer-api.minter.network/api/v2/addresses/{wallet}/delegations').json()['meta']['additional']['total_delegated_bip_value']), 2)

    # find out the number of BIP coins in unbonds by wallet
    def get_unbonds(self, wallet: str) -> float:
        unbonds_json = requests.get(f'https://explorer-api.minter.network/api/v2/addresses/{wallet}/events/unbonds').json()
        if not unbonds_json['data']: return 0
        else:
            unbonds = 0.0
            for d in unbonds_json['data']:
                unbonds += float(d['value'])
            return round(unbonds, 2)

    # find out the number of BIP coins in wallet
    def get_current_balance(self, wallet: str) -> float:
        balances_json = requests.get(f'https://explorer-api.minter.network/api/v2/addresses/{wallet}').json()
        if not balances_json['data']['balances']: return 0
        else:
            balance = 0.0
            for d in balances_json['data']['balances']:
                balance += float(d['bip_amount'])
            return round(balance, 2)

class ExchangeRate:
    # find out the BTC-USDT exchange rate on Binance
    def get_binance_rate(self, symbol: str) -> float:
        return float(requests.get('https://api2.binance.com/api/v3/ticker/price', params={'symbol':symbol}).json()['price'])

    # find out the BIP-USDT exchange rate on Bithumb
    def get_bithumb_rate(self, symbol: str) -> float:
        return float(requests.get('https://global-openapi.bithumb.pro/openapi/v1/spot/ticker', params={'symbol':symbol}).json()['data'][0]['c'])
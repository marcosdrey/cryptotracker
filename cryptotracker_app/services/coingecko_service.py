import requests
from django.conf import settings


class CoingeckoService:
    def __init__(self):
        self.__base_url = 'https://api.coingecko.com/api/v3/'
        self.__vs_currency_param = 'vs_currency=usd'
        self.__headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": settings.COINGECKO_API_KEY
        }

    def get_coins_market_infos(self) -> list[dict]:
        url = f'{self.__base_url}coins/markets?{self.__vs_currency_param}'
        response = requests.get(url, headers=self.__headers)
        return response.json()

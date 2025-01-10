from celery import shared_task
from services.coingecko_service import CoingeckoService
from .models import CryptocurrencyPrice, Cryptocurrency


@shared_task
def update_cryptos_price():
    if not Cryptocurrency.objects.exists():
        return
    coingecko_service = CoingeckoService()
    data = coingecko_service.get_coins_market_infos()
    for dict_info in data:
        id_crypto = dict_info.get('id')
        try:
            cryptocurrency = Cryptocurrency.objects.get(pk=id_crypto)
            CryptocurrencyPrice.objects.create(
                cryptocurrency=cryptocurrency,
                price=dict_info.get('current_price'),
                price_change_percentage_24h=dict_info.get('price_change_percentage_24h'),
                market_rank=dict_info.get('market_cap_rank')
            )
        except Cryptocurrency.DoesNotExist:
            pass

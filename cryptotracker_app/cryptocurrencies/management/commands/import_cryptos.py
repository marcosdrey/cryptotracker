from django.core.management.base import BaseCommand
from services.coingecko_service import CoingeckoService
from cryptocurrencies.models import Cryptocurrency


class Command(BaseCommand):
    def handle(self, *args, **options):
        coingecko_service = CoingeckoService()
        data = coingecko_service.get_coins_market_infos()
        counter = 0
        for dict_info in data:
            id_crypto = dict_info.get('id')
            name_crypto = dict_info.get('name')
            symbol_crypto = dict_info.get('symbol')
            image_crypto = dict_info.get('image')

            try:
                Cryptocurrency.objects.get(pk=id_crypto)
            except Cryptocurrency.DoesNotExist:
                Cryptocurrency.objects.create(
                    id=id_crypto,
                    name=name_crypto,
                    symbol=symbol_crypto,
                    image=image_crypto
                )
                counter += 1

        self.stdout.write(
            self.style.SUCCESS(f'{str(counter)} novas criptomoedas foram criadas!')
        )

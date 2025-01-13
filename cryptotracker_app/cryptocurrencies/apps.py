from django.apps import AppConfig


class CryptocurrenciesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cryptocurrencies'

    def ready(self):
        import cryptocurrencies.signals  # noqa: F401

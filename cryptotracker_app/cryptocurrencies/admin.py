from django.contrib import admin
from .models import Cryptocurrency, CryptocurrencyAlert, CryptocurrencyPrice


@admin.register(Cryptocurrency)
class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'symbol', 'created_at')
    search_fields = ('name', 'symbol')


@admin.register(CryptocurrencyAlert)
class CryptocurrencyAlertAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'cryptocurrency__name', 'alert_type', 'value')
    search_fields = ('user__username', 'cryptocurrency__name')
    list_filter = ('alert_type', 'value')


@admin.register(CryptocurrencyPrice)
class CryptocurrencyPriceAdmin(admin.ModelAdmin):
    list_display = ('cryptocurrency__name', 'price', 'price_change_percentage_24h', 'timestamp')
    search_fields = ('cryptocurrency__name',)
    list_filter = ('price', 'price_change_percentage_24h')

from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from django.core import serializers
from .models import CryptocurrencyPrice, CryptocurrencyAlert
from services.notify_alert_service import NotifyAlertService


@receiver(post_save, sender=CryptocurrencyPrice)
def send_cryptos_price_webhook(sender, instance, created, **kwargs):
    try:
        if created:
            alerts = CryptocurrencyAlert.objects.filter(
                Q(alert_type='price_above', value__gt=instance.price),
                Q(alert_type='price_below', value__lt=instance.price),
                cryptocurrency=instance.cryptocurrency,
            )
            notify_alert_service = NotifyAlertService()
            data = {
                'event_type': 'create_cryptocurrency_price',
                'cryptocurrency': instance.cryptocurrency.name,
                'price': float(instance.price),
                'timestamp': instance.timestamp.strftime('%Y-%m-%d, %H:%M:%S'),
                'alerts': serializers.serialize('json', alerts),
            }
            notify_alert_service.send_alert(data)
    except:
        pass

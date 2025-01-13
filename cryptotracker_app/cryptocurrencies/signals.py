from django.db.models.signals import post_save
from django.db.models import Q, FloatField
from django.db.models.functions import Cast
from django.utils.timezone import localtime
from django.dispatch import receiver
from .models import CryptocurrencyPrice, CryptocurrencyAlert
from services.notify_alert_service import NotifyAlertService


@receiver(post_save, sender=CryptocurrencyPrice)
def send_cryptos_price_webhook(sender, instance, created, **kwargs):
    try:
        if created:
            alerts = CryptocurrencyAlert.objects.filter(
                Q(cryptocurrency=instance.cryptocurrency),
                Q(alert_type='price_above', value__lt=instance.price) |
                Q(alert_type='price_below', value__gt=instance.price)
            ).annotate(
                alert_value=Cast('value', output_field=FloatField())
            ).values(
                'user__username', 'user__email', 'alert_type', 'alert_value'
            )
            notify_alert_service = NotifyAlertService()
            data = {
                'event_type': 'create_cryptocurrency_price',
                'cryptocurrency': instance.cryptocurrency.name,
                'current_price': float(instance.price),
                'timestamp': localtime(instance.timestamp).strftime('%Y-%m-%d, %H:%M:%S'),
                'alerts': list(alerts),
            }
            notify_alert_service.send_alert(data)
    except:
        pass

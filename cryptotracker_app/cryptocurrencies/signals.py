from django.db.models.signals import post_save
from django.db.models import Q, FloatField
from django.db.models.functions import Cast
from django.utils.timezone import localtime
from django.dispatch import receiver
from .models import CryptocurrencyPrice, CryptocurrencyAlert
from services.notify_alert_service import NotifyAlertService
from notifications.models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def get_alerts(instance):
    alerts = CryptocurrencyAlert.objects.filter(
                Q(cryptocurrency=instance.cryptocurrency),
                Q(alert_type='price_above', value__lt=instance.price) |
                Q(alert_type='price_below', value__gt=instance.price)
            )
    return alerts

@receiver(post_save, sender=CryptocurrencyPrice)
def send_cryptos_price_webhook(sender, instance, created, **kwargs):
    try:
        if created:
            alerts = get_alerts(instance)
            alerts_webhook = alerts.annotate(
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
                'alerts': list(alerts_webhook),
            }
            notify_alert_service.send_alert(data)

            for alert in alerts:
                user = alert.user
                message = f"O preço da criptomoeda {instance.cryptocurrency.name} atingiu o alerta definido ({alert.get_alert_type_display()} {alert.value})"
                Notification.objects.create(
                    message=message,
                    user=user
                )
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"notifications_{user.username}",
                    {
                        "type": "send_notification",
                        "message": message
                    }
                )

    except:  # noqa: E722
        pass

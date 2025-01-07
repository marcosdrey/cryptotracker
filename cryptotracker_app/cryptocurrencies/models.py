import uuid
from django.db import models
from django.contrib.auth.models import User


class Cryptocurrency(models.Model):
    id = models.CharField(max_length=300, primary_key=True)
    name = models.CharField(max_length=500)
    symbol = models.CharField(max_length=50, unique=True)
    image = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.symbol.upper()})'


class CryptocurrencyAlert(models.Model):
    ALERT_TYPES = (
        ('price_above', 'Preço acima de'),
        ('price_below', 'Preço abaixo de'),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, related_name='alerts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPES)
    value = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alerta de '{self.user.username}' para '{self.cryptocurrency.name}'"


class CryptocurrencyPrice(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=20, decimal_places=2)
    price_change_percentage_24h = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.cryptocurrency.symbol}: ${self.price}"

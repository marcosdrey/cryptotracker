# Generated by Django 5.1.4 on 2025-01-08 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocurrencies', '0002_alter_cryptocurrency_symbol'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptocurrencyprice',
            name='market_rank',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
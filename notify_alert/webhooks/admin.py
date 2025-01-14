from django.contrib import admin
from webhooks.models import Webhook


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_type', 'event_text', 'created_at')
    search_fields = ('event_type',)
    list_filter = ('event_type',)

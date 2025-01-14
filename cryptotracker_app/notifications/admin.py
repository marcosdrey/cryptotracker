from django.contrib import admin
from notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'is_read', 'timestamp')
    search_fields = ('user__username', 'message')

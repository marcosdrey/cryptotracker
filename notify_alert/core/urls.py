from django.contrib import admin
from django.urls import path
from webhooks.views import WebhookNotifyAlertView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/alert/', WebhookNotifyAlertView.as_view(), name='webhook_notify_alert')
]

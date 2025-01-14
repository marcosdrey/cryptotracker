from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cryptocurrencies/<str:pk>/', views.CryptocurrencyDetailView.as_view(), name='crypto_detail'),
    path('alerts/<uuid:pk>/update/', views.CryptocurrencyAlertUpdateView.as_view(), name='crypto_alert_update'),
    path('alerts/<uuid:pk>/delete/', views.CryptocurrencyAlertDeleteView.as_view(), name='crypto_alert_delete'),
]

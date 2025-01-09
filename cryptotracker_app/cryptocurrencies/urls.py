from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<str:pk>/', views.CryptocurrencyDetailView.as_view(), name='crypto_detail'),
]

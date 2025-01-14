from django.urls import path
from . import views


urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification_list'),
    path('read/<int:pk>/', views.NotificationReadView.as_view(), name='notification_read'),
    path('delete/<int:pk>/', views.NotificationDeleteView.as_view(), name='notification_delete'),
]

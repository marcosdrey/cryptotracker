from django.views.generic import ListView, View
from notifications.models import Notification
from django.shortcuts import redirect, get_object_or_404


class NotificationListView(ListView):
    context_object_name = 'notifications'
    template_name = 'notifications_list.html'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationReadView(View):

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk == 0:
            notifications = Notification.objects.filter(user=self.request.user)
            if notifications.exists():
                notifications.update(is_read=True)
        else:
            notification = get_object_or_404(Notification, pk=pk)
            if notification.user == self.request.user:
                notification.is_read = True
                notification.save()
        return redirect('notification_list')


class NotificationDeleteView(View):

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk == 0:
            notifications = Notification.objects.filter(user=self.request.user)
            if notifications.exists():
                notifications.delete()
        else:
            notification = get_object_or_404(Notification, pk=pk)
            if notification.user == self.request.user:
                notification.delete()
        return redirect('notification_list')

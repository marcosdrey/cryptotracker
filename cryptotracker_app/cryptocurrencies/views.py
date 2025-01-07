from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cryptocurrency


class HomeView(LoginRequiredMixin, ListView):
    template_name = 'home.html'
    queryset = Cryptocurrency.objects.all()
    context_object_name = 'cryptos'

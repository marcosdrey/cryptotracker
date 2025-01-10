from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import ModelFormMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import CryptocurrencyPrice, Cryptocurrency, CryptocurrencyAlert
from .forms import CryptocurrencyAlertForm


class HomeView(LoginRequiredMixin, ListView):
    template_name = 'home.html'
    context_object_name = 'cryptos_price'

    def get_queryset(self):
        latest_price_subquery = CryptocurrencyPrice.objects.filter(
            cryptocurrency=OuterRef('cryptocurrency')
        ).values('id')[:1]

        latest_prices = CryptocurrencyPrice.objects.filter(
            id__in=Subquery(latest_price_subquery)
        )
        return latest_prices

    def __get_queryset_by_search_method(self, queryset):
        crypto_name = self.request.GET.get('cryptocurrency')
        if crypto_name:
            return queryset.filter(cryptocurrency__name__icontains=crypto_name)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        context['search_queryset'] = self.__get_queryset_by_search_method(queryset)
        if context['search_queryset']:
            search_paginator = Paginator(context['search_queryset'], 5)
            search_page = search_paginator.get_page(self.request.GET.get('search_page'))
            context['search_page'] = search_page

        context['trending_cryptos'] = queryset.order_by('market_rank')[:5]
        context['most_expensive_cryptos'] = queryset.order_by('-price')[:5]
        context['most_devalued_cryptos'] = queryset.order_by('price_change_percentage_24h')[:5]
        context['most_valued_cryptos'] = queryset.order_by('-price_change_percentage_24h')[:5]
        return context


class CryptocurrencyDetailView(LoginRequiredMixin, ModelFormMixin, DetailView):
    model = Cryptocurrency
    template_name = "cryptocurrency_detail.html"
    form_class = CryptocurrencyAlertForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['current_price'] = obj.prices.first()
        context['user_crypto_alerts'] = CryptocurrencyAlert.objects.filter(
            cryptocurrency=obj,
            user=self.request.user
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'cryptocurrency': self.kwargs.get('pk'),
            'user': self.request.user
        }
        return kwargs

    def post(self, request, *args, **kwargs):
        cryptocurrency_id = request.POST.get('cryptocurrency')
        user_id = request.POST.get('user')
        alert_type = request.POST.get('alert_type')
        value = request.POST.get('value')

        CryptocurrencyAlert.objects.create(
            cryptocurrency=get_object_or_404(Cryptocurrency, pk=cryptocurrency_id),
            user=get_object_or_404(User, pk=user_id),
            alert_type=alert_type,
            value=value
        )
        return redirect(request.path)


class CryptocurrencyAlertUpdateView(LoginRequiredMixin, UpdateView):
    model = CryptocurrencyAlert
    template_name = "cryptocurrency_alert_update.html"
    form_class = CryptocurrencyAlertForm

    def get_success_url(self):
        return reverse_lazy('crypto_detail', kwargs={'pk': self.get_object().cryptocurrency.id})


class CryptocurrencyAlertDeleteView(LoginRequiredMixin, DeleteView):
    model = CryptocurrencyAlert
    template_name = "cryptocurrency_alert_delete.html"

    def get_success_url(self):
        return reverse_lazy('crypto_detail', kwargs={'pk': self.get_object().cryptocurrency.id})

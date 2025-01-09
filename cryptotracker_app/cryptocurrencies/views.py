from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CryptocurrencyPrice, Cryptocurrency


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


class CryptocurrencyDetailView(LoginRequiredMixin, DetailView):
    model = Cryptocurrency
    template_name = "cryptocurrency_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['current_price'] = obj.prices.first()
        return context

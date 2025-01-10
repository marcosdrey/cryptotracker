from django import forms
from .models import CryptocurrencyAlert


class CryptocurrencyAlertForm(forms.ModelForm):
    class Meta:
        model = CryptocurrencyAlert
        fields = '__all__'
        widgets = {
            'alert_type': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'cryptocurrency': forms.HiddenInput(),
            'user': forms.HiddenInput()
        }
        labels = {
            'alert_type': 'Tipo de Alerta',
            'value': 'Valor'
        }

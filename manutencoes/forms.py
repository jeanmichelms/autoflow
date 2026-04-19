from calendar import monthrange
from datetime import date

from django import forms
from .models import Manutencao


HTML5_DATE_FORMAT = '%Y-%m-%d'


def add_months(base_date, months):
    month = base_date.month - 1 + months
    year = base_date.year + month // 12
    month = month % 12 + 1
    day = min(base_date.day, monthrange(year, month)[1])
    return date(year, month, day)


class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = [
            'veiculo',
            'descricao',
            'data_manutencao',
            'data_proxima_manutencao',
            'quilometragem',
            'valor',
            'observacoes',
        ]
        labels = {
            'veiculo': 'Veículo',
            'descricao': 'Descrição',
            'data_manutencao': 'Data da manutenção',
            'data_proxima_manutencao': 'Data prevista da próxima manutenção',
            'observacoes': 'Observações',
        }
        widgets = {
            'veiculo': forms.HiddenInput(),
            'descricao': forms.Textarea(attrs={'rows': 5, 'style': 'width: 100%; box-sizing: border-box;'}),
            'data_manutencao': forms.DateInput(format=HTML5_DATE_FORMAT, attrs={'type': 'date'}),
            'data_proxima_manutencao': forms.DateInput(format=HTML5_DATE_FORMAT, attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 5, 'style': 'width: 100%; box-sizing: border-box;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['veiculo'].required = True
        self.fields['data_manutencao'].input_formats = [HTML5_DATE_FORMAT]
        self.fields['data_proxima_manutencao'].input_formats = [HTML5_DATE_FORMAT]

        if not self.is_bound and not getattr(self.instance, 'pk', None):
            hoje = date.today()
            self.initial.setdefault('data_manutencao', hoje.strftime(HTML5_DATE_FORMAT))
            self.initial.setdefault('data_proxima_manutencao', add_months(hoje, 6).strftime(HTML5_DATE_FORMAT))

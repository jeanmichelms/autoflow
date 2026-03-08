from django import forms
from .models import Veiculo


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['cliente', 'marca', 'modelo', 'ano', 'placa', 'cor', 'chassi']
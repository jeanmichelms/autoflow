from django import forms
from .models import Veiculo


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['cliente', 'marca', 'modelo', 'ano', 'placa', 'cor', 'chassi']
        widgets = {
            'cliente': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].required = True

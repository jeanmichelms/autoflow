from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Veiculo
from .forms import VeiculoForm


class VeiculoListView(ListView):
    model = Veiculo
    template_name = 'veiculos/lista.html'
    context_object_name = 'veiculos'


class VeiculoCreateView(CreateView):
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'veiculos/form.html'
    success_url = reverse_lazy('veiculos_lista')


class VeiculoUpdateView(UpdateView):
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'veiculos/form.html'
    success_url = reverse_lazy('veiculos_lista')


class VeiculoDeleteView(DeleteView):
    model = Veiculo
    template_name = 'veiculos/confirmar_exclusao.html'
    success_url = reverse_lazy('veiculos_lista')


class VeiculoDetailView(DetailView):
    model = Veiculo
    template_name = 'veiculos/detalhe.html'
    context_object_name = 'veiculo'
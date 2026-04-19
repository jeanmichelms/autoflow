from datetime import date

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .forms import ManutencaoForm, add_months
from .models import Manutencao


class ManutencaoListView(ListView):
    model = Manutencao
    template_name = 'manutencoes/lista.html'
    context_object_name = 'manutencoes'


class ManutencaoCreateView(CreateView):
    model = Manutencao
    form_class = ManutencaoForm
    template_name = 'manutencoes/form.html'
    success_url = reverse_lazy('manutencoes_lista')

    def get_initial(self):
        initial = super().get_initial()
        hoje = date.today()
        initial.setdefault('data_manutencao', hoje)
        initial.setdefault('data_proxima_manutencao', add_months(hoje, 6))
        return initial


class ManutencaoUpdateView(UpdateView):
    model = Manutencao
    form_class = ManutencaoForm
    template_name = 'manutencoes/form.html'
    success_url = reverse_lazy('manutencoes_lista')


class ManutencaoDeleteView(DeleteView):
    model = Manutencao
    template_name = 'manutencoes/confirmar_exclusao.html'
    success_url = reverse_lazy('manutencoes_lista')


class ManutencaoDetailView(DetailView):
    model = Manutencao
    template_name = 'manutencoes/detalhe.html'
    context_object_name = 'manutencao'

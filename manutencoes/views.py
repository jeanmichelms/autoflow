from datetime import date

from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from veiculos.models import Veiculo
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

    def get_success_url(self):
        veiculo_id = self.request.GET.get('veiculo')
        origem = self.request.GET.get('origem')

        if origem == 'veiculo_detalhe' and veiculo_id and veiculo_id.isdigit():
            return reverse('veiculos_detalhe', kwargs={'pk': int(veiculo_id)})

        return str(self.success_url)

    def get_initial(self):
        initial = super().get_initial()
        hoje = date.today()
        initial.setdefault('data_manutencao', hoje)
        initial.setdefault('data_proxima_manutencao', add_months(hoje, 6))

        veiculo_id = self.request.GET.get('veiculo')
        if veiculo_id and veiculo_id.isdigit():
            try:
                initial['veiculo'] = Veiculo.objects.select_related('cliente').get(pk=int(veiculo_id))
            except Veiculo.DoesNotExist:
                pass

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        veiculo_id = self.request.GET.get('veiculo')
        selected_veiculo = None

        if self.request.method == 'GET' and veiculo_id and veiculo_id.isdigit():
            selected_veiculo = Veiculo.objects.select_related('cliente').filter(pk=int(veiculo_id)).first()

        context['selected_veiculo'] = selected_veiculo
        context['cancel_url'] = (
            reverse('veiculos_detalhe', kwargs={'pk': int(veiculo_id)})
            if self.request.GET.get('origem') == 'veiculo_detalhe' and veiculo_id and veiculo_id.isdigit()
            else reverse('manutencoes_lista')
        )
        return context


class ManutencaoUpdateView(UpdateView):
    model = Manutencao
    form_class = ManutencaoForm
    template_name = 'manutencoes/form.html'
    success_url = reverse_lazy('manutencoes_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse('manutencoes_lista')
        return context


class ManutencaoDeleteView(DeleteView):
    model = Manutencao
    template_name = 'manutencoes/confirmar_exclusao.html'
    success_url = reverse_lazy('manutencoes_lista')


class ManutencaoDetailView(DetailView):
    model = Manutencao
    template_name = 'manutencoes/detalhe.html'
    context_object_name = 'manutencao'


class VeiculoBuscaView(View):
    def get(self, request, *args, **kwargs):
        filtro = (request.GET.get('q') or '').strip()
        veiculos = Veiculo.objects.select_related('cliente').all()

        if filtro:
            condicao = (
                Q(cliente__nome__icontains=filtro)
                | Q(cliente__cpf__icontains=filtro)
                | Q(marca__icontains=filtro)
                | Q(modelo__icontains=filtro)
                | Q(placa__icontains=filtro)
            )

            if filtro.isdigit():
                condicao |= Q(ano=int(filtro))

            veiculos = veiculos.filter(condicao)

        veiculos = veiculos.order_by('cliente__nome', 'marca', 'modelo', 'placa')[:50]

        resultados = [
            {
                'id': veiculo.id,
                'cliente_nome': veiculo.cliente.nome,
                'cliente_cpf': veiculo.cliente.cpf,
                'marca': veiculo.marca,
                'modelo': veiculo.modelo,
                'ano': veiculo.ano,
                'placa': veiculo.placa,
            }
            for veiculo in veiculos
        ]

        return JsonResponse({'results': resultados})

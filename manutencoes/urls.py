from django.urls import path
from .views import (
    ManutencaoListView,
    ManutencaoCreateView,
    ManutencaoUpdateView,
    ManutencaoDeleteView,
    ManutencaoDetailView,
    VeiculoBuscaView,
)

urlpatterns = [
    path('', ManutencaoListView.as_view(), name='manutencoes_lista'),
    path('novo/', ManutencaoCreateView.as_view(), name='manutencoes_novo'),
    path('buscar-veiculos/', VeiculoBuscaView.as_view(), name='manutencoes_buscar_veiculos'),
    path('<int:pk>/', ManutencaoDetailView.as_view(), name='manutencoes_detalhe'),
    path('<int:pk>/editar/', ManutencaoUpdateView.as_view(), name='manutencoes_editar'),
    path('<int:pk>/excluir/', ManutencaoDeleteView.as_view(), name='manutencoes_excluir'),
]

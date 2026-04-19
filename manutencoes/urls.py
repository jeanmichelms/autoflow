from django.urls import path
from .views import (
    ManutencaoListView,
    ManutencaoCreateView,
    ManutencaoUpdateView,
    ManutencaoDeleteView,
    ManutencaoDetailView,
)

urlpatterns = [
    path('', ManutencaoListView.as_view(), name='manutencoes_lista'),
    path('novo/', ManutencaoCreateView.as_view(), name='manutencoes_novo'),
    path('<int:pk>/', ManutencaoDetailView.as_view(), name='manutencoes_detalhe'),
    path('<int:pk>/editar/', ManutencaoUpdateView.as_view(), name='manutencoes_editar'),
    path('<int:pk>/excluir/', ManutencaoDeleteView.as_view(), name='manutencoes_excluir'),
]

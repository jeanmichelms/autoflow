from django.contrib import admin
from .models import Manutencao


@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'veiculo', 'descricao', 'data_manutencao', 'quilometragem', 'valor')
    search_fields = ('descricao', 'veiculo__marca', 'veiculo__modelo', 'veiculo__placa')
    list_filter = ('data_manutencao',)

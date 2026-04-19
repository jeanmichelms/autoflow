from django.db import models
from veiculos.models import Veiculo


class Manutencao(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='manutencoes')
    descricao = models.TextField()
    data_manutencao = models.DateField()
    quilometragem = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True, null=True)
    data_proxima_manutencao = models.DateField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_manutencao', '-id']
        verbose_name = 'Manutenção'
        verbose_name_plural = 'Manutenções'

    def __str__(self):
        return f'{self.veiculo} - {self.descricao} ({self.data_manutencao})'

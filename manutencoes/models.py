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
    email_aviso_revisao_enviado = models.BooleanField(default=False, editable=False)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_manutencao', '-id']
        verbose_name = 'Manutenção'
        verbose_name_plural = 'Manutenções'

    def __str__(self):
        return f'{self.veiculo} - {self.descricao} ({self.data_manutencao})'

    def save(self, *args, **kwargs):
        if self.pk:
            data_anterior = (
                Manutencao.objects
                .filter(pk=self.pk)
                .values_list('data_proxima_manutencao', flat=True)
                .first()
            )

            if data_anterior != self.data_proxima_manutencao:
                self.email_aviso_revisao_enviado = False
                update_fields = kwargs.get('update_fields')
                if update_fields is not None:
                    kwargs['update_fields'] = set(update_fields) | {
                        'email_aviso_revisao_enviado',
                    }

        super().save(*args, **kwargs)

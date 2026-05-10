from datetime import date, timedelta

from django.core import mail
from django.test import TestCase, override_settings

from clientes.models import Cliente
from veiculos.models import Veiculo

from .hosted_service import enviar_avisos_revisao
from .models import Manutencao


@override_settings(
    AVISO_REVISAO_EMAIL_DIAS_ANTECEDENCIA=3,
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    DEFAULT_FROM_EMAIL='teste@autoflow.local',
)
class AvisoRevisaoEmailTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome='Maria Silva',
            cpf='123.456.789-10',
            email='maria@example.com',
        )
        self.veiculo = Veiculo.objects.create(
            cliente=self.cliente,
            marca='Fiat',
            modelo='Uno',
            ano=2020,
            placa='ABC1D23',
        )

    def test_envia_email_e_marca_manutencao_como_enviada(self):
        data_base = date(2026, 5, 10)
        manutencao = self._criar_manutencao(data_base + timedelta(days=3))

        resultado = enviar_avisos_revisao(data_base=data_base)

        manutencao.refresh_from_db()
        self.assertEqual(resultado.encontrados, 1)
        self.assertEqual(resultado.enviados, 1)
        self.assertEqual(resultado.falhas, 0)
        self.assertTrue(manutencao.email_aviso_revisao_enviado)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['maria@example.com'])
        self.assertIn('13/05/2026', mail.outbox[0].body)

    def test_nao_reenvia_email_ja_marcado_como_enviado(self):
        data_base = date(2026, 5, 10)
        self._criar_manutencao(
            data_base + timedelta(days=3),
            email_aviso_revisao_enviado=True,
        )

        resultado = enviar_avisos_revisao(data_base=data_base)

        self.assertEqual(resultado.encontrados, 0)
        self.assertEqual(resultado.enviados, 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_nao_envia_email_fora_da_data_alvo(self):
        data_base = date(2026, 5, 10)
        self._criar_manutencao(data_base + timedelta(days=4))

        resultado = enviar_avisos_revisao(data_base=data_base)

        self.assertEqual(resultado.encontrados, 0)
        self.assertEqual(resultado.enviados, 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_alterar_data_proxima_manutencao_reseta_indicador_de_envio(self):
        manutencao = self._criar_manutencao(
            date(2026, 5, 13),
            email_aviso_revisao_enviado=True,
        )

        manutencao.data_proxima_manutencao = date(2026, 6, 13)
        manutencao.save(update_fields=['data_proxima_manutencao'])

        manutencao.refresh_from_db()
        self.assertFalse(manutencao.email_aviso_revisao_enviado)

    def _criar_manutencao(self, data_proxima_manutencao, **kwargs):
        dados = {
            'veiculo': self.veiculo,
            'descricao': 'Revisão preventiva',
            'data_manutencao': date(2026, 1, 10),
            'quilometragem': 10000,
            'valor': '250.00',
            'data_proxima_manutencao': data_proxima_manutencao,
        }
        dados.update(kwargs)
        return Manutencao.objects.create(**dados)

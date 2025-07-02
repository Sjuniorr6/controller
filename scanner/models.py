from django.db import models

class Equipamento(models.Model):
    codigo = models.CharField(max_length=100)
    data_recebido = models.DateTimeField(auto_now_add=True)
    peso_liquido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    peso_bruto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    medidas_caixa = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.codigo
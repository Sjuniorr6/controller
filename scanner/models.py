from django.db import models

class Equipamento(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    data_recebido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo
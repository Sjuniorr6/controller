from django.db import models

class CodigoEscaneado(models.Model):
    codigo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo

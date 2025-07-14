from django.db import models
from django.contrib.auth.models import User

class Equipamento(models.Model):
    TIPO_CHOICES = [
        ('guardian', 'Guardian'),
        ('sensor_porta', 'Sensor de Porta'),
        ('tetis', 'Tetis'),
    ]
    
    codigo = models.CharField(max_length=100)
    tipo_equipamento = models.CharField(max_length=20, choices=TIPO_CHOICES, default='tetis')
    data_recebido = models.DateTimeField(auto_now_add=True)
    peso_liquido = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    peso_bruto = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    medidas_caixa = models.CharField(max_length=200, null=True, blank=True)
    usuario_cadastro = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipamentos_cadastrados', default=1)

    def determinar_tipo_equipamento(self):
        """Determina o tipo de equipamento baseado no código"""
        if self.codigo.startswith('8373'):
            return 'guardian'
        elif self.codigo.startswith('8304'):
            return 'sensor_porta'
        else:
            return 'tetis'
    
    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"
        ordering = ['-data_recebido']
        permissions = [
            ("can_access_scanner", "Pode acessar o scanner"),
            ("can_access_eventos",  "Pode acessar eventos"),  # <-- nova permissão
        ]

    def save(self, *args, **kwargs):
        # Determina automaticamente o tipo antes de salvar
        self.tipo_equipamento = self.determinar_tipo_equipamento()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.get_tipo_equipamento_display()}"

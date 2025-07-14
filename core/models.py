from django.db import models
from django.db import models
from django.utils.timezone import now


# Create your models here.
class altocafezalmodel(models.Model):
    nome           = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro  = models.DateTimeField(default=now, editable=False)
    
    class Meta:
        verbose_name = "Alto Cafezal"
        verbose_name_plural = "Alto Cafezal"
        permissions = [
            ("can_access_mapa", "Pode acessar o mapa"),
        ]
    
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"






class burbomcofelmodel(models.Model):
    nome           = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro  = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"
    
    
    
    
    
class carmocofelmodel(models.Model):
    nome           = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro  = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"
    
    
    
    
    
class expocacermodel(models.Model):
    nome           = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro  = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"
    
    



class coxupemodel(models.Model):
    nome           = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro  = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"
    





class nkgmodel(models.Model):
    nome           = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro  = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"
    



class velosocofemodel(models.Model):
    nome           = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro  = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"
    


class velosogreenmodel(models.Model):
    nome           = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro  = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"




class volcafemodel(models.Model):
    nome           = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro  = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"
    
    
class EventoTratado(models.Model):
    """
    Armazena cada alerta gerado pela task Celery.
    Ex.: tipo_evento = "door" | "light" | "error"
    """
    guid             = models.CharField(max_length=255)
    tipo_evento      = models.CharField(max_length=20)
    valor            = models.FloatField(null=True, blank=True)
    criado_em        = models.DateTimeField(auto_now_add=True)
    alerta_disparado = models.BooleanField(default=False)
    
    # Status do evento
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('tratado', 'Tratado'),
        ('ignorado', 'Ignorado'),
    ], default='pendente')
    
    # Campos para tratamento
    tratado_em  = models.DateTimeField(null=True, blank=True)
    tratado_por = models.CharField(max_length=100, null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)
    acao_tomada = models.CharField(max_length=50, choices=[
        ('verificado', 'Verificado'),
        ('corrigido', 'Corrigido'),
        ('ignorado', 'Ignorado'),
        ('escalado', 'Escalado'),
        ('outro', 'Outro')
    ], null=True, blank=True)
    
    class Meta:
        ordering = ["-criado_em"]
        indexes  = [models.Index(fields=["criado_em"])]
        permissions = [
            ("can_access_eventos", "Pode acessar eventos"),
        ]

    def __str__(self) -> str:
        return f"{self.tipo_evento.upper()} – {self.guid} ({self.get_status_display()})"
    
    def marcar_como_tratado(self, tratado_por, observacoes=None, acao_tomada=None):
        """Marca o evento como tratado"""
        from django.utils.timezone import now
        self.alerta_disparado = True
        self.status = 'tratado'
        self.tratado_em = now()
        self.tratado_por = tratado_por
        if observacoes:
            self.observacoes = observacoes
        if acao_tomada:
            self.acao_tomada = acao_tomada
        self.save()

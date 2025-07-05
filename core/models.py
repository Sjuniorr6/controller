from django.db import models
from django.db import models
from django.utils.timezone import now


# Create your models here.
class altocafezalmodel(models.Model):
    nome = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"






class burbomcofelmodel(models.Model):
    nome = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"
    
    
    
    
    
class carmocofelmodel(models.Model):
    nome = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"
    
    
    
    
    
class expocacermodel(models.Model):
    nome = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"
    
    



class coxupemodel(models.Model):
    nome = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"
    





class nkgmodel(models.Model):
    nome = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"
    



class velosocofemodel(models.Model):
    nome = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"
    


class velosogreenmodel(models.Model):
    nome = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"




class volcafemodel(models.Model):
    nome = models.CharField(max_length=100000)
    id_equipamento = models.CharField(max_length=100000)  # Removido `unique=True`
    data_registro = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.id_equipamento} - {self.nome}"
    
    
class EventoTratado(models.Model):
    """
    Armazena cada alerta gerado pela task Celery.
    Ex.: tipo_evento = "door" | "light" | "error"
    """
    guid        = models.CharField(max_length=255)
    tipo_evento = models.CharField(max_length=20)
    valor       = models.FloatField(null=True, blank=True)
    criado_em   = models.DateTimeField(auto_now_add=True)
    alerta_disparado = models.BooleanField(default=False) 
    class Meta:
        ordering = ["-criado_em"]
        indexes  = [models.Index(fields=["criado_em"])]

    def __str__(self) -> str:
        return f"{self.tipo_evento.upper()} – {self.guid}"
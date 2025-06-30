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
    
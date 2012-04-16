from django.db import models

# Create your models here.
class CadastroUsuario(models.Model):
    nome = models.CharField(max_length=60)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100,unique=True)
    conta_twitter = models.CharField(max_length=30, blank=True)
    
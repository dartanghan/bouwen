from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class empresa(models.Model):
    empresa_nome = models.CharField(max_length=255)
    empresa_cnpj = models.CharField(max_length=20)
    empresa_endereco = models.CharField(max_length=255)
    empresa_email = models.CharField(max_length=255)
    empresa_telefone = models.CharField(max_length=20)

class usuario(User):
    empresa = models.ForeignKey('empresa',on_delete=models.CASCADE)


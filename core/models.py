from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.
class empresa(models.Model):
    """
    Tudo gira em torno de uma empresa...
    Os controles dos usuários, ativos de rede, lançamentos e créditos
    ficarão todos amarrados à uma empresa....
    """
    empresa_nome = models.CharField(max_length=255)
    empresa_cnpj = models.CharField(max_length=20)
    empresa_endereco = models.CharField(max_length=255)
    empresa_email = models.CharField(max_length=255,blank=True)
    empresa_telefone = models.CharField(max_length=20,blank=True)
    empresa_saldo_creditos = models.DecimalField(max_digits=10,decimal_places=1,default=0)
    def __str__(self):
        return self.empresa_nome

class usuario(User):
    empresa = models.ForeignKey('empresa',on_delete=models.CASCADE)

class credito(models.Model):
    """
    Unidade básica de trabalho. Tudo custa crédito.
    Crédito será a unidade mínima de cobrança de algo.
    - Credito foi comprado por uma empresa
    - Credito é uma unidade
    """
    empresa_compradora = models.ForeignKey("empresa",on_delete=models.CASCADE)
    credito_finalizado = models.BooleanField(default=False)
    credito_parcialmente_finalizado = models.BooleanField(default=False)
    credito_valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    credito_dt_aquisicao = models.DateTimeField(auto_now_add=True)
    credito_dt_vencimento = models.DateTimeField(blank=True,null=True)

class credito_usado(models.Model):
    empresa_debitada = models.ForeignKey("empresa",related_name='empresa_debitada',on_delete=models.CASCADE) #empresa que sera debitada
    empresa_creditada = models.ForeignKey('empresa',related_name='empresa_creditada',on_delete=models.CASCADE) #empresa que trabalhou
    credito = models.ForeignKey('credito',on_delete=models.CASCADE) #credito que sera consumido
    credito_usado_dt = models.DateTimeField(auto_now=True)
    credito_usado_parcial = models.BooleanField(default=False) #indica se metade do credito foi consumido

    def save(self, *args, **kwargs):
        """Ao salvar um consumo, ja debitamos da empresa do saldo e baixar o credito"""
        # Credito ja usado nao vale...
        if self.credito.credito_finalizado:
            return False
        # Credito menor do que a unidade consumida...            
        if self.credito.credito_parcialmente_finalizado and not self.credito_usado_parcial:
            return False


        if self.credito_usado_parcial:
            # Baixando o saldo...
            self.empresa_debitada.empresa_saldo_creditos = self.empresa_debitada.empresa_saldo_creditos - Decimal(0.5)
            if not self.credito.credito_parcialmente_finalizado:
                # parte do credito consumido
                self.credito.credito_parcialmente_finalizado = True
            else:
                # so tinha um pedaco, agora zera...
                self.credito.credito_finalizado = True    
        else:
            # Baixando o saldo...
            self.empresa_debitada.empresa_saldo_creditos = self.empresa_debitada.empresa_saldo_creditos - 1 
            # Finalizando? 
            self.credito.credito_finalizado = True
        self.credito.save()
        self.empresa_debitada.save()
        super(credito_usado, self).save(*args, **kwargs)
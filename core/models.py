from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import datetime,timedelta
from django.db.models import Max

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
    
    def creditos_get(self, creditos_ativos:bool):
        """ Retorna a lista de credito disponiveis """
        creditos = credito.objects.filter(empresa_compradora=self)
        if creditos_ativos is not None and creditos_ativos == True:
            creditos = creditos.filter(credito_finalizado=False)
        elif creditos_ativos is not None and creditos_ativos == False:
            creditos = creditos.filter(credito_finalizado=True)
        return creditos

    def creditos_processa(self,dt_inicio:datetime,forcar_reprocessamento:bool=False):
        """
         Processa os consumos da empresa
        :param forcar_reprocessamento:bool informa se temos que reativar os creditos e recalcular tudo
        """
        if forcar_reprocessamento: ## reativar todos os creditos
            credito.objects.filter(empresa_compradora=self).update(credito_finalizado=False,credito_parcialmente_finalizado=False)
            credito_usado.objects.all().delete() #remove consumos
        dt_processamento = dt_inicio
        while dt_processamento < datetime.now():
            # works feitos na hora do processamento
            trabalhos_executados = workbox.objects.filter(w_empresa=self,w_creditos__gte=1,w_inicio__gte=dt_processamento,w_inicio__lt= dt_processamento + timedelta(hours=1))
            for trabalho in trabalhos_executados:
                creditos_para_consumir = trabalho.w_creditos
                while creditos_para_consumir > 0: # se o trabalho exige 2 creditos por hora, por ex.
                    creus = credito_usado(
                        empresa_creditada=trabalho.w_usuario.empresa,
                        credito=self.creditos_get(True)[0],
                        credito_usado_dt = dt_processamento,
                        credito_usado_parcial = False # TODO ainda nao calcula parcial
                    )
                    creus.save()
                    creditos_para_consumir = creditos_para_consumir - 1
            # vamos para proxima hora
            dt_processamento = dt_processamento + timedelta(hours=1)
            

            
        


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
            if not self.credito.credito_parcialmente_finalizado:
                # parte do credito consumido
                self.credito.credito_parcialmente_finalizado = True
            else:
                # so tinha um pedaco, agora zera...
                self.credito.credito_finalizado = True    
        else:
            # Baixando o saldo...
            # Finalizando? 
            self.credito.credito_finalizado = True
        self.credito.save()
        super(credito_usado, self).save(*args, **kwargs)

class workbox(models.Model):
    w_inicio = models.DateTimeField(default=datetime.now)
    w_fim = models.DateTimeField(default=datetime.now)
    w_titulo = models.CharField(max_length=200)
    w_descricao = models.TextField()
    w_creditos = models.IntegerField(default=1)
    w_empresa = models.ForeignKey(empresa,on_delete=models.CASCADE)
    w_usuario = models.ForeignKey(usuario,on_delete=models.CASCADE)
    def __str__(self):
        return "%s - %s =>  %s"%(
            self.w_inicio.astimezone().strftime( '%d/%m/%y %H:%M'),
            self.w_fim.astimezone().strftime( '%d/%m/%y %H:%M'),
            self.w_titulo)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.w_inicio=workbox.objects.filter(w_usuario=self.w_usuario).aggregate(Max('w_fim'))['w_fim__max']
            if not self.w_inicio:
                self.w_inicio = datetime.strptime('2023-01-01','%Y-%m-%d')
        super(workbox, self).save(*args, **kwargs)

    class Meta:
        ordering = ['w_inicio']

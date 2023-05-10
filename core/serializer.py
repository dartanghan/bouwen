from rest_framework import serializers
from .models import usuario,empresa,credito,credito_usado,workbox

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = usuario
        fields = ['username', 'email', 'empresa']

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = empresa
        fields = ['empresa_nome', 'empresa_cnpj', 'empresa_email','empresa_saldo_creditos']

class CreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = credito
        fields = ['empresa_compradora', 'credito_valor_pago', 'credito_dt_aquisicao', 'credito_dt_vencimento', 'credito_finalizado']

class CreditoUsadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = credito_usado
        fields = ['credito', 'credito_usado_dt', 'credito_usado_parcial']

class WorkboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = workbox
        fields = ['w_inicio', 'w_fim', 'w_titulo', 'w_creditos', 'w_usuario']



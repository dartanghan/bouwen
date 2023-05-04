from django.contrib import admin
from .models import usuario,empresa,credito,credito_usado
# Register your models here.

class usuarioAdmin(admin.ModelAdmin):
    def empresa_nome(self,obj):
        return obj.empresa.empresa_nome
    list_display=['username','email','empresa_nome']

class empresaAdmin(admin.ModelAdmin):
    list_display = ['empresa_nome','empresa_cnpj','empresa_email']

class creditoAdmin(admin.ModelAdmin):
    def empresa_nome(self,obj):
        return obj.empresa_compradora.empresa_nome
    list_display = ['empresa_nome','credito_valor_pago','credito_dt_aquisicao','credito_dt_vencimento','credito_finalizado']



admin.site.register(usuario,usuarioAdmin)
admin.site.register(empresa,empresaAdmin)
admin.site.register(credito,creditoAdmin)
admin.site.register(credito_usado)
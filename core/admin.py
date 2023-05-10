from django.contrib import admin
from .models import usuario,empresa,credito,credito_usado,workbox
from datetime import datetime
# Register your models here.


@admin.action(description="Processa creditos")
def processa_creditos(modeladmin, request, queryset):
    for emp in queryset:
        emp.creditos_processa(datetime.strptime('2023-05-01','%Y-%m-%d'),forcar_reprocessamento=True)

class usuarioAdmin(admin.ModelAdmin):
    def empresa_nome(self,obj):
        return obj.empresa.empresa_nome
    list_display=['username','email','empresa_nome']

class empresaAdmin(admin.ModelAdmin):
    list_display = ['empresa_nome','empresa_cnpj','empresa_email','empresa_saldo_creditos']
    actions = [processa_creditos]

class creditoAdmin(admin.ModelAdmin):
    def empresa_nome(self,obj):
        return obj.empresa_compradora.empresa_nome
    list_display = ['empresa_nome','credito_valor_pago','credito_dt_aquisicao','credito_dt_vencimento','credito_finalizado']

class creditoUsadoAdmin(admin.ModelAdmin):
    list_display = ['credito__empresa','credito__credito_finalizado','credito_usado_dt','credito_usado_parcial']

class workboxAdmin(admin.ModelAdmin):
    list_display = ['w_inicio','w_fim','w_titulo','w_creditos','w_usuario']

admin.site.register(workbox,workboxAdmin)
admin.site.register(usuario,usuarioAdmin)
admin.site.register(empresa,empresaAdmin)
admin.site.register(credito,creditoAdmin)
admin.site.register(credito_usado,creditoUsadoAdmin)


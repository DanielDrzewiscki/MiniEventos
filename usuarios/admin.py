from django.contrib import admin

from .models import Cliente2,Contrato2,Pagos2,SumaContrato2,ActualizacionContrato2,SumaActualizacion2,Tarjeta,Menu,ServicioContratado

# Register your models here.

class TarjetaAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

admin.site.register(Tarjeta, TarjetaAdmin)



admin.site.register([Cliente2, Contrato2,Pagos2,SumaContrato2,ActualizacionContrato2,SumaActualizacion2,Menu,ServicioContratado])
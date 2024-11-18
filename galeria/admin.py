from django.contrib import admin
from galeria.models import Sector,Detalle

# Register your models here.

class AdminGaleria(admin.ModelAdmin):
    readonly_fields=('created','updated')

admin.site.register(Sector, AdminGaleria)

class AdminDetalle(admin.ModelAdmin):
    readonly_fields=('created','updated')

admin.site.register(Detalle, AdminDetalle)
from django.contrib import admin
from .models import Tablas,Pagina,Usuarioregistrado,FamiliaMenu,CartaMenu,TipoMenu,ModalidadMenu


# Register your models here.

class TablasAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

admin.site.register(Tablas, TablasAdmin)

class PaginaAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

admin.site.register(Pagina, PaginaAdmin)

   
admin.site.register([Usuarioregistrado, FamiliaMenu, CartaMenu,TipoMenu,ModalidadMenu])
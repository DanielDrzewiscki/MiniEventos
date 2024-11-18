from django.contrib import admin
from servicios.models import Servicio,Item

# Register your models here.

class AdminServicio(admin.ModelAdmin):
    readonly_fields=('created','updated')

admin.site.register(Servicio, AdminServicio)

class ItemAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

admin.site.register(Item, ItemAdmin)
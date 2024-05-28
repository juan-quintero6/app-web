from django.contrib import admin
from .models import Perfil, Conductor, Cliente, Administrador

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo')
    list_filter = ('tipo',)

class ConductorAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'get_tipo')
    
    def get_tipo(self, obj):
        return obj.perfil.tipo
    get_tipo.short_description = 'Tipo de Perfil'

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'get_tipo')
    
    def get_tipo(self, obj):
        return obj.perfil.tipo
    get_tipo.short_description = 'Tipo de Perfil'

class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'get_tipo')
    
    def get_tipo(self, obj):
        return obj.perfil.tipo
    get_tipo.short_description = 'Tipo de Perfil'

admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Conductor, ConductorAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Administrador, AdministradorAdmin)

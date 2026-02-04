#Configuración del panel de administración para los modelos del restaurante.
from django.contrib import admin
from .models import Mesa, Pedido


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Mesa."""
    list_display = ('numero', 'capacidad', 'estado', 'created_at')
    list_filter = ('estado',)
    search_fields = ('numero',)
    ordering = ('numero',)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Pedido."""
    list_display = ('id', 'mesa', 'estado', 'total', 'created_at')
    list_filter = ('estado', 'mesa')
    search_fields = ('descripcion',)
    ordering = ('-created_at',)
    raw_id_fields = ('mesa',)


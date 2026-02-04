"""
Serializadores para los modelos del restaurante.
"""

from rest_framework import serializers
from .models import Mesa, Pedido


class BaseSerializer(serializers.ModelSerializer):
    """
    Serializador base con campos comunes (DRY).
    Proporciona campos de solo lectura para timestamps.
    """
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class MesaSerializer(BaseSerializer):
    """
    Serializador para el modelo Mesa.
    """
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    total_pedidos = serializers.SerializerMethodField()

    class Meta:
        model = Mesa
        fields = [
            'id', 'numero', 'capacidad', 'estado', 'estado_display',
            'total_pedidos', 'created_at', 'updated_at'
        ]

    def get_total_pedidos(self, obj):
        """Retorna el número total de pedidos de la mesa."""
        return obj.pedidos.count()


class MesaSimpleSerializer(serializers.ModelSerializer):
    """
    Serializador simplificado de Mesa para usar en relaciones anidadas.
    """
    class Meta:
        model = Mesa
        fields = ['id', 'numero', 'estado']


class PedidoSerializer(BaseSerializer):
    """
    Serializador para el modelo Pedido.
    """
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    mesa_info = MesaSimpleSerializer(source='mesa', read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'id', 'mesa', 'mesa_info', 'descripcion', 'total',
            'estado', 'estado_display', 'created_at', 'updated_at'
        ]


class PedidoCreateSerializer(serializers.ModelSerializer):
    """
    Serializador para crear/actualizar pedidos.
    """
    class Meta:
        model = Pedido
        fields = ['id', 'mesa', 'descripcion', 'total', 'estado']

    def validate_total(self, value):
        """Valida que el total no sea negativo."""
        if value < 0:
            raise serializers.ValidationError("El total no puede ser negativo.")
        return value


class MesaPedidosSerializer(serializers.ModelSerializer):
    """
    Serializador para mostrar una mesa con todos sus pedidos.
    Usado en la api_view personalizada.
    """
    pedidos = PedidoSerializer(many=True, read_only=True)
    total_pedidos = serializers.SerializerMethodField()
    total_facturado = serializers.SerializerMethodField()
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = Mesa
        fields = [
            'id', 'numero', 'capacidad', 'estado', 'estado_display',
            'pedidos', 'total_pedidos', 'total_facturado',
            'created_at', 'updated_at'
        ]

    def get_total_pedidos(self, obj):
        """Retorna el número total de pedidos de la mesa."""
        return obj.pedidos.count()

    def get_total_facturado(self, obj):
        """Retorna el total facturado de todos los pedidos de la mesa."""
        return sum(pedido.total for pedido in obj.pedidos.all())


from django.db.models import Sum, Count
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Mesa, Pedido
from .serializers import (
    MesaSerializer, PedidoSerializer, PedidoCreateSerializer,
    MesaPedidosSerializer
)
from .permissions import CanDeletePermission, IsAdminGroup

class MesaListView(generics.ListAPIView):
    """
    Vista genérica para listar todas las mesas.
    GET /api/mesas/
    """
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer
    permission_classes = [IsAuthenticated]


class MesaCreateView(generics.CreateAPIView):
    """
    Vista genérica para crear una nueva mesa.
    POST /api/mesas/create/
    """
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer
    permission_classes = [IsAuthenticated]


class MesaRetrieveView(generics.RetrieveAPIView):
    """
    Vista genérica para obtener el detalle de una mesa.
    GET /api/mesas/<id>/
    """
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer
    permission_classes = [IsAuthenticated]


class MesaUpdateView(generics.UpdateAPIView):
    """
    Vista genérica para actualizar una mesa.
    PUT/PATCH /api/mesas/<id>/update/
    """
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer
    permission_classes = [IsAuthenticated]


class MesaDestroyView(generics.DestroyAPIView):
    """
    Vista genérica para eliminar una mesa.
    Solo administradores pueden eliminar.
    DELETE /api/mesas/<id>/delete/
    """
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer
    permission_classes = [IsAuthenticated, IsAdminGroup]

#Vistas Pedido

class PedidoListView(generics.ListAPIView):
    """
    Vista genérica para listar todos los pedidos.
    GET /api/pedidos/
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]


class PedidoCreateView(generics.CreateAPIView):
    """
    Vista genérica para crear un nuevo pedido.
    POST /api/pedidos/create/
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoCreateSerializer
    permission_classes = [IsAuthenticated]


class PedidoRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    Vista genérica para obtener y actualizar un pedido.
    GET/PUT/PATCH /api/pedidos/<id>/
    """
    queryset = Pedido.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PedidoCreateSerializer
        return PedidoSerializer


class PedidoDestroyView(generics.DestroyAPIView):
    """
    Vista genérica para eliminar un pedido.
    Solo administradores pueden eliminar.
    DELETE /api/pedidos/<id>/delete/
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated, IsAdminGroup]


# Viewset Pedido

class PedidoViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para el modelo Pedido.
    Proporciona acciones CRUD con permisos por acción.
    
    - list: GET /api/pedidos-viewset/
    - create: POST /api/pedidos-viewset/
    - retrieve: GET /api/pedidos-viewset/<id>/
    - update: PUT /api/pedidos-viewset/<id>/
    - partial_update: PATCH /api/pedidos-viewset/<id>/
    - destroy: DELETE /api/pedidos-viewset/<id>/
    """
    queryset = Pedido.objects.all()
    permission_classes = [IsAuthenticated, CanDeletePermission]

    def get_serializer_class(self):
        """Retorna el serializador según la acción."""
        if self.action in ['create', 'update', 'partial_update']:
            return PedidoCreateSerializer
        return PedidoSerializer

    def get_permissions(self):
        """
        Personaliza permisos por acción.
        Solo administradores pueden eliminar.
        """
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdminGroup()]
        return [IsAuthenticated(), CanDeletePermission()]


#api view personalizada

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mesa_pedidos_view(request, mesa_id):
    """
    API View personalizada que obtiene todos los pedidos de una mesa específica
    con estadísticas adicionales.
    
    GET /api/mesas/<mesa_id>/pedidos/
 """
    try:
        mesa = Mesa.objects.get(pk=mesa_id)
    except Mesa.DoesNotExist:
        return Response(
            {'error': f'Mesa con id {mesa_id} no encontrada.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Obtener estadísticas de pedidos por estado
    estadisticas_estado = (
        mesa.pedidos
        .values('estado')
        .annotate(cantidad=Count('id'), total=Sum('total'))
        .order_by('estado')
    )

    # Serializar la mesa con sus pedidos
    serializer = MesaPedidosSerializer(mesa)
    
    # Construir respuesta con estadísticas adicionales
    response_data = serializer.data
    response_data['estadisticas_por_estado'] = list(estadisticas_estado)

    return Response(response_data, status=status.HTTP_200_OK)


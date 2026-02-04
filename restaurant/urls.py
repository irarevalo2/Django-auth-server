"""
URLs para la API del restaurante.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    #Vistas genéricas de Mesa
    MesaListView, MesaCreateView, MesaRetrieveView,
    MesaUpdateView, MesaDestroyView,
    #Vistas genéricas de Pedido
    PedidoListView, PedidoCreateView, PedidoRetrieveUpdateView,
    PedidoDestroyView,
    #ViewSet de Pedido
    PedidoViewSet,
    #API View personalizada
    mesa_pedidos_view,
)

router = DefaultRouter()
router.register(r'pedidos-viewset', PedidoViewSet, basename='pedido-viewset')

urlpatterns = [
    path('mesas/', MesaListView.as_view(), name='mesa-list'),
    path('mesas/create/', MesaCreateView.as_view(), name='mesa-create'),
    path('mesas/<int:pk>/', MesaRetrieveView.as_view(), name='mesa-detail'),
    path('mesas/<int:pk>/update/', MesaUpdateView.as_view(), name='mesa-update'),
    path('mesas/<int:pk>/delete/', MesaDestroyView.as_view(), name='mesa-delete'),
    path('mesas/<int:mesa_id>/pedidos/', mesa_pedidos_view, name='mesa-pedidos'),
    path('pedidos/', PedidoListView.as_view(), name='pedido-list'),
    path('pedidos/create/', PedidoCreateView.as_view(), name='pedido-create'),
    path('pedidos/<int:pk>/', PedidoRetrieveUpdateView.as_view(), name='pedido-detail'),
    path('pedidos/<int:pk>/delete/', PedidoDestroyView.as_view(), name='pedido-delete'),
    path('', include(router.urls)),
]


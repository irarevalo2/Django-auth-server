"""
Modelos para la gestión del restaurante.
"""

from django.db import models


class BaseModel(models.Model):
    """
    Modelo base abstracto con campos comunes (DRY).
    Proporciona timestamps de creación y actualización.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        abstract = True


class Mesa(BaseModel):
    """
    Modelo para representar las mesas del restaurante.
    """
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('reservada', 'Reservada'),
    ]

    numero = models.PositiveIntegerField(unique=True, verbose_name='Número de mesa')
    capacidad = models.PositiveIntegerField(verbose_name='Capacidad de comensales')
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='disponible',
        verbose_name='Estado'
    )

    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'
        ordering = ['numero']

    def __str__(self):
        return f'Mesa {self.numero} ({self.get_estado_display()})'


class Pedido(BaseModel):
    """
    Modelo para representar los pedidos del restaurante.
    Cada pedido está asociado a una mesa.
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_preparacion', 'En Preparación'),
        ('servido', 'Servido'),
        ('pagado', 'Pagado'),
    ]

    mesa = models.ForeignKey(
        Mesa,
        on_delete=models.CASCADE,
        related_name='pedidos',
        verbose_name='Mesa'
    )
    descripcion = models.TextField(verbose_name='Descripción del pedido')
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Total'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado'
    )

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']

    def __str__(self):
        return f'Pedido #{self.id} - Mesa {self.mesa.numero} ({self.get_estado_display()})'


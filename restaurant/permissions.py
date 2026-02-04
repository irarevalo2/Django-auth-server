"""
Permisos personalizados para la API del restaurante.
Implementa control de acceso basado en grupos de usuarios.
"""

from rest_framework import permissions


class IsAdminGroup(permissions.BasePermission):
    """
    Permiso que verifica si el usuario pertenece al grupo 'Administradores'.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            request.user.is_superuser or
            request.user.groups.filter(name='Administradores').exists()
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso que permite acceso de solo lectura a todos los usuarios autenticados,
    pero solo los administradores pueden realizar acciones de escritura.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user.is_superuser or
            request.user.groups.filter(name='Administradores').exists()
        )


class CanDeletePermission(permissions.BasePermission):
    """
    Permiso que solo permite eliminar registros a los administradores.
    Los empleados pueden crear, leer y actualizar, pero no eliminar.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method != 'DELETE':
            return True

        return (
            request.user.is_superuser or
            request.user.groups.filter(name='Administradores').exists()
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permiso para vistas de usuario: permite acceso si es el propio usuario o un admin.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        

        if hasattr(obj, 'id') and obj.id == request.user.id:
            return True

        return (
            request.user.is_superuser or
            request.user.groups.filter(name='Administradores').exists()
        )


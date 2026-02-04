"""
Migración de datos para crear los grupos de usuarios iniciales.
Crea los grupos 'Administradores' y 'Empleados' con sus permisos correspondientes.
"""
from django.db import migrations


def create_groups(apps, schema_editor):
    """
    Crea los grupos de usuarios con sus permisos.
    - Administradores: CRUD completo en todos los modelos
    - Empleados: Crear, Leer, Actualizar (sin Eliminar)
    """
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    #Crear grupo Administradores
    admin_group, _ = Group.objects.get_or_create(name='Administradores')
    
    #Crear grupo Empleados
    empleados_group, _ = Group.objects.get_or_create(name='Empleados')

    #Obtener content types para Mesa y Pedido
    try:
        mesa_ct = ContentType.objects.get(app_label='restaurant', model='mesa')
        pedido_ct = ContentType.objects.get(app_label='restaurant', model='pedido')

        # Permisos para Mesa
        mesa_perms = Permission.objects.filter(content_type=mesa_ct)
        # Permisos para Pedido
        pedido_perms = Permission.objects.filter(content_type=pedido_ct)

        # Administradores obtienen todos los permisos
        for perm in mesa_perms:
            admin_group.permissions.add(perm)
        for perm in pedido_perms:
            admin_group.permissions.add(perm)

        # Empleados obtienen permisos de ver, crear y cambiar (no eliminar)
        for perm in mesa_perms:
            if 'delete' not in perm.codename:
                empleados_group.permissions.add(perm)
        for perm in pedido_perms:
            if 'delete' not in perm.codename:
                empleados_group.permissions.add(perm)

    except ContentType.DoesNotExist:
        # Los content types se crearán cuando se apliquen las migraciones
        pass


def remove_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Administradores', 'Empleados']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]


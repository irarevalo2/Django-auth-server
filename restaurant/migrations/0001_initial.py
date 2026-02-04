from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('numero', models.PositiveIntegerField(unique=True, verbose_name='Número de mesa')),
                ('capacidad', models.PositiveIntegerField(verbose_name='Capacidad de comensales')),
                ('estado', models.CharField(choices=[('disponible', 'Disponible'), ('ocupada', 'Ocupada'), ('reservada', 'Reservada')], default='disponible', max_length=20, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Mesa',
                'verbose_name_plural': 'Mesas',
                'ordering': ['numero'],
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('descripcion', models.TextField(verbose_name='Descripción del pedido')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('en_preparacion', 'En Preparación'), ('servido', 'Servido'), ('pagado', 'Pagado')], default='pendiente', max_length=20, verbose_name='Estado')),
                ('mesa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='restaurant.mesa', verbose_name='Mesa')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'ordering': ['-created_at'],
            },
        ),
    ]


# Generated by Django 5.0.4 on 2024-05-03 20:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('listados', '0001_initial'),
        ('publicaciones', '0001_initial'),
        ('sesiones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
                ('ubicacion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ofrecimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('articulo', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField()),
                ('descripcion', models.CharField(max_length=250)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='')),
                ('categoriaId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listados.categoria')),
                ('publicacionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publicaciones.publicacion')),
                ('usuarioId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sesiones.usuario')),
                ('sucursalId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ofrecimientos.sucursal')),
            ],
        ),
    ]

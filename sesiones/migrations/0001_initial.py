# Generated by Django 5.0.4 on 2024-05-03 20:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
                ('apellido', models.TextField()),
                ('contraseña', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Ayudante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_usuario', models.TextField()),
                ('personaId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sesiones.persona')),
            ],
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_usuario', models.TextField()),
                ('personaId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sesiones.persona')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.BigIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('fecha_nac', models.DateField()),
                ('reputacion', models.FloatField()),
                ('cant_valoraciones', models.IntegerField()),
                ('personaId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sesiones.persona')),
            ],
        ),
    ]

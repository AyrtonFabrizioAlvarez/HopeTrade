# Generated by Django 5.0.4 on 2024-05-12 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sesiones', '0003_alter_usuario_dni'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='rol',
            field=models.TextField(default='usuario'),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.0.6 on 2024-05-28 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicaciones', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicacion',
            name='aceptada',
        ),
        migrations.AddField(
            model_name='publicacion',
            name='estado',
            field=models.TextField(default='pendiente'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comentario',
            name='texto',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='imagen',
            field=models.BinaryField(blank=True, editable=True, null=True),
        ),
    ]
# Generated by Django 5.2.3 on 2025-06-26 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0005_equipamento_status_js'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipamento',
            name='destino',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Destino'),
        ),
    ]

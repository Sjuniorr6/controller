# Generated by Django 5.2.3 on 2025-07-03 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_eventotratado_valor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventotratado',
            name='nome_equipamento',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

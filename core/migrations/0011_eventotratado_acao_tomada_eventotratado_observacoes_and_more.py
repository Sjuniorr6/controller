# Generated by Django 5.2.3 on 2025-07-05 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_eventotratado_alerta_disparado'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventotratado',
            name='acao_tomada',
            field=models.CharField(blank=True, choices=[('verificado', 'Verificado'), ('corrigido', 'Corrigido'), ('ignorado', 'Ignorado'), ('escalado', 'Escalado'), ('outro', 'Outro')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='eventotratado',
            name='observacoes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventotratado',
            name='tratado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventotratado',
            name='tratado_por',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

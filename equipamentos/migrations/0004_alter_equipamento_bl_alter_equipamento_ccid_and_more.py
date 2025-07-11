# Generated by Django 5.1.2 on 2025-03-12 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0003_alter_equipamento_bl_alter_equipamento_ccid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipamento',
            name='BL',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='BL'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='CCID',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='CCID'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='cliente',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='container',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Container'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='data_brasil',
            field=models.DateField(blank=True, null=True, verbose_name='Data no Brasil'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='data_chegada_destino',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Chegada no Destino'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='data_desembarque_maritimo',
            field=models.DateField(blank=True, db_column='Data_Desembarque_Maritimo', null=True, verbose_name='Data de Desembarque Marítimo'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='data_do_desembarque',
            field=models.DateField(blank=True, db_column='Data_do_Desembarque', null=True, verbose_name='Data do Desembarque'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='data_embarque_maritimo',
            field=models.CharField(blank=True, db_column='Data_Embarque_Maritimo', max_length=50, null=True, verbose_name='Data de Embarque Marítimo'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='data_entrega',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Entrega'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='data_envio_brasil',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Envio ao Brasil'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='data_insercao',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data de Inserção'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='data_retirada',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Retirada'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='destino',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Destino'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='identificador',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Identificador do Equipamento'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='local_atual',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Local'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='local_entrega',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Local de Entrega'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='modelo',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Modelo'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='observacao',
            field=models.TextField(blank=True, null=True, verbose_name='Observação'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='reposicao',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Reposição'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='requisicao',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Requisição'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='sla_envio_brasil',
            field=models.IntegerField(blank=True, null=True, verbose_name='SLA de Envio ao Brasil'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='sla_insercao',
            field=models.IntegerField(blank=True, null=True, verbose_name='SLA de Inserção'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='sla_maritimo',
            field=models.IntegerField(blank=True, db_column='SLA_Maritimo', null=True, verbose_name='SLA Marítimo'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='sla_operacao',
            field=models.IntegerField(blank=True, null=True, verbose_name='SLA da Operação'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='sla_retirada',
            field=models.IntegerField(blank=True, null=True, verbose_name='SLA de Retirada'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='sla_terrestre',
            field=models.IntegerField(blank=True, db_column='SLA_Terrestre', null=True, verbose_name='SLA Terrestre'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='sla_viagem',
            field=models.IntegerField(blank=True, null=True, verbose_name='SLA de Viagem'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='status_do_container',
            field=models.CharField(blank=True, db_column='Status_do_Container', max_length=100, null=True, verbose_name='Status do Container'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='status_operacao',
            field=models.CharField(choices=[('em_viagem', 'Em Viagem'), ('no_destino', 'No Destino'), ('desacoplado', 'Desacoplado'), ('em_estoque', 'Em Estoque'), ('na_fazenda', 'Na Fazenda')], default='em_viagem', max_length=20, verbose_name='Status da Operação'),
        ),
    ]

# Generated by Django 5.2.3 on 2025-07-02 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodigoEscaneado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=255)),
                ('tipo', models.CharField(blank=True, max_length=50, null=True)),
                ('data', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

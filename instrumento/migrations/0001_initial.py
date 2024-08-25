# Generated by Django 5.1 on 2024-08-25 06:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('veiculo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoInstrumento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('descricao', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instrumento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_serie', models.CharField(max_length=255, unique=True)),
                ('veiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='veiculo.veiculo')),
                ('tipo_instrumento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instrumento.tipoinstrumento')),
            ],
        ),
    ]
# Generated by Django 5.1 on 2024-08-25 06:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('instrumento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_certificado', models.CharField(max_length=255)),
                ('data_validade', models.DateField()),
                ('instrumento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instrumento.instrumento')),
            ],
        ),
    ]

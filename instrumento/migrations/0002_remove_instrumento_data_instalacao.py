# Generated by Django 4.2.15 on 2024-08-13 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instrumento', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instrumento',
            name='data_instalacao',
        ),
    ]
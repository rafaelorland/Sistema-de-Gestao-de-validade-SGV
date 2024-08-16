# Generated by Django 4.2.15 on 2024-08-12 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_alter_cliente_options_alter_telefonecliente_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telefonecliente',
            name='enviar_mensagem',
        ),
        migrations.AddField(
            model_name='cliente',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Email do Cliente'),
        ),
    ]
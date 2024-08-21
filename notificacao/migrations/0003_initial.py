# Generated by Django 4.2.15 on 2024-08-17 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('certificado', '0003_alter_certificado_numero_certificado'),
        ('notificacao', '0002_delete_notificacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataDeEnvioNotificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('data_envio', models.DateField()),
                ('status', models.CharField(default='pendente', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Data de Envio de Notificação',
                'verbose_name_plural': 'Datas de Envio de Notificação',
            },
        ),
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('canal', models.CharField(choices=[('sms', 'SMS'), ('email', 'Email'), ('whatsapp', 'WhatsApp')], max_length=10)),
                ('status', models.CharField(default='pendente', max_length=20)),
                ('mensagem', models.TextField()),
                ('certificado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificado.certificado')),
                ('data_envio_notificacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notificacao.datadeenvionotificacao')),
            ],
            options={
                'verbose_name': 'Notificação',
                'verbose_name_plural': 'Notificações',
            },
        ),
    ]
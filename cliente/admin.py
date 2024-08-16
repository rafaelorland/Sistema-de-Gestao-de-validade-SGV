from django.contrib import admin

from cliente.models import Cliente,TelefoneCliente

# Register your models here.
admin.site.register(Cliente)
admin.site.register(TelefoneCliente)
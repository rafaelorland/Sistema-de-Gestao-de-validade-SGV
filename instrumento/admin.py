from django.contrib import admin

from instrumento.models import Instrumento, TipoInstrumento

# Register your models here.
admin.site.register(Instrumento)
admin.site.register(TipoInstrumento)
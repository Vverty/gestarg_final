from django.contrib import admin
from .models import Gasto, Ingreso, Cliente

admin.site.register(Gasto)
admin.site.register(Ingreso)
admin.site.register(Cliente)


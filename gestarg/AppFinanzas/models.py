from django.db import models
from django.contrib.auth.models import User

class Gasto(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_valor = models.DateTimeField(blank=True, null=True)
    descripcion = models.CharField(max_length=60)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    comentarios = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gastos', null=False, blank=False) # Usuario que cargó el gasto

    def __str__(self):
        return f'Fecha: {self.fecha} | Descripcion: {self.descripcion} | Monto: {self.monto}'
    
class Cliente(models.Model):
    razon_social = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    cuit = models.BigIntegerField(null=True, blank=True)  # No obligatorio
    fecha_onboarding = models.DateField(null=True, blank=True, default=None)  # No obligatorio
    fecha_salida = models.DateField(null=True, blank=True, default=None)  # No obligatorio
    rubro = models.CharField(max_length=100, blank=True)  # No obligatorio
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Usuario que cargó el cliente

    def __str__(self):
        return f'Razon social: {self.razon_social} | Email: {self.email}'
    
class Ingreso(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=60)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=50, blank=True)  # No obligatorio
    fecha_valor = models.DateField(null=True, blank=True)  
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ingresos', null=False, blank=False)  # Usuario que cargó el ingreso

    def __str__(self):
        return f'Fecha: {self.fecha} | Descripción: {self.descripcion} | Monto: {self.monto}'

    

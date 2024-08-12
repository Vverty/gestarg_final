from django.db import models

class Gasto(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=60)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'Fecha: {self.fecha} | Descripcion: {self.descripcion} | Monto: {self.monto}'
    
class Cliente(models.Model):
    razon_social = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f'Razon social: {self.razon_social} | Email: {self.email}'
    
class Ingreso(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=60)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.descripcion} - {self.monto} - {self.fecha} - {self.cliente.razon_social}'

    

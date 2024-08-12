from django import forms
from .models import Gasto, Ingreso, Cliente

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['descripcion', 'monto']
        
class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['descripcion', 'monto', 'cliente']
        
class BuscarClienteForm(forms.Form):
    razon_social = forms.CharField(required=False, label='Razón Social')
    email = forms.EmailField(required=False, label='Email')
    
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['razon_social', 'email', 'telefono']
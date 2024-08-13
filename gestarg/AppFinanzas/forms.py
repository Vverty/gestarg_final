from django import forms
from .models import Gasto, Ingreso, Cliente

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['fecha_valor', 'descripcion', 'monto', 'comentarios', 'usuario']
        widgets = {
            'fecha_valor': forms.DateInput(attrs={'type': 'date'}),
            'comentarios': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Si el usuario está presente, se establece como valor predeterminado
        if user:
            self.fields['usuario'].initial = user
            self.fields['usuario'].widget = forms.HiddenInput()  # Ocultar el campo en la interfaz
        
        self.fields['usuario'].required = False

    def clean_fecha_valor(self):
        fecha_valor = self.cleaned_data.get('fecha_valor')
        if not fecha_valor:
            # Mensaje de error si 'fecha_valor' no está completado
            raise forms.ValidationError("Por favor, complete la fecha valor.")
        return fecha_valor


class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['fecha_valor', 'descripcion', 'monto', 'cliente', 'metodo_pago', 'usuario']
        widgets = {
            'fecha_valor': forms.DateInput(attrs={'type': 'date'}),
            'usuario': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['usuario'].initial = user
            self.fields['usuario'].widget = forms.HiddenInput()
            self.fields['usuario'].required = False

    def clean_fecha_valor(self):
        fecha_valor = self.cleaned_data.get('fecha_valor')
        if not fecha_valor:
            self.add_error('fecha_valor', 'Por favor, complete la fecha valor.')
        return fecha_valor

class BuscarClienteForm(forms.Form):
    razon_social = forms.CharField(required=False, label='Razón Social')
    email = forms.EmailField(required=False, label='Email')
    
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['razon_social', 'email', 'telefono', 'cuit', 'fecha_onboarding', 'fecha_salida', 'rubro']
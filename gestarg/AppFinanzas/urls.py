from django.contrib import admin
from django.urls import path
from AppFinanzas import views
from .views import *

#GASTOS
urlpatterns = [
    path('', InicioView.as_view(), name='Inicio'),
    path('403/', TemplateView.as_view(template_name="AppFinanzas/403.html"), name='403'),
    path('gastos/', MostrarGastosView.as_view(), name='MostrarGastos'),
    path('gastos/agregar/', AgregarGastoView.as_view(), name='AgregarGasto'),
    path('gastos/detalle/<int:pk>/', VerGastoView.as_view(), name='VerGasto'),
    path('gastos/editar/<int:pk>/', EditarGastoView.as_view(), name='EditarGasto'),
    path('gastos/eliminar/<int:pk>/', EliminarGastoView.as_view(), name='EliminarGasto')
]

#INGRESOS
urlpatterns += [
    path('ingresos/', MostrarIngresosView.as_view(), name='MostrarIngresos'),
    path('ingresos/agregar/', AgregarIngresoView.as_view(), name='AgregarIngreso'),
    path('ingresos/detalle/<int:pk>/', VerIngresoView.as_view(), name='VerIngreso'),
    path('ingresos/editar/<int:pk>/', EditarIngresoView.as_view(), name='EditarIngreso'),
    path('ingresos/eliminar/<int:pk>/', EliminarIngresoView.as_view(), name='EliminarIngreso')
]

#CLIENTES
urlpatterns += [
    path('clientes/', MostrarClientesView.as_view(), name='MostrarClientes'),
    path('clientes/agregar/', AgregarClienteView.as_view(), name='AgregarCliente'),
    path('clientes/detalle/<int:pk>/', VerClienteView.as_view(), name='VerCliente'),
    path('clientes/editar/<int:pk>/', EditarClienteView.as_view(), name='EditarCliente'),
    path('clientes/eliminar/<int:pk>/', EliminarClienteView.as_view(), name='EliminarCliente')
]

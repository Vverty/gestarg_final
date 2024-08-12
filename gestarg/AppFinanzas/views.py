import json
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.db.models.functions import TruncDay
from django.views.generic.edit import CreateView, UpdateView, DeleteView     
from django.urls import reverse_lazy

from .models import Gasto, Ingreso, Cliente
from .forms import GastoForm, IngresoForm, BuscarClienteForm, ClienteForm




class InicioView(LoginRequiredMixin, TemplateView):
    template_name = 'AppFinanzas/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Cálculos de ingresos, gastos y clientes
        context['total_ingresos'] = Ingreso.objects.aggregate(Sum('monto'))['monto__sum'] or 0
        context['total_gastos'] = Gasto.objects.aggregate(Sum('monto'))['monto__sum'] or 0
        context['cantidad_clientes'] = Cliente.objects.count()

        # Ingresos y gastos diarios
        ingresos_diarios = list(Ingreso.objects.values('fecha').annotate(total=Sum('monto')).order_by('fecha'))
        gastos_diarios = list(Gasto.objects.values('fecha').annotate(total=Sum('monto')).order_by('fecha'))

        # Formatear las fechas y convertir a JSON
        for ingreso in ingresos_diarios:
            ingreso['fecha'] = ingreso['fecha'].strftime('%Y-%m-%d')
            ingreso['total'] = float(ingreso['total'])

        for gasto in gastos_diarios:
            gasto['fecha'] = gasto['fecha'].strftime('%Y-%m-%d')
            gasto['total'] = float(gasto['total'])

        # Añadir los datos al contexto
        context['ingresos_diarios'] = json.dumps(ingresos_diarios)
        context['gastos_diarios'] = json.dumps(gastos_diarios)

        return context

#GASTOS
class AgregarGastoView(LoginRequiredMixin, CreateView):
    model = Gasto
    form_class = GastoForm
    template_name = 'AppFinanzas/agregar_gasto.html'
    success_url = reverse_lazy('MostrarGastos')

class MostrarGastosView(LoginRequiredMixin, ListView):
    model = Gasto
    template_name = 'AppFinanzas/mostrar_gastos.html'
    context_object_name = 'gastos'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Gasto.objects.filter(descripcion__icontains=query)
        else:
            return Gasto.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class EditarGastoView(LoginRequiredMixin, UpdateView):
    model = Gasto
    form_class = GastoForm
    template_name = 'AppFinanzas/editar_gasto.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse_lazy('MostrarGastos')
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Gasto, pk=pk)


class EliminarGastoView(LoginRequiredMixin, DeleteView):
    model = Gasto
    template_name = 'AppFinanzas/eliminar_gasto.html'
    context_object_name = 'gasto'
    success_url = reverse_lazy('MostrarGastos')
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Gasto, pk=pk)

#INGRESOS
class AgregarIngresoView(LoginRequiredMixin, CreateView):
    model = Ingreso
    form_class = IngresoForm
    template_name = 'AppFinanzas/agregar_ingreso.html'
    success_url = reverse_lazy('MostrarIngresos')

class MostrarIngresosView(LoginRequiredMixin, ListView):
    model = Ingreso
    template_name = 'AppFinanzas/mostrar_ingresos.html'
    context_object_name = 'ingresos'
    paginate_by = 10  # Opcional: Puedes agregar paginación si es necesario

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Ingreso.objects.filter(descripcion__icontains=query)
        return Ingreso.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class EditarIngresoView(LoginRequiredMixin, UpdateView):
    model = Ingreso
    form_class = IngresoForm
    template_name = 'AppFinanzas/editar_ingreso.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse_lazy('MostrarIngresos')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Ingreso, pk=pk)

class EliminarIngresoView(LoginRequiredMixin, DeleteView):
    model = Ingreso
    template_name = 'AppFinanzas/eliminar_ingreso.html'
    context_object_name = 'ingreso'
    success_url = reverse_lazy('MostrarIngresos')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Ingreso, pk=pk)

#CLIENTES

class MostrarClientesView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'AppFinanzas/mostrar_clientes.html'
    context_object_name = 'clientes'
    form_class = BuscarClienteForm

    def get_queryset(self):
        queryset = super().get_queryset()
        razon_social = self.request.GET.get('razon_social')
        email = self.request.GET.get('email')

        if razon_social:
            queryset = queryset.filter(razon_social__icontains=razon_social)
        if email:
            queryset = queryset.filter(email__icontains=email)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET or None)
        return context

class AgregarClienteView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'AppFinanzas/agregar_cliente.html'
    success_url = reverse_lazy('MostrarClientes')

class EditarClienteView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'AppFinanzas/editar_cliente.html'
    success_url = reverse_lazy('MostrarClientes')
    pk_url_kwarg = 'pk'

class EliminarClienteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'AppFinanzas/eliminar_cliente.html'
    context_object_name = 'cliente'
    success_url = reverse_lazy('MostrarClientes')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Cliente, pk=pk)


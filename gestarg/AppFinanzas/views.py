import json
from decimal import Decimal
import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
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
class AgregarGastoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Gasto
    form_class = GastoForm
    template_name = 'AppFinanzas/agregar_gasto.html'
    success_url = reverse_lazy('MostrarGastos')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Añadir el usuario actual al kwargs para el formulario
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Asegurarse de que el campo usuario se establezca correctamente
        if form.instance.fecha_valor is None:
            form.instance.fecha_valor = self.request.POST.get('fecha_valor')  # Usa el valor del formulario o establece uno predeterminado
        # Establecer el usuario directamente en el formulario antes de guardarlo
        form.instance.usuario = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        # Verificar si el usuario es miembro del staff
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        # Redirigir a la página de error 403 personalizada
        return redirect('403') 
    
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

class EditarGastoView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Gasto
    form_class = GastoForm
    template_name = 'AppFinanzas/editar_gasto.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse_lazy('MostrarGastos')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Añadir el usuario actual al kwargs para el formulario
        kwargs['user'] = self.request.user
        return kwargs
    
    def test_func(self):
        # Verificar si el usuario es miembro del staff
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        # Redirigir a la página de error 403 personalizada
        return redirect('403') 

    def form_valid(self, form):
        # Asegurarse de que el campo usuario se establezca correctamente
        if form.instance.fecha_valor is None:
            form.instance.fecha_valor = self.request.POST.get('fecha_valor')  # Usa el valor del formulario o establece uno predeterminado
        # Establecer el usuario directamente en el formulario antes de guardarlo
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class VerGastoView(LoginRequiredMixin, DetailView):
    model = Gasto
    template_name = 'AppFinanzas/ver_gasto.html'
    context_object_name = 'gasto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EliminarGastoView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Gasto
    template_name = 'AppFinanzas/eliminar_gasto.html'
    context_object_name = 'gasto'
    success_url = reverse_lazy('MostrarGastos')
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Gasto, pk=pk)

    def test_func(self):
        # Verificar si el usuario es miembro del staff
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        # Redirigir a la página de error 403 personalizada
        return redirect('403') 

#INGRESOS
class AgregarIngresoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Ingreso
    form_class = IngresoForm
    template_name = 'AppFinanzas/agregar_ingreso.html'
    success_url = reverse_lazy('MostrarIngresos')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pasar el usuario actual al formulario
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Si fecha_valor no se ha proporcionado, establecerla en la fecha actual
        if not form.cleaned_data.get('fecha_valor'):
            form.instance.fecha_valor = datetime.date.today()  # O la fecha que prefieras

        # Establecer el usuario directamente en el formulario antes de guardarlo
        form.instance.usuario = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        # Verificar si el usuario es miembro del staff
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        # Redirigir a la página de error 403 personalizada
        return redirect('403') 

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

class VerIngresoView(LoginRequiredMixin, DetailView):
    model = Ingreso
    template_name = 'AppFinanzas/ver_ingreso.html'
    context_object_name = 'ingreso'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Ingreso, pk=pk)

class EditarIngresoView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ingreso
    form_class = IngresoForm
    template_name = 'AppFinanzas/editar_ingreso.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse_lazy('MostrarIngresos')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pasar el usuario actual al formulario
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Establecer el usuario directamente en el formulario antes de guardarlo
        form.instance.usuario = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        # Verificar si el usuario es miembro del staff
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        # Redirigir a la página de error 403 personalizada
        return redirect('403') 

class EliminarIngresoView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ingreso
    template_name = 'AppFinanzas/eliminar_ingreso.html'
    context_object_name = 'ingreso'
    success_url = reverse_lazy('MostrarIngresos')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Ingreso, pk=pk)
    
    def test_func(self):
        # Verificar si el usuario es miembro del staff
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        # Redirigir a la página de error 403 personalizada
        return redirect('403') 

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

class VerClienteView(DetailView):
    model = Cliente
    template_name = 'AppFinanzas/ver_cliente.html'
    context_object_name = 'cliente'
    
class AgregarClienteView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'AppFinanzas/agregar_cliente.html'
    success_url = reverse_lazy('MostrarClientes')
    
    def test_func(self):
        # Verificar si el usuario es miembro del staff
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        # Redirigir a la página de error 403 personalizada
        return redirect('403') 

class EditarClienteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'AppFinanzas/editar_cliente.html'
    success_url = reverse_lazy('MostrarClientes')
    pk_url_kwarg = 'pk'

    def test_func(self):
        # Verificar si el usuario es miembro del staff
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        # Redirigir a la página de error 403 personalizada
        return redirect('403') 

class EliminarClienteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cliente
    template_name = 'AppFinanzas/eliminar_cliente.html'
    context_object_name = 'cliente'
    success_url = reverse_lazy('MostrarClientes')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Cliente, pk=pk)
    
    def test_func(self):
        # Verificar si el usuario es miembro del staff
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        # Redirigir a la página de error 403 personalizada
        return redirect('403') 


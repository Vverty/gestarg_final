import json
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDay

from .models import Gasto, Ingreso, Cliente
from .forms import GastoForm, IngresoForm, BuscarClienteForm, ClienteForm




@login_required
def inicio(request):
    total_ingresos = Ingreso.objects.aggregate(Sum('monto'))['monto__sum'] or 0
    total_gastos = Gasto.objects.aggregate(Sum('monto'))['monto__sum'] or 0
    cantidad_clientes = Cliente.objects.count()

    ingresos_diarios = list(Ingreso.objects.values('fecha').annotate(total=Sum('monto')).order_by('fecha'))
    gastos_diarios = list(Gasto.objects.values('fecha').annotate(total=Sum('monto')).order_by('fecha'))

    for ingreso in ingresos_diarios:
        ingreso['fecha'] = ingreso['fecha'].strftime('%Y-%m-%d')
        ingreso['total'] = float(ingreso['total'])

    for gasto in gastos_diarios:
        gasto['fecha'] = gasto['fecha'].strftime('%Y-%m-%d')
        gasto['total'] = float(gasto['total'])

    # Imprime los datos en la consola del servidor
    print(json.dumps(ingresos_diarios, indent=2))
    print(json.dumps(gastos_diarios, indent=2))

    context = {
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'cantidad_clientes': cantidad_clientes,
        'ingresos_diarios': json.dumps(ingresos_diarios),  # Convertir a JSON
        'gastos_diarios': json.dumps(gastos_diarios),    # Convertir a JSON
    }
    return render(request, 'AppFinanzas/index.html', context)

#GASTOS
@login_required
def agregar_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MostrarGastos')
    else:
        form = GastoForm()
    return render(request, 'AppFinanzas/agregar_gasto.html', {'form': form})

@login_required
def mostrar_gastos(request):
    query = request.GET.get('q')
    if query:
        gastos = Gasto.objects.filter(descripcion__icontains=query)
    else:
        gastos = Gasto.objects.all()
    return render(request, 'AppFinanzas/mostrar_gastos.html', {'gastos': gastos, 'query': query})

@login_required
def editar_gasto(request, id):
    gasto = get_object_or_404(Gasto, id=id)
    if request.method == 'POST':
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            return redirect('MostrarGastos')
    else:
        form = GastoForm(instance=gasto)
    return render(request, 'AppFinanzas/editar_gasto.html', {'form': form})

@login_required
def eliminar_gasto(request, id):
    gasto = get_object_or_404(Gasto, id=id)
    if request.method == 'POST':
        gasto.delete()
        return redirect('MostrarGastos')
    return render(request, 'AppFinanzas/eliminar_gasto.html', {'gasto': gasto})

#INGRESOS
@login_required
def agregar_ingreso(request):
    if request.method == 'POST':
        form = IngresoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MostrarIngresos')
    else:
        form = IngresoForm()
    return render(request, 'AppFinanzas/agregar_ingreso.html', {'form': form})

@login_required
def mostrar_ingresos(request):
    query = request.GET.get('q')
    if query:
        ingresos = Ingreso.objects.filter(descripcion__icontains=query)
    else:
        ingresos = Ingreso.objects.all()
    return render(request, 'AppFinanzas/mostrar_ingresos.html', {'ingresos': ingresos, 'query': query})

@login_required
def editar_ingreso(request, pk):
    ingreso = get_object_or_404(Ingreso, pk=pk)
    if request.method == 'POST':
        form = IngresoForm(request.POST, instance=ingreso)
        if form.is_valid():
            form.save()
            return redirect('MostrarIngresos')
    else:
        form = IngresoForm(instance=ingreso)
    return render(request, 'AppFinanzas/editar_ingreso.html', {'form': form})

@login_required
def eliminar_ingreso(request, pk):
    ingreso = get_object_or_404(Ingreso, pk=pk)
    if request.method == 'POST':
        ingreso.delete()
        return redirect('MostrarIngresos')
    return render(request, 'AppFinanzas/eliminar_ingreso.html', {'ingreso': ingreso})

#CLIENTES

@login_required
def mostrar_clientes(request):
    form = BuscarClienteForm(request.GET or None)
    clientes = Cliente.objects.all()

    razon_social = request.GET.get('razon_social')
    email = request.GET.get('email')

    if razon_social:
        clientes = clientes.filter(razon_social__icontains=razon_social)
    if email:
        clientes = clientes.filter(email__icontains=email)

    context = {
        'clientes': clientes,
        'form': form,
    }

    return render(request, 'AppFinanzas/mostrar_clientes.html', context)

@login_required
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MostrarClientes')
    else:
        form = ClienteForm()
    return render(request, 'AppFinanzas/agregar_cliente.html', {'form': form})

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('MostrarClientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'AppFinanzas/editar_cliente.html', {'form': form})

@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('MostrarClientes')
    return render(request, 'AppFinanzas/eliminar_cliente.html', {'cliente': cliente})


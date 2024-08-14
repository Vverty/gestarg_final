from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from .forms import UserRegisterForm, UserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Profile
from django.views.generic import ListView, View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse

def login_request(request):

    msg_login = ""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')

            user = authenticate(username=usuario, password=contrasenia)

            if user is not None:
                login(request, user)
                return render(request, 'AppFinanzas/index.html')

        msg_login = "Usuario o contraseña incorrectos"

    form = AuthenticationForm()
    return render(request, "Users/login.html", {"form": form, "msg_login": msg_login})

def register(request):
    msg_register = ""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)  # Añadido request.FILES para manejar archivos
        if form.is_valid():
            form.save()
            return redirect('Login')  # Redirige a la página de inicio o a donde necesites
        else:
            msg_register = "Error en los datos ingresados"
    else:
        form = UserRegisterForm()

    return render(request, "Users/register.html", {"form": form, "msg_register": msg_register})

# Vista de editar el perfil
# Obligamos a loguearse para editar los datos del usuario activo
@login_required
def editar_perfil(request):
    usuario = request.user

    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST, request.FILES, instance=usuario)
        if miFormulario.is_valid():
            # Guardar el formulario, incluyendo la lógica para eliminar la imagen si es necesario
            miFormulario.save()
            return redirect('EditarPerfil')  # Redirige a la vista de perfil editado

    else:
        miFormulario = UserEditForm(instance=usuario)

    return render(request, "Users/edit_user.html", {"mi_form": miFormulario, "usuario": usuario})



@login_required
def cambiar_contrasenia(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantener la sesión iniciada después del cambio de contraseña
            messages.success(request, 'Tu contraseña ha sido actualizada con éxito.')
            return redirect('EditarPerfil')  # Redirige al perfil o a la página deseada
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'Users/password_change.html', {'form': form})

class ManageStaffView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'Users/manage_staff.html'
    context_object_name = 'usuarios'

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        # Excluye a los superusuarios de la lista
        return User.objects.filter(is_superuser=False)

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = User.objects.get(id=user_id)

        if action == 'add_staff':
            user.is_staff = True
            user.save()
        elif action == 'remove_staff':
            user.is_staff = False
            user.save()
        elif action == 'delete_user':
            user.delete()

        return redirect('ManageStaff')
    
@login_required
def eliminar_imagen(request):
    usuario = request.user
    profile, created = Profile.objects.get_or_create(user=usuario)
    profile.profile_image = None
    profile.save()
    return redirect('EditarPerfil')


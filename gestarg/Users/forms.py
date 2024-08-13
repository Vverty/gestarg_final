from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User  # Asegúrate de importar el modelo User
from django.core.exceptions import ValidationError
from .models import Profile, User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo Electrónico')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir Contraseña', widget=forms.PasswordInput)
    profile_image = forms.ImageField(label='Imagen de Perfil', required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "profile_image"]
        help_texts = {k: "" for k in fields}  # Limpia los mensajes de ayuda predeterminados

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Crear un perfil con la imagen de perfil
            profile_image = self.cleaned_data.get('profile_image')
            Profile.objects.create(user=user, profile_image=profile_image)
        return user
class UserEditForm(forms.ModelForm):
    email = forms.EmailField(label="Ingrese su email:")
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    profile_image = forms.ImageField(label='Imagen de Perfil', required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_image']
        help_texts = {k: "" for k in fields}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            profile, created = Profile.objects.get_or_create(user=user)
            self.fields['profile_image'].initial = profile.profile_image

    def save(self, commit=True):
        user = super().save(commit=False)
        profile_image = self.cleaned_data.get('profile_image')
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            if profile_image:
                profile.profile_image = profile_image
            profile.save()
        return user

from django.urls import path
from Users import views
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('login/', views.login_request, name='Login'),
    path('register/', views.register, name='Register'),
    path('logout/', LogoutView.as_view(template_name='Landing/index.html'), name="Logout"),
    path('profile/', views.editar_perfil, name='EditarPerfil'),
    path('password-change/', views.cambiar_contrasenia, name='PasswordChange'),
    path('manage-staff/', ManageStaffView.as_view(), name='ManageStaff'),
    path('eliminar-imagen/', views.eliminar_imagen, name='EliminarImagen'),
] 
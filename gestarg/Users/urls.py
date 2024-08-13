from django.urls import path
from Users import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.login_request, name='Login'),
    path('register/', views.register, name='Register'),
    path('logout/', LogoutView.as_view(template_name='Landing/index.html'), name="Logout"),
    path('profile/', views.editar_perfil, name='EditarPerfil'),
    path('password-change/', views.cambiar_contrasenia, name='PasswordChange'),
] 
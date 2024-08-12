from django.urls import path
from Landing import views

urlpatterns = [
    path('nosotros/', views.nosotros, name='Nosotros'),
    path('', views.inicio_landing, name='InicioLanding'),
    path('acerca-de-mi/', views.acerca_de_mi, name='AboutMe')
]

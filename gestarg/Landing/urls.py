from django.urls import path
from .views import *

urlpatterns = [
    path('', InicioLandingView.as_view(), name='InicioLanding'),
    path('nosotros/', NosotrosView.as_view(), name='Nosotros'),
    path('about/', AboutView.as_view(), name='AboutMe')
]

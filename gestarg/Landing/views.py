from django.shortcuts import render
from datetime import datetime

def nosotros(request):
    return render(request, 'Landing/nosotros.html')

def inicio_landing(request):
    current_year = datetime.now().year
    return render(request, 'Landing/index.html', {'current_year': current_year})

def acerca_de_mi(request):
    return render(request, 'Landing/about_me.html')

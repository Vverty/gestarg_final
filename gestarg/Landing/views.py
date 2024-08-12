from django.shortcuts import render
from datetime import datetime
from django.views.generic import TemplateView

class NosotrosView(TemplateView):
    template_name = 'Landing/nosotros.html'

class InicioLandingView(TemplateView):
    template_name = 'Landing/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = datetime.now().year
        return context

class AboutView(TemplateView):
    template_name = 'Landing/about_me.html'

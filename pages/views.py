from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import SearchBarForm

class HomePageView(TemplateView):
    template_name = 'home.html'

def search_bar(request):
    form = SearchBarForm()
    return render(request, 'base.html',)

# Create your views here.

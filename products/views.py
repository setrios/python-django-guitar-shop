from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Guitar

# Create your views here.

class GuitarList(ListView):
    model = Guitar
    template_name = 'guitar_list.html'

class GuitarDetail(DetailView):
    model = Guitar
    template_name = 'guitar_detail.html'

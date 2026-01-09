from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from django_filters.views import FilterView

from .models import Guitar, Accessory

# Create your views here.

class GuitarList(FilterView):
    model = Guitar
    filterset_fields = ['guitar_type', 'brand', 'string_num', 'handedness']
    template_name = 'guitar_list.html'


class GuitarDetail(DetailView):
    model = Guitar
    template_name = 'guitar_detail.html'


class AccesoriesList(FilterView):
    model = Accessory
    filterset_fields = ['brand',]
    template_name = 'accessory_list.html'


class AccessoryDetail(DetailView):
    model = Accessory
    template_name = 'accessory_detail.html'

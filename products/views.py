from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from django_filters.views import FilterView
from django.db.models import Q

from .models import Guitar, Accessory
from .filters import ProductFilter, AccessoryFilter

# Create your views here.

class GuitarList(FilterView):
    model = Guitar
    filterset_class = ProductFilter
    template_name = 'guitar_list.html'
    
    def get_queryset(self):
        queryset = Guitar.objects.all()
        query = self.request.GET.get('q')
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        
        return queryset



class GuitarDetail(DetailView):
    model = Guitar
    template_name = 'guitar_detail.html'


class AccesoriesList(FilterView):
    model = Accessory
    filterset_class = AccessoryFilter
    template_name = 'accessory_list.html'
    
    def get_queryset(self):
        queryset = Accessory.objects.all()
        query = self.request.GET.get('q')
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        
        return queryset



class AccessoryDetail(DetailView):
    model = Accessory
    template_name = 'accessory_detail.html'

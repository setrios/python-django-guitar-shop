import django_filters
from django import forms
from .models import Guitar, Brand, GuitarType

class ProductFilter(django_filters.FilterSet):
    guitar_type = django_filters.ModelMultipleChoiceFilter(
        queryset=GuitarType.objects.all(),
        widget=forms.CheckboxSelectMultiple  # here choosing any widget we want
    )
    
    brand = django_filters.ModelMultipleChoiceFilter(
        queryset=Brand.objects.filter(guitar__is_avaliable=True).distinct(),
        widget=forms.CheckboxSelectMultiple
    )
    
    string_num = django_filters.MultipleChoiceFilter(
        choices=lambda: [(num, num) for num in Guitar.objects.values_list('string_num', flat=True).distinct().order_by('string_num')],
        widget=forms.CheckboxSelectMultiple,
        label='String Number'
    )
    
    handedness = django_filters.MultipleChoiceFilter(
        choices=Guitar.HANDEDNESS_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    
    class Meta:
        model = Guitar
        fields = [
            'guitar_type', 
            'brand', 
            'string_num', 
            'handedness'
        ]


class AccessoryFilter(django_filters.FilterSet):
    brand = django_filters.ModelMultipleChoiceFilter(
        queryset=Brand.objects.filter(accessory__is_avaliable=True).distinct(),
        widget=forms.CheckboxSelectMultiple
    )
    
    class Meta:
        model = Guitar
        fields = [
            'brand', 
        ]
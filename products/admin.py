from django.contrib import admin
from .models import Guitar, GuitarType, Brand, Accessory, AccessoryType

# Register your models here.

admin.site.register(Guitar)
admin.site.register(GuitarType)
admin.site.register(Brand)
admin.site.register(Accessory)
admin.site.register(AccessoryType)

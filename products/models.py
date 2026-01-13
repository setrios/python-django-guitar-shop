from django.db import models
from django.urls import reverse

# Create your models here.

class Guitar(models.Model):
    HANDEDNESS_CHOICES = [
      # ('name_in_db', 'readable_name')
        ('right', 'Right-handed'),
        ('left', 'Left-handed'),
    ]

    image = models.ImageField(upload_to='guitars/')
    name = models.CharField(max_length=255)
    guitar_type = models.ForeignKey('GuitarType', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='guitar')
    model = models.CharField(max_length=255)
    string_num = models.PositiveIntegerField()
    handedness = models.CharField(max_length=10, choices=HANDEDNESS_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_avaliable = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:guitar_detail', kwargs={'pk': self.pk})
    

class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class GuitarType(models.Model):
    guitar_type_name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.guitar_type_name
    

class Accessory(models.Model):
    image = models.ImageField(upload_to='accessories/')
    name = models.CharField(max_length=255)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='accessory')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_avaliable = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:accessory_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Accessories'


class AccessoryType(models.Model):
    accessory_type_name = models.CharField(max_length=255, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.accessory_type_name
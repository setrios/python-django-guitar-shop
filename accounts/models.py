from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    

class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')

    address1 = models.CharField(max_length=255)  # steet / house number
    address2 = models.CharField(max_length=255, blank=True)  # Apartment / Unit / Suite Number
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.PositiveIntegerField()
    country = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    
    # Optional: make one address the default
    is_default = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Shipping Addresses"
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.address1}, {self.city}, {self.country}"
    
    def save(self, *args, **kwargs):
        # If this is set as default, unset other defaults for this user
        if self.is_default:
            ShippingAddress.objects.filter(
                user=self.user, 
                is_default=True
            ).update(is_default=False)
        super().save(*args, **kwargs)
    
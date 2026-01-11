from django import forms
from .models import Order
from accounts.models import ShippingAddress


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('address', 'comment', 'payment_provider')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Filter addresses to only show user's addresses
            self.fields['address'].queryset = ShippingAddress.objects.filter(user=user)
            self.fields['address'].empty_label = 'Select an address'


class CheckoutWithNewAddressForm(forms.ModelForm):
    address1 = forms.CharField(max_length=255, label='Address Line 1')
    address2 = forms.CharField(max_length=255, required=False, label='Address Line 2')
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100, required=False)
    postal_code = forms.CharField(max_length=20, label='Postal Code')
    country = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20, required=False, label='Phone Number')
    
    class Meta:
        model = Order
        fields = ('comment', 'payment_provider')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
    
    def save_address(self, user):
        address = ShippingAddress.objects.create(
            user=user,
            address1=self.cleaned_data['address1'],
            address2=self.cleaned_data.get('address2', ''),
            city=self.cleaned_data['city'],
            state=self.cleaned_data.get('state', ''),
            postal_code=self.cleaned_data['postal_code'],
            country=self.cleaned_data['country'],
            phone=self.cleaned_data.get('phone', ''),
        )
        return address
from django.db import models
from django import forms
from django.contrib.auth.models import User

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)  # New field to indicate if it's a default address
    
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}"

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state']
        widgets = {
            'street': forms.TextInput(attrs={'class': 'contact__form--input', 'placeholder': 'Street'}),
            'city': forms.TextInput(attrs={'class': 'contact__form--input', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'contact__form--input', 'placeholder': 'State'}),
        }
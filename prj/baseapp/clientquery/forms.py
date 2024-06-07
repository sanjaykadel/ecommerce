from django import forms
from .clientModel import ClientQuery

class ClientQueryForm(forms.ModelForm):
    subject = forms.CharField(max_length=100,required=False)
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ClientQuery
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'message']  # Remove 'company_name' from the fields list
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'contact__form--input', 'id': 'first_name', 'placeholder': 'Your First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'contact__form--input', 'id': 'last_name', 'placeholder': 'Your Last Name'}),
            'email': forms.TextInput(attrs={'class': 'contact__form--input', 'id': 'email', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'contact__form--input', 'id': 'phone_number', 'placeholder': 'Phone Number'}),
            'message': forms.TextInput(attrs={'class': 'contact__form--input', 'id': 'message', 'placeholder': 'Message'}),
        }

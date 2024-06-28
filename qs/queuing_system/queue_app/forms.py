from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TableNumberForm(forms.Form):
    table_number = forms.IntegerField(min_value=1, max_value=10, label='Table Number')

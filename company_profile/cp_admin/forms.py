from django import forms
from django.contrib.auth.models import User
from membership.models import Member

class CmsLoginForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=150)
    attrs = {
        "type": "password"
    }
    password = forms.CharField(label='Password :', widget=forms.PasswordInput(attrs=attrs))


class CmsActivationForm(forms.Form):
    user_id = forms.CharField(label='User ID:', max_length=150)
    access_key = forms.CharField(label='Access Key :')

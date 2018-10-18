from django import forms
from store.st_database_wilayah.models import Provinsi

class CustomerAddForm(forms.Form):
    USERNAME_MAX = 20
    USERNAME_MIN = 6
    username = forms.CharField(label='Username/ Phone/ Email :', max_length=150)
    attrs = {
        "type": "password"
    }
    password = forms.CharField(label='Password :', widget=forms.PasswordInput(attrs=attrs))
    provinsi_home = forms.ModelChoiceField(Provinsi.objects.all(), initial='')
    home_address = forms.CharField(max_length=250, required=True)
    
    def __init__(self, *args, **kwargs):
        super(CustomerAddForm, self).__init__(*args, **kwargs)
       
        self.fields['provinsi_home'].widget.attrs['onClick'] = 'getKota(this.id)'
        self.fields['provinsi_home'].widget.attrs['style'] = 'width:100%'

        self.fields['home_address'].widget = forms.Textarea()
        self.fields['home_address'].widget.attrs['rows'] = '3'
        self.fields['home_address'].widget.attrs['placeholder'] = 'Contoh: Jl. Angkasa 1 Blok AF6 NO 18'
        self.fields['home_address'].widget.attrs['style'] = 'width:100%'

        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs['placeholder'] = '*********'
        self.fields['password'].widget.attrs['class'] = 'input-text'
        self.fields['password'].widget.attrs['style'] = 'width:100%'

        self.fields['username'].widget.attrs['placeholder'] = 'Masukan Username'
        self.fields['username'].widget.attrs['class'] = 'input-text'
        self.fields['username'].widget.attrs['style'] = 'width:100%'
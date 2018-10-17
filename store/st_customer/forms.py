from django import forms
from store.st_database_wilayah.models import Provinsi

class CustomerAddForm(forms.Form):
    USERNAME_MAX = 20
    USERNAME_MIN = 6
    provinsi_home = forms.ModelChoiceField(Provinsi.objects.all(), initial='')
    home_address = forms.CharField(max_length=250, required=True)
    name = forms.CharField(required=True, min_length=USERNAME_MIN, max_length=USERNAME_MAX)

    def __init__(self, *args, **kwargs):
        super(CustomerAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Nama Penerima'
        self.fields['name'].widget.attrs['class'] = 'input-text'
        self.fields['name'].widget.attrs['style'] = 'width:100%'
        self.fields['provinsi_home'].widget.attrs['onchange'] = 'getKota(this.id)'
        self.fields['provinsi_home'].widget.attrs['style'] = 'width:100%'

        self.fields['home_address'].widget = forms.Textarea()
        self.fields['home_address'].widget.attrs['rows'] = '3'
        self.fields['home_address'].widget.attrs['placeholder'] = 'Contoh: Jl. Angkasa 1 Blok AF6 NO 18'
        self.fields['home_address'].widget.attrs['style'] = 'width:100%'
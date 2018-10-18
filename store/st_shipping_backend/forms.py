from django import forms
from store.st_database_wilayah.models import Provinsi

class ShippingAddForm(forms.Form):
    name = forms.CharField(label='Username/ Phone/ Email :', max_length=150)
    provinsi = forms.ModelChoiceField(Provinsi.objects.all(), initial='')
    alamat = forms.CharField(max_length=250, required=True)
    is_default = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(ShippingAddForm, self).__init__(*args, **kwargs)
       
        self.fields['provinsi'].widget.attrs['onClick'] = 'getKota(this.id)'
        self.fields['provinsi'].widget.attrs['style'] = 'width:100%'
 
        self.fields['is_default'].widget.attrs['style'] = 'margin:10px 10px 0 0'
        self.fields['is_default'].widget.attrs['data-toggle'] = 'toggle'

        self.fields['name'].widget.attrs['style'] = 'width:100%; padding:10px'

        self.fields['alamat'].widget = forms.Textarea()
        self.fields['alamat'].widget.attrs['rows'] = '3'
        self.fields['alamat'].widget.attrs['placeholder'] = 'Contoh: Jl. Angkasa 1 Blok AF6 NO 18'
        self.fields['alamat'].widget.attrs['style'] = 'width:100%'

from django import forms
from .models import PurchaseOrder

class OrderAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderAddForm, self).__init__(*args, **kwargs)
        self.fields['is_verified'].widget.attrs['style'] = 'margin:10px 10px 0 0'
        self.fields['is_verified'].widget.attrs['data-toggle'] = 'toggle'
        self.fields['is_verified'].widget.attrs['data-on'] = 'Yes'
        self.fields['is_verified'].widget.attrs['data-off'] = 'No'
        self.fields['is_verified'].widget.attrs['data-onstyle'] = 'success'
        self.fields['is_verified'].widget.attrs['data-offstyle'] = 'danger'

        self.fields['is_valid'].widget.attrs['style'] = 'margin:10px 10px 0 0'
        self.fields['is_valid'].widget.attrs['data-toggle'] = 'toggle'
        self.fields['is_valid'].widget.attrs['data-on'] = 'Yes'
        self.fields['is_valid'].widget.attrs['data-off'] = 'No'
        self.fields['is_valid'].widget.attrs['data-onstyle'] = 'success'
        self.fields['is_valid'].widget.attrs['data-offstyle'] = 'danger'

        self.fields['is_paid'].widget.attrs['style'] = 'margin:10px 10px 0 0'
        self.fields['is_paid'].widget.attrs['data-toggle'] = 'toggle'
        self.fields['is_paid'].widget.attrs['data-on'] = 'Yes'
        self.fields['is_paid'].widget.attrs['data-off'] = 'No'
        self.fields['is_paid'].widget.attrs['data-onstyle'] = 'success'
        self.fields['is_paid'].widget.attrs['data-offstyle'] = 'danger'

    class Meta:
        model = PurchaseOrder
        fields = ('is_verified',
        'is_valid',
        'is_paid',
        )
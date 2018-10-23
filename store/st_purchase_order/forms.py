from django import forms
from .models import PurchaseOrder

class OrderAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderAddForm, self).__init__(*args, **kwargs)
        self.fields['is_verified'].widget.attrs['style'] = 'margin:10px 10px 0 0'
        self.fields['is_verified'].widget.attrs['data-toggle'] = 'toggle'
        
        self.fields['is_valid'].widget.attrs['style'] = 'margin:10px 10px 0 0'
        self.fields['is_valid'].widget.attrs['data-toggle'] = 'toggle'

        self.fields['is_paid'].widget.attrs['style'] = 'margin:10px 10px 0 0'
        self.fields['is_paid'].widget.attrs['data-toggle'] = 'toggle'
        self.fields['is_paid'].widget.attrs['readonly'] = True
        self.fields['is_paid'].widget.attrs['class'] = 'disabled'
        
        self.fields['order_number'].widget.attrs['style'] = 'width:100%; padding:10px; display:none'
        self.fields['service'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['sub_service'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['total_price'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['total_price'].widget.attrs['readonly'] = True
        self.fields['total_price'].widget.attrs['class'] = 'disabled'
        self.fields['discount'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['discount'].widget.attrs['readonly'] = True
        self.fields['discount'].widget.attrs['class'] = 'disabled'
        self.fields['shipping_cost'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['shipping_cost'].widget.attrs['readonly'] = True
        self.fields['shipping_cost'].widget.attrs['class'] = 'disabled'
        self.fields['total_payment'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['total_payment'].widget.attrs['readonly'] = True
        self.fields['total_payment'].widget.attrs['class'] = 'disabled'
        
               

    class Meta:
        model = PurchaseOrder
        fields = ('is_verified',
        'is_valid',
        'is_paid',
        'order_number',
        'service',
        'sub_service',
        'shipping_cost',
        'total_payment',
        'total_price',
        'discount',
        )
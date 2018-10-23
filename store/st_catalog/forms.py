from django import forms
from .models import Product, Category

class CategoryAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['style'] = 'width:100%; padding:10px'
    class Meta:
        model = Category
        fields = ('name',)

class ProductAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductAddForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = '13'
        self.fields['description'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['description'].widget.attrs['placeholder'] = ''
        self.fields['categories'].help_text = 'Pilih Kategori Artikel *(bisa lebih dari 1)'
        self.fields['categories'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['name'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['is_available'].widget.attrs['style'] = 'margin:10px 10px 0 0'
        self.fields['is_available'].widget.attrs['data-toggle'] = 'toggle'
        self.fields['is_archived'].widget.attrs['style'] = 'margin:10px 10px 0 0'
        self.fields['is_archived'].widget.attrs['data-toggle'] = 'toggle'
        self.fields['price'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['unit_weight'].widget.attrs['style'] = 'width:100%; padding:10px'
        
        
    class Meta:
        model = Product
        fields = ('name',
                'description',
                'photo',
                'photo_alt1',
                'photo_alt2',
                'photo_alt3',
                'photo_alt4',
                'photo_alt5',
                'unit_weight',
                'categories',
                'is_available',
                'is_archived',
                'price',)
from django import forms
from company_profile.cp_configs.models import BrandAsset, BrandIdentity, Template, ColorScheme

class AssetEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssetEditForm, self).__init__(*args, **kwargs)
        self.fields['favicon'].widget = forms.FileInput() 
        self.fields['hero_image_1'].widget = forms.FileInput() 
        self.fields['hero_image_2'].widget = forms.FileInput() 
        self.fields['hero_image_3'].widget = forms.FileInput() 
        self.fields['brand_logo'].widget = forms.FileInput() 
        self.fields['main_photo_1'].widget = forms.FileInput() 
        self.fields['main_photo_2'].widget = forms.FileInput() 
        self.fields['extra_image_1'].widget = forms.FileInput() 
        self.fields['extra_image_2'].widget = forms.FileInput() 
        self.fields['extra_image_3'].widget = forms.FileInput() 

    class Meta:
        model = BrandAsset
        fields = ('favicon',
                    'hero_image_1',
                    'hero_image_2',
                    'hero_image_3',
                    'brand_logo',
                    'main_photo_1',
                    'main_photo_2',
                    'extra_image_1',
                    'extra_image_2',
                    'extra_image_3',)

class IdentityEditForm(forms.ModelForm):
    class Meta:
        model = BrandIdentity
        fields = ('company_name',
            'company_tagline', 
            'company_address', 
            'company_email_address',
            'company_phone_number',
            'company_fax_number',
            'company_facebook',
            'company_instagram',
            'company_whatsapp',)

class TemplateEditForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ('name',)

class ColorEditForm(forms.ModelForm):
    class Meta:
        model = ColorScheme
        fields = ('name','primary_color', 'dark_color', 'accent_color',)
from django import forms
from company_profile.cp_configs.models import BrandAsset

class AssetEditForm(forms.ModelForm):
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
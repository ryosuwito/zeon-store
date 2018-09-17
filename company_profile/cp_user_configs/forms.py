from django import forms
from company_profile.cp_configs.models import BrandAsset

class AssetEditForm(forms.ModelForm):
    class Meta:
        model = BrandAsset
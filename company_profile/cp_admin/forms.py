from django import forms
from django.contrib.auth.models import User
from membership.models import Member
from company_profile.cp_user_configs.forms import AssetEditForm, IdentityEditForm

class CmsLoginForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=150)
    attrs = {
        "type": "password"
    }
    password = forms.CharField(label='Password :', widget=forms.PasswordInput(attrs=attrs))


class CmsActivationForm(forms.Form):
    user_id = forms.CharField(label='User ID:', max_length=150)
    access_key = forms.CharField(label='Access Key :')

    def __init__(self, *args, **kwargs):
        super(CmsActivationForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].widget.attrs['type'] = 'hidden'
        self.fields['access_key'].widget.attrs['type'] = 'hidden'

class CmsRegisterForm(forms.Form):
    user_id = forms.CharField(label='User ID:', max_length=150)
    access_key = forms.CharField(label='Access Key :')
    username = forms.CharField(label='Username:', max_length=150)
    attrs = {
        "type": "password"
    }
    password = forms.CharField(label='Password :', widget=forms.PasswordInput(attrs=attrs))
    site_domain = forms.CharField(label='Site Domain:', max_length=150)

    def __init__(self, *args, **kwargs):
        super(CmsRegisterForm, self).__init__(*args, **kwargs)
        self.fields['site_domain'].widget.attrs['style'] = 'width:50%; padding:10px; display:inline-block'
        self.fields['user_id'].widget.attrs['type'] = 'hidden'
        self.fields['access_key'].widget.attrs['type'] = 'hidden'

class CmsBrandAssetsForm(AssetEditForm):
    def __init__(self, *args, **kwargs):
            super(CmsBrandAssetsForm, self).__init__(*args, **kwargs)
            
class CmsBrandIdentityForm(IdentityEditForm):
    def __init__(self, *args, **kwargs):
            super(CmsBrandIdentityForm, self).__init__(*args, **kwargs)
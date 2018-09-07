from django import forms
from taggit import forms as taggit_form
from .models import PageModel
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PageAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
         super(PageAddForm, self).__init__(*args, **kwargs)
         self.fields['title'].widget.attrs['style'] = 'width:100%; padding:10px'
         self.fields['content'].widget = CKEditorUploadingWidget()
    class Meta:
        model = PageModel
        fields = ('title','content')

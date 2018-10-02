from django import forms
from taggit import forms as taggit_form
from .models import PageModel, TempPageModel
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PageAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
         super(PageAddForm, self).__init__(*args, **kwargs)
         self.fields['title'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['meta_description'].widget = forms.Textarea() 
        self.fields['meta_description'].widget.attrs['rows'] = '3'
        self.fields['meta_description'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['meta_description'].widget.attrs['placeholder'] = ''
        self.fields['content'].widget = CKEditorUploadingWidget()
        self.fields['meta_keyword'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['meta_keyword'].help_text = 'Bisa lebih dari 1, pisahkan dengan koma ( , )'
        self.fields['meta_keyword'].required = False
    class Meta:
        model = PageModel
        fields = ('title',
            'content',
            'is_published',
            'banner_image_1',
            'banner_image_2',
            'banner_image_3',
            'meta_description',
            'meta_keyword')

class PagePreviewForm(PageAddForm):
    class Meta:
        model = TempPageModel
        fields = ('title',
            'content',
            'is_published',
            'banner_image_1',
            'banner_image_2',
            'banner_image_3',
            'meta_description',
            'meta_keyword')
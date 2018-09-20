from django import forms
from taggit import forms as taggit_form
from .models import Article, TempArticle, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CategoryAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryAddForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['style'] = 'width:100%; padding:10px'
    class Meta:
        model = Category
        fields = ('title',)

class ArticleAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleAddForm, self).__init__(*args, **kwargs)
        self.fields['category'].help_text = 'Pilih Kategori Artikel *(bisa lebih dari 1)'
        self.fields['category'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['title'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['is_featured'].widget.attrs['style'] = 'margin:10px 10px 0 0'
        self.fields['is_featured'].widget.attrs['data-toggle'] = 'toggle'
        self.fields['is_published'].widget.attrs['style'] = 'margin:10px 10px 0 0'
        self.fields['is_published'].widget.attrs['data-toggle'] = 'toggle'
        self.fields['lead_in'].widget = forms.Textarea() 
        self.fields['lead_in'].widget.attrs['rows'] = '3'
        self.fields['lead_in'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['lead_in'].widget.attrs['placeholder'] = ''
        self.fields['content'].widget = CKEditorUploadingWidget()
        self.fields['tags'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['tags'].help_text = 'Bisa lebih dari 1, pisahkan dengan koma ( , )'
        self.fields['tags'].required = False
    class Meta:
        model = Article
        fields = ('title','content','is_published','is_featured','featured_image', 'category', 'tags', 'lead_in')

class ArticlePreviewForm(ArticleAddForm):
    class Meta:
        model = TempArticle
        fields = ('title','content','is_published','is_featured','featured_image', 'category', 'tags', 'lead_in')
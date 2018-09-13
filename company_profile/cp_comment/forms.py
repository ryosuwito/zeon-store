from django import forms
from .models import Comment, Reply, Visitor

class AddVisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor

class AddCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.fields['content'].widget = forms.Textarea() 
        self.fields['content'].widget.attrs['rows'] = '3'
        self.fields['content'].widget.attrs['style'] = 'width:100%; padding:10px'
        self.fields['content'].widget.attrs['placeholder'] = 'Komentar Anda'
    class Meta:
        model = Comment
        fields = ('content')

class AddReplyForm(AddCommentForm):
    class Meta(AddCommentForm.Meta):
        model = Reply

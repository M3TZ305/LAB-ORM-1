from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        labels = {
            'title': _('Title'),
            'content': _('Content'),
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': _('Write a thoughtful title...'),
                'maxlength': '2048',
                'required': True,
                'id': 'post-title-input',
                'dir': 'auto',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': _('Write your article or reflection here...'),
                'rows': 10,
                'required': True,
                'id': 'post-content-input',
                'dir': 'auto',
            }),
        }
        error_messages = {
            'title': {
                'required': _('Please enter an article title.'),
                'max_length': _('The title is too long (maximum 2048 characters).'),
            },
            'content': {
                'required': _('Please enter the article content.'),
            },
        }

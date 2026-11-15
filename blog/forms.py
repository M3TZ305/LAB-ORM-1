from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post
from .validators import validate_publisher_name, validate_article_title, validate_article_content


class PostForm(forms.ModelForm):
    publisher_name = forms.CharField(
        max_length=150,
        required=True,
        validators=[validate_publisher_name],
        label=_('Publisher Name'),
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': _('Enter publisher name...'),
            'maxlength': '150',
            'required': True,
            'id': 'post-publisher-input',
            'dir': 'auto',
        })
    )

    title = forms.CharField(
        max_length=2048,
        required=True,
        validators=[validate_article_title],
        label=_('Article Title'),
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': _('Enter article title...'),
            'maxlength': '2048',
            'required': True,
            'id': 'post-title-input',
            'dir': 'auto',
        })
    )

    content = forms.CharField(
        required=True,
        validators=[validate_article_content],
        label=_('Article Content'),
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': _('Enter article content...'),
            'rows': 10,
            'required': True,
            'id': 'post-content-input',
            'dir': 'auto',
        })
    )

    class Meta:
        model = Post
        fields = ['publisher_name', 'title', 'content']
        labels = {
            'publisher_name': _('Publisher Name'),
            'title': _('Article Title'),
            'content': _('Article Content'),
        }

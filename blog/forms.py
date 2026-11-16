from django import forms
from .models import Post
from .validators import validate_publisher_name, validate_article_title, validate_article_content
from media_library.forms import MultipleFileField

class PostForm(forms.ModelForm):
    publisher_name = forms.CharField(label='اسم الناشر', max_length=150, validators=[validate_publisher_name])
    title = forms.CharField(label='عنوان المقال', max_length=2048, validators=[validate_article_title])
    published_at = forms.DateTimeField(label='تاريخ ووقت النشر (الرياض)', input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S'], widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M:%S', attrs={'type':'datetime-local','step':'1','class':'form-input','dir':'ltr','lang':'en'}))
    content = forms.CharField(label='محتوى المقال', widget=forms.Textarea, validators=[validate_article_content])
    attachments = MultipleFileField(label='المرفقات', required=False, help_text='صور ومستندات: حتى 5 ملفات، بحد 10 ميجابايت لكل ملف.')
    remove_attachments = forms.ModelMultipleChoiceField(label='إزالة المرفقات المحددة نهائيًا عند الحفظ', queryset=None, required=False, widget=forms.CheckboxSelectMultiple)
    featured = forms.ModelChoiceField(label='صورة الغلاف', queryset=None, required=False, empty_label='الصورة الافتراضية')
    feature_new = forms.BooleanField(label='استخدام أول صورة جديدة كغلاف', required=False)
    class Meta:
        model = Post
        fields = ['publisher_name', 'title', 'published_at', 'content']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            from django.utils import timezone
            self.fields['published_at'].initial = timezone.localtime()
        for name in ['publisher_name', 'title', 'published_at', 'content']:
            self.fields[name].required = True
            self.fields[name].error_messages['required'] = 'هذا الحقل مطلوب.'
        self.fields['published_at'].error_messages['invalid'] = 'أدخل تاريخا ووقتا صحيحين بتوقيت الرياض.'
        from media_library.models import PostAttachment
        qs = self.instance.attachments.all() if self.instance.pk else PostAttachment.objects.none()
        self.fields['remove_attachments'].queryset = qs
        self.fields['featured'].queryset = qs.filter(file_type__startswith='image/')
        self.fields['featured'].initial = qs.filter(is_featured=True).first()
        for name, field in self.fields.items():
            if name in ['publisher_name','title','content']:
                field.widget.attrs.update({'class': 'form-textarea' if name == 'content' else 'form-input', 'dir':'auto'})
    def clean(self):
        data = super().clean()
        from django.conf import settings
        existing = self.instance.attachments.count() if self.instance.pk else 0
        removed = len(data.get('remove_attachments', []))
        if existing - removed + len(data.get('attachments', [])) > settings.MAX_POST_ATTACHMENTS:
            self.add_error('attachments', 'الحد الأقصى للمرفقات في المقال هو ٥ ملفات.')

        return data

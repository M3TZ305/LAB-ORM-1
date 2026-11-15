from django.db import models
from django.conf import settings
from django.utils.translation import get_language
from .validators import validate_publisher_name, validate_article_title, validate_article_content


class Post(models.Model):
    publisher_name = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )
    title = models.CharField(max_length=2048)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if self.publisher_name:
            validate_publisher_name(self.publisher_name)
        if self.title:
            validate_article_title(self.title)
        if self.content:
            validate_article_content(self.content)

    def __str__(self):
        return f"{self.title} ({self.publisher_name})" if self.publisher_name else self.title

    def get_title(self, lang_code=None):
        if not lang_code:
            lang_code = get_language()
        translation = self.translations.filter(language_code=lang_code).first()
        if translation:
            return translation.title
        return self.title

    def get_content(self, lang_code=None):
        if not lang_code:
            lang_code = get_language()
        translation = self.translations.filter(language_code=lang_code).first()
        if translation:
            return translation.content
        return self.content

    def get_image_url(self, is_detail=False):
        if self.id == 1:
            return '/static/blog/img/posts/siyaq-city.webp'
        elif self.id == 2:
            return '/static/blog/img/posts/siyaq-reading.webp'
        else:
            images = [
                '/static/blog/img/posts/siyaq-city.webp',
                '/static/blog/img/posts/siyaq-reading.webp',
            ]
            idx = (self.id - 1) % len(images) if self.id else 0
            return images[idx]


class PostTranslation(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='translations')
    language_code = models.CharField(max_length=10, choices=settings.LANGUAGES, default='ar')
    title = models.CharField(max_length=2048)
    content = models.TextField()

    class Meta:
        unique_together = ('post', 'language_code')

    def __str__(self):
        return f"[{self.language_code}] {self.title}"

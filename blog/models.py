from django.db import models
from django.conf import settings
from django.utils import timezone
from .validators import validate_publisher_name, validate_article_title, validate_article_content


class Post(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="posts")
    publisher_name = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )
    title = models.CharField(max_length=2048)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now, verbose_name="تاريخ النشر")

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

    def can_manage(self, user):
        return user.is_authenticated and (user.is_staff or user.is_superuser or self.owner_id == user.pk)

    def get_image_url(self, is_detail=False):
        images = [attachment for attachment in self.attachments.all() if attachment.file_type.startswith('image/')]
        for attachment in images:
            if attachment.is_featured and attachment.file_type.startswith('image/'):
                from django.urls import reverse
                return reverse('media_library:attachment', args=[attachment.pk])
        if images:
            from django.urls import reverse
            return reverse('media_library:attachment', args=[images[0].pk])
        if self.id == 1:
            return '/static/blog/img/posts/siyaq-city.webp'
        elif self.id == 2:
            return '/static/blog/img/posts/siyaq-reading.webp'
        return '/static/blog/img/posts/default-cover.svg'

from pathlib import Path
from uuid import uuid4
from django.db import models
from .validators import validate_upload
def upload_path(instance, filename):
    ext = Path(filename).suffix.lower()
    folder = 'images' if ext in ['.jpg','.jpeg','.png','.webp','.gif'] else ('pdf' if ext == '.pdf' else 'documents')
    return f'{folder}/{uuid4().hex}{ext}'
class PostAttachment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=upload_path, validators=[validate_upload])
    original_filename = models.CharField(max_length=200)
    file_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    class Meta:
        ordering = ['uploaded_at', 'id']
        constraints = [models.UniqueConstraint(fields=['post'], condition=models.Q(is_featured=True), name='one_featured_attachment')]
    def __str__(self): return self.original_filename

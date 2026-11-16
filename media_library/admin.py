from django.contrib import admin
from .models import PostAttachment
@admin.register(PostAttachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('original_filename','post','file_type','uploaded_at')
    readonly_fields = ('post','file','original_filename','file_type','uploaded_at','is_featured')
    def has_add_permission(self, request): return False

from django.apps import AppConfig
class MediaLibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'media_library'
    verbose_name = 'مكتبة الوسائط'
    def ready(self):
        from . import signals

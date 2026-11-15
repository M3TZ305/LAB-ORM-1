from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from blog.views import legacy_lang_redirect

urlpatterns = [
    path('', RedirectView.as_view(url='/home/', permanent=False)),
    path('', include('blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('ar/<path:subpath>', legacy_lang_redirect, {'lang': 'ar'}),
    path('en/<path:subpath>', legacy_lang_redirect, {'lang': 'en'}),
    path('ar', legacy_lang_redirect, {'lang': 'ar', 'subpath': 'home/'}),
    path('en', legacy_lang_redirect, {'lang': 'en', 'subpath': 'home/'}),
]

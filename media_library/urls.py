from django.urls import path
from .views import attachment
app_name = 'media_library'
urlpatterns = [path('<int:attachment_id>/', attachment, name='attachment')]

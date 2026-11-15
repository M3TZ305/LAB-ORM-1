from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    # Add post
    path('add/', views.add_post, name='add_post'),
    # Post detail with integer path parameter
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    # Set theme preference with string path parameter
    path('theme/<str:mode>/', views.set_theme, name='set_theme'),
]

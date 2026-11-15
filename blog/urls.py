from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('add/', views.add_post, name='add_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('theme/<str:mode>/', views.set_theme, name='set_theme'),
]

from django.contrib import admin
from .models import Post, PostTranslation


class PostTranslationInline(admin.TabularInline):
    model = PostTranslation
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher_name', 'is_published', 'published_at')
    list_filter = ('is_published', 'published_at')
    search_fields = ('title', 'publisher_name', 'content')
    ordering = ('-published_at', '-id')
    date_hierarchy = 'published_at'
    inlines = [PostTranslationInline]


@admin.register(PostTranslation)
class PostTranslationAdmin(admin.ModelAdmin):
    list_display = ('post', 'language_code', 'title')
    list_filter = ('language_code',)
    search_fields = ('title', 'content')

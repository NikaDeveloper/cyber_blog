from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import User, Post, Comment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'is_staff')
    search_fields = ('username', 'email')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_link', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content')

    def author_link(self, obj):
        url = reverse('admin:blog_user_change', args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', url, obj.author.username)

    author_link.short_description = 'Автор'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)

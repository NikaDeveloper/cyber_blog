from django.contrib.auth.models import AbstractUser
from django.db import models

from blog.validators import validate_email_domain, validate_forbidden_words, validate_author_age


class User(AbstractUser):
    email = models.EmailField(unique=True, validators=[validate_email_domain], verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Номер телефона")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок", validators=[validate_forbidden_words])
    content = models.TextField(verbose_name="Текст")
    # null=True, blank=True — потому что картинка может отсутствовать
    image = models.ImageField(upload_to='posts/', null=True, blank=True, verbose_name="Изображение")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="Автор")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.author:
            validate_author_age(self.author)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Пост")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="Автор")
    text = models.TextField(verbose_name="Текст комментария")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

from rest_framework import serializers
from .models import User, Post, Comment
from datetime import date


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели пользователя.
    Обрабатывает регистрацию и просмотр профиля"""
    # пароль можно только отправить при регистрации, но нельзя прочитать
    password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_birth_date(value):
        """ Проверка, что пользователю есть 18 лет."""
        if value:
            today = date.today()
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 18:
                raise serializers.ValidationError("Регистрация разрешена только с 18 лет")
        return value

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone', 'birth_date']

    def create(self, validated_data):
        """ Создание пользователя с хешированием пароля """
        user = User.objects.create_user(**validated_data)
        return user


class CommentSerializer(serializers.ModelSerializer):
    """ Сериализатор для комментариев """
    # поле 'author' доступно только для чтения и возвращает username
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'text', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    """ Сериализатор для постов """
    # имя автора вместо id
    author = serializers.ReadOnlyField(source='author.username')
    # вывод комментов сразу в посте
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'author', 'comments', 'created_at', 'updated_at']

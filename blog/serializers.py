from rest_framework import serializers
from .models import User, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    # пароль можно только отправить при регистрации, но нельзя прочитать
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone', 'birth_date']

    def create(self, validated_data):
        # хеширование пароля перед сохранением
        user = User.objects.create_user(**validated_data)
        return user


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'text', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    # имя автора вместо id
    author = serializers.ReadOnlyField(source='author.username')
    # вывод комментов сразу в посте
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'author', 'comments', 'created_at', 'updated_at']

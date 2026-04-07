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

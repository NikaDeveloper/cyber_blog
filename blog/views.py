from rest_framework import viewsets, permissions
from .models import User, Post, Comment
from .serializers import UserSerializer, CommentSerializer, PostSerializer
from .permissions import IsOwnerOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing users """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            # регистрация доступна всем
            return [permissions.AllowAny()]
        if self.action in ['update', 'partial_update']:
            # редактировать может только сам себя или админ
            return [IsOwnerOrAdmin()]
        if self.action == 'destroy':
            # удалять может только админ
            return [permissions.IsAdminUser()]
        # читать могут только авторизованные или админы
        return [permissions.IsAuthenticated()]


class PostViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing posts """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # читать могут все
            return [permissions.AllowAny()]
        if self.action == 'create':
            # создавать только авторизованные
            return [permissions.IsAuthenticated()]
        # обновлять и удалять только владелец или админ
        return [IsOwnerOrAdmin()]

    def perform_create(self, serializer):
        """ Create a new post """
        # автоматически автор поста текущий юзер
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing comments """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        """ Allow users to edit their own comments """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrAdmin()]

    def perform_create(self, serializer):
        """ Create a new post """
        # текущий юзер автор коммента
        serializer.save(author=self.request.user)

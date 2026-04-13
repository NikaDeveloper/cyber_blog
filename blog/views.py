from rest_framework import viewsets, permissions
from .models import User, Post, Comment
from .serializers import UserSerializer, CommentSerializer, PostSerializer
from .permissions import IsOwnerOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    """ ViewSet для управления профилями пользователей """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action == 'destroy':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]


class PostViewSet(viewsets.ModelViewSet):
    """ ViewSet для работы с постами.
    Поддерживает создание, чтение, обновление и удаление. """

    queryset = Post.objects.all().prefetch_related('comments', 'author')
    serializer_class = PostSerializer

    def get_permissions(self):
        """ Определяет права доступа в зависимости от действия. """
        if self.action in ['list', 'retrieve']:
            # читать могут все
            return [permissions.AllowAny()]
        if self.action == 'create':
            # создавать только авторизованные
            return [permissions.IsAuthenticated()]
        # обновлять и удалять только владелец или админ
        return [IsOwnerOrAdmin()]

    def perform_create(self, serializer):
        """ Сохраняет пост, устанавливая текущего пользователя автором. """
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ ViewSet для работы с комментариями """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        """ Разрешает юзерам редактировать их комменты """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrAdmin()]

    def perform_create(self, serializer):
        """ Сохраняет комментарий, устанавливая текущего пользователя автором """
        serializer.save(author=self.request.user)

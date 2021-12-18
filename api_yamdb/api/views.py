import secrets

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, mixins, viewsets
from rest_framework.pagination import (LimitOffsetPagination, 
                                       PageNumberPagination,)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title, User
from . import permissions, serializers


class EmailConfirmation(APIView):
    """Отправка кода подтверждения на email, переданный в запросе."""
    def post(self, request):
        email = request.data.get('email')
        confirmation_code = secrets.token_hex(15)
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            send_mail(
                'Код подтверждения',
                confirmation_code,
                'from@yamdb.com',
                [email],
                fail_silently=False,
            )
            serializer.save(confirmation_code=confirmation_code, role='user')
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetToken(APIView):
    "Создание JWT токена."
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'token': str(refresh.access_token),
        }

    def post(self, request):
        serializer = serializers.TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=request.data.get('username'))
            return Response(self.get_tokens_for_user(user), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminOrReadOnlyViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = [permissions.AdminOrReadOnlyPermission]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',) 


class CategoryViewSet(AdminOrReadOnlyViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class GenreViewSet(AdminOrReadOnlyViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.AdminOrReadOnlyPermission] 


class AuthorAdminOrReadOnlyViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AuthorAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ReviewViewSet(AuthorAdminOrReadOnlyViewSet):
    """Всьюстер для модели Review."""
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer


class CommentViewSet(AuthorAdminOrReadOnlyViewSet):
    """Всьюстер для модели Comment."""
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

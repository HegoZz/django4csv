from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, mixins, viewsets
from rest_framework.pagination import (LimitOffsetPagination, 
                                       PageNumberPagination,)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from reviews.models import Category, Genre, Review, Title, User
from reviews.models import generate_confirmation_code
from . import permissions, serializers


class EmailConfirmation(APIView):
    """Отправка кода подтверждения на email, переданный в запросе."""
    def post(self, request):
        email = request.data.get('email')
        confirmation_code = generate_confirmation_code()
        serializer = serializers.UserConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            send_mail(
                'Код подтверждения',
                confirmation_code,
                'from@yamdb.com',
                [email],
                fail_silently=False,
            )
            serializer.save(confirmation_code=confirmation_code)
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
            return Response(self.get_tokens_for_user(user),
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryAndGenreViewSet(mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    permission_classes = [permissions.IsSuperuserOrReadOnly]
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class CategoryViewSet(CategoryAndGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class GenreViewSet(CategoryAndGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsSuperuserOrReadOnly|IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return serializers.TitlePostUpdateSerializer
        return serializers.TitleSerializer


class ReviewAndCommentViewSet(viewsets.ModelViewSet):
    permissions_classes = (permissions.AuthorAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ReviewViewSet(ReviewAndCommentViewSet):
    """Всьюстер для модели Review."""
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def perform_create(self, serializer):
        title = Title.objects.get(id=self.kwargs['title_id'])
        serializer.save(title_id=title, author=self.request.user)

    # def get_queryset(self):
    #     title = get_object_or_404(Title, id=self.kwargs['title_id'])
    #     return title.reviews.all()


class CommentViewSet(ReviewAndCommentViewSet):
    """Всьюстер для модели Comment."""
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'
    permission_classes = (permissions.IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)

    @action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, pk=None):
        if request.method == 'GET':
            serializer = self.get_serializer(instance=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.user.role == 'user':
            serializer = serializers.UserRoleSerializer(instance=request.user, data=request.data, partial=True)
        else:
            serializer = self.get_serializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

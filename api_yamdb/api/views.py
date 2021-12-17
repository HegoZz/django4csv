from django.shortcuts import render

from django.core.mail import send_mail
from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .permissions import AdminOrReadOnlyPermission
from reviews.models import Category, Genre, Title


# send_mail(
#     'Тема письма',
#     'Текст письма.',
#     'from@example.com',  # Это поле "От кого"
#     ['to@example.com'],  # Это поле "Кому" (можно указать список адресов)
#     fail_silently=False, # Сообщать об ошибках («молчать ли об ошибках?»)
# )


class AdminOrReadOnlyViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = (AdminOrReadOnlyPermission)


class CategoryViewSet(AdminOrReadOnlyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(AdminOrReadOnlyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnlyPermission)
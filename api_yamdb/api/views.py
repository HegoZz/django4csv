import secrets

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User
from .serializers import TokenSerializer, UserSerializer


class EmailConfirmation(APIView):
    """Отправка кода подтверждения на email, переданный в запросе."""
    def post(self, request):
        email = request.data.get('email')
        confirmation_code = secrets.token_hex(15)
        serializer = UserSerializer(data=request.data)
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
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=request.data.get('username'))
            return Response(self.get_tokens_for_user(user), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

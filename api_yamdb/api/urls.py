from django.urls import path
from .views import EmailConfirmation, GetToken


urlpatterns = [
    path('v1/auth/signup/', EmailConfirmation.as_view()),
    path('v1/auth/token/', GetToken.as_view()),
#     path('v1/users/me/', )
]
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

router = SimpleRouter()

router.register('categories', views.CategoryViewSet)
router.register('genres', views.GenreViewSet)
router.register('titles', views.TitleViewSet)

urlpatterns = [
    # path('v1/auth/signup/', ),
    # path('v1/auth/token/', ),
    # path('v1/users/me/', )
    path('v1/', include(router.urls)),
]
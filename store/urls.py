
from django.urls import include, path
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.ColletionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
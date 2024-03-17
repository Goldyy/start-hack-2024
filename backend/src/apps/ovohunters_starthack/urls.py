from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.ovo_hunter_viewset import OvoHunterViewset

router = DefaultRouter()
router.register(r"ovo-hunters", OvoHunterViewset)

urlpatterns = [
    path("", include(router.urls)),
]
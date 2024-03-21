from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceLocationRetrieveView, DeviceLocationManagerApiView, DeviceLocationViewSet

router = DefaultRouter()
router.register(r"device-locations", DeviceLocationViewSet, basename="device-locations")


urlpatterns = [
    path("", include(router.urls)),
    path("device-location-manager/", DeviceLocationManagerApiView.as_view(), name="device-location-manager"),
    path("device-locations/by_mac_address/<str:mac_address>/", DeviceLocationRetrieveView.as_view(), name="device-location-manager")
]
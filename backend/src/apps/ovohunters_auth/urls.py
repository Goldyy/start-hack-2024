from django.urls import path
from .views import (
    FetchKeycloakGroupsView,
    CreateKeycloakGroupView,
    DeleteKeycloakGroupView, FetchKeycloakGroupView
)

urlpatterns = [
    path("keycloak/groups/", FetchKeycloakGroupsView.as_view()),
    path("keycloak/group/<str:group_id>", FetchKeycloakGroupView.as_view()),
    path("keycloak/group/create/", CreateKeycloakGroupView.as_view()),
    path("keycloak/group/delete/<str:group_id>", DeleteKeycloakGroupView.as_view()),
]

from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
import os

from .mixins import KeycloakServicesMixins
from .services import create_keycloak_group, delete_keycloak_group, get_group

import logging
import inspect

logger = logging.getLogger(__name__)


class FetchKeycloakGroupsView(APIView):
    """
    API-View zum Abrufen aller Keycloak-Gruppen.

    Methoden:
        get(request): Alle Keycloak-Gruppen abrufen.
    """    
    def get(self, request):
        """
        Alle Keycloak-Gruppen abrufen, die dem User zugebordnet sind. Ein User ist einer Gruppe zugeordnet, wenn er mindestens eine Rolle in der Gruppe hat.

        Args:
            request: Das HTTP-Anfrageobjekt.

        Returns:
            Response: Ein Response-Objekt, das das Ergebnis der Abruffunktion enthält.
        """
        logger.trace("Class: " + str(self.__class__.__name__) + "; Method called: " + inspect.currentframe().f_code.co_name)
        logger.info("Starting to fetch all groups")

        user_groups:list[str] = request.user_groups
        user_groups_attributes:dict[str,str] = []

        for user_group in user_groups:
            user_groups_attributes.append(get_group(user_group))
            

        response = Response()
        response.data = user_groups_attributes
        logger.info("All groups fetched.")
        return response

class FetchKeycloakGroupView(APIView):
    """
    API-View zum Abrufen einer Keycloak-Gruppe.
    
    Methoden:
        get(request, group_id): Eine Keycloak-Gruppe abrufen.
    """
    def get(self, request, group_id:str):
        """
        Eine Keycloak-Gruppe abrufen. Ein User kann nur Gruppen abrufen, denen er selbst zugeordnet ist.

        Args:
            request: Das HTTP-Anfrageobjekt.
            group_id: Die ID der abzurufenden Gruppe.

        Returns:
            Response: Ein Response-Objekt, das das Ergebnis der Abruffunktion enthält.
        """
        logger.trace("Class: " + str(self.__class__.__name__) + "; Method called: " + inspect.currentframe().f_code.co_name)
        logger.info("Starting to fetch group with ID: " + group_id)

        response = Response()
        if os.environ.get("API_AUTHENTICATION", "True") == "False":
            response.data = get_group(group_id)

        else:
            if group_id in request.user_groups:
                response.data = get_group(group_id)
            else:
                response.data = []
                response.status_code = 403
        logger.info("Group with ID " + group_id + " fetched.")
        return response

class CreateKeycloakGroupView(APIView, KeycloakServicesMixins):
    """
    API-View zum Erstellen einer Keycloak-Gruppe mit Hilfe der Keycloak Services.

    Diese Ansicht verwendet die KeycloakServicesMixins, um auf die erforderlichen Attribute und Methoden im Zusammenhang mit den Keycloak Services zuzugreifen.

    Methoden:
        post(request): Erstellen einer Keycloak-Gruppe mit der Keycloak ADMIN REST API.

    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "groupName": openapi.Schema(type=openapi.TYPE_STRING),
                "attributes": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "address": openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            }
        )
    )
    def post(self, request):
        """
        Erstellen einer Keycloak-Gruppe mit Hilfe der Keycloak Services.

        Args:
            request: Das HTTP-Anfrageobjekt.

        Returns:
            Response: Ein Response-Objekt, das das Ergebnis der Gruppenerstellung enthält.

        """
        
        logger.trace("Class: " + str(self.__class__.__name__) + "; Method called: " + inspect.currentframe().f_code.co_name)
        logger.info("Starting to create group with name: " + request.data["groupName"])
        response = create_keycloak_group(request.data["groupName"], request.data["attributes"]["address"], request.user_id)
        logger.info("Group with name " + request.data["groupName"] + " created.")
        return response

class DeleteKeycloakGroupView(APIView, KeycloakServicesMixins):
    """
    API-View zum Löschen einer Keycloak-Gruppe mit Hilfe der Keycloak Services.

    Methoden:
        delete(request, group_id): Löschen einer Keycloak-Gruppe mit der Keycloak ADMIN REST API.
    """
    def delete(self, request, group_id:str):
        """
        Löschen einer Keycloak-Gruppe mit Hilfe der Keycloak Services. Ein User kann nur eine Gruppe löschen, der er selbst zugeordnet ist.

        Args:
            request: Das HTTP-Anfrageobjekt.
            group_id: Die ID der zu löschenden Gruppe.

        Returns:
            Response: Ein Response-Objekt, das das Ergebnis der Löschfunktion enthält.
        """
        logger.trace("Class: " + str(self.__class__.__name__) + "; Method called: " + inspect.currentframe().f_code.co_name)
        logger.info("Starting to delete group with ID: " + group_id)

        if group_id in request.user_groups:
            response = delete_keycloak_group(group_id)
            logger.info("Group with ID " + group_id + " deleted.")
        else:
            response = Response()
            response.status_code = 403
            logger.debug("User does not belong to group.")
            response.data = {"error": "User does not belong to group."}
        return response

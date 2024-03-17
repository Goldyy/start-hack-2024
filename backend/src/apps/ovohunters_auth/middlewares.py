import os
from keycloak import KeycloakOpenID
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from apps.ovo-hunters_auth.services import get_user_groups, get_user_roles, fetch_keycloak_groups, get_user_id
from django.urls import reverse

import logging

logger = logging.getLogger(__name__)


class KeycloakAuthorizationMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        
    def process_request(self, request):
        if os.environ.get("API_AUTHENTICATION", "True") == "False":
            logger.info("API_AUTHENTICATION is set to False. Skipping Keycloak Authorization.")
            #setting user groups to all avaialble groups
            all_groups_object = fetch_keycloak_groups()
            all_groups = []
            for group_object in all_groups_object:
                all_groups.append(group_object["id"])
            request.user_groups = all_groups


            return self.get_response(request)

        elif not "api/schema" in request.path:
            logger.info("Adding user_id, user_groups and user_roles to request object.")

            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header == '':
                return JsonResponse({"error": "Authorization header missing"}, status=401)
            
            auth_token = auth_header.split()[1]
      
            user_groups:list[str] = get_user_groups(auth_token)
            request.user_groups:list[str] = user_groups

            user_roles = get_user_roles(auth_token)
            request.user_roles = user_roles

            request.user_id = get_user_id(auth_token)
            logger.info("Finished adding auth info to request object.")
            return self.get_response(request)

        else:
            return self.get_response(request)


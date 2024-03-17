from functools import wraps
from django.http import JsonResponse

import logging

logger = logging.getLogger(__name__)

def api_permission_required(required_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):            
            user_roles = self.request.user_roles
            
            logger.info(f'Checking permissions for user {self.request.user.username}')
            logger.debug(f'Required roles: {required_roles}')
            logger.debug(f'User roles: {user_roles}')
            
            if not any(item in user_roles for item in required_roles):                
                logger.warning(f'Access denied for user {self.request.user.username}')
                logger.warning(f'Required roles: {required_roles}')
                logger.warning(f'User roles: {user_roles}')

                return JsonResponse({"error": "The user does not have the required permissions"}, status=403)
            
            logger.info(f'Access granted for user {self.request.user.username}')
            logger.info(f'User roles: {user_roles}')

            return view_func(self, request, *args, **kwargs)

        return _wrapped_view

    return decorator

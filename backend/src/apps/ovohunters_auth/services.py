import os
import requests
from rest_framework.response import Response

import logging

# Logger initialisieren
logger = logging.getLogger(__name__)

"""
This module contains functions to interact with Keycloak. 

Important: When using the module make sure the user you are acting on behalf of has the required permissions.
"""

def get_admin_token():
    """
    Function to retrieve an access token for the keycloak admin REST API.
    
    Returns:
        Response: A Response object containing the result of the token retrieval.
    """
    token_url = f"{os.getenv('KEYCLOAK_URL')}/realms/{os.getenv('REALM')}/protocol/openid-connect/token"    
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': os.getenv('ADMIN_CLIENT_ID'),
        'client_secret': os.getenv('ADMIN_CLIENT_SECRET')
    }    
    return requests.post(token_url, data=token_data, verify=False)

def get_backend_token():
    """
    Function to retrieve an access token for the backend client.
    
    Returns:
        Response: A Response object containing the result of the token retrieval.
    """
    token_url = f"{os.getenv('KEYCLOAK_URL')}/realms/{os.getenv('REALM')}/protocol/openid-connect/token"
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET')
    }
    return requests.post(token_url, data=token_data, verify=False)

def fetch_keycloak_groups()->list[dict[str, str]]:
    """
    Retrieves all groups from Keycloak.
    
    Returns:
        list[dict[str, str]]: A list of dictionaries containing the group information.
        
    """
    token_response = get_admin_token()
    groups = []
    if token_response.status_code == 200:
        access_token = token_response.json()['access_token']
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        groups_url = f"{os.getenv('KEYCLOAK_URL')}/admin/realms/{os.getenv('REALM')}/groups"
        
        keycloak_response = requests.get(groups_url, headers=headers)

        if keycloak_response.status_code == 200:
            data = keycloak_response.json()    
                   
            for group in data:
                groups.append(get_group(group["id"]))
            return groups
        else:
            logger.debug(f"Failed to retrieve groups. Status code: {keycloak_response.status_code}")
            return []
    else:
        logger.debug(f"Failed to obtain access token. Status code: {token_response.status_code}")
        return []
    


def get_group(group_id:str)->dict[str, str]:
    """
    Retrieves the id, name and attributes of a group by the group ID.
    
    Args:
        group_id(str): The ID of the group.
        
    Returns:
        dict[str, str]: A dictionary containing the group information.
        
    """
    group_infos = fetch_group_infos(group_id)
    group = {
        "id": group_id,
        "name": group_infos["name"],
        "attributes": group_infos["attributes"]
    }
    return group

def get_group_names_by_ids(group_ids:list[str])->list[str]:
    """
    Retrieves the names of groups by the group IDs.
    
    Args:
        group_ids(str[]): The IDs of the groups.
        
    Returns:
        str[]: The names of the groups.
        
    """
    group_names = []
    for id in group_ids:
        group_infos = fetch_group_infos(id)
        group_names.append(group_infos["name"])
    return group_names

def get_group_names_as_dict_by_ids(group_ids:list[str])->list[dict[str, str]]:
    """
    Retrieves the names of groups by the group IDs.
    
    Args:
        group_id(str[]): The IDs of the groups.
        
    Returns:
        dict[str, str][]: The names of the groups.
        
    """
    keycloak_groups_names = get_group_names_by_ids(group_ids)
    keycloak_groups_as_dict = []
    for i, id in enumerate(group_ids):
        keycloak_groups_as_dict.append({"id": id, "name": keycloak_groups_names[i]})

    return keycloak_groups_as_dict



def fetch_group_infos(group_id)->dict[str, str]:
    """
    Retrieves the information of a group by the group ID.
    
    Args:
        group_id(str): The ID of the group.
        
    Returns:
        dict[str, str]: A dictionary containing the group information.
        
    """
    token_response = get_admin_token()
    group = {}

    if token_response.status_code == 200:
        access_token = token_response.json()['access_token']
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        groups_url = f"{os.getenv('KEYCLOAK_URL')}/admin/realms/{os.getenv('REALM')}/groups/{group_id}"
        response = requests.get(groups_url, headers=headers)
        
        if response.status_code == 200:
            group = response.json()
        else:
            logger.debug(f"Failed to retrieve group infos. Status code: {response.status_code}")
    else:
        logger.debug(f"Failed to obtain access token. Status code: {token_response.status_code}")
    return group

def add_user_to_group(user_id:str, group_id:str)-> Response:
    """
    Adds a user to a group. When using, make sure the user has the required permissions.

    Args:
        user_id(str): The ID of the user to be added to the group.
        group_id(str): The ID of the group to which the user is to be added.

    Returns:
        Response: A Response object containing the result of the addition.
    """
    token_response = get_admin_token()
    response = Response()

    if token_response.status_code == 200:
        access_token = token_response.json()['access_token']
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        group_url = f"{os.getenv('KEYCLOAK_URL')}/admin/realms/{os.getenv('REALM')}/users/{user_id}/groups/{group_id}"
        keycloak_response = requests.put(group_url, headers=headers)

        if keycloak_response.status_code == 204:
            logger.info(f"User with ID {user_id} has been added to group with ID {group_id}.")
            response = Response({'message': f"User with ID {user_id} has been added to group with ID {group_id}."}, status=200)
        else:
            logger.info(f"Failed to add user with ID {user_id} to group with ID {group_id}. Status code: {keycloak_response.status_code}")
            response = Response({'message': f"Failed to add user with ID {user_id} to group with ID {group_id}. Status code: {keycloak_response.status_code}"}, status=keycloak_response.status_code)
    else:
        logger.info(f"Failed to obtain access token. Status code: {token_response.status_code}")
        response = Response({'message': f"Failed to obtain access token. Status code: {token_response.status_code}"})

    return response

def get_groupid_by_name(group_name:str)->str:
    """
    Retrieves the ID of a group by the group name.
    
    Args:
        group_name(str): The name of the group.
        
    Returns:
        group_id(str): The ID of the group.
            
    """
    token_response = get_admin_token()
    group_id = ""

    if token_response.status_code == 200:
        access_token = token_response.json()['access_token']
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        groups_url = f"{os.getenv('KEYCLOAK_URL')}/admin/realms/{os.getenv('REALM')}/groups"
        keycloak_response = requests.get(groups_url, headers=headers)

        if keycloak_response.status_code == 200:
            data = keycloak_response.json()
            for group in data:
                if group["name"] == group_name:
                    group_id = group["id"]
        else:
            logger.info(f"Failed to retrieve groups. Status code: {keycloak_response.status_code}")
    else:
        logger.info(f"Failed to obtain access token. Status code: {token_response.status_code}")

    return group_id

def create_keycloak_group(group_name:str, address:str,user_id:str)->Response:
    """
    Creates a Keycloak group and adds a user to it.

    Args:
        group_name(str): The name of the group to be created.
        address(str): The address of the group to be created.
        user_id(str): The ID of the user to be added to the group.

    Returns:
        Response: A Response object containing the result of the creation.

    """
    token_response = get_admin_token()
    response = Response()

    if token_response.status_code == 200:
        access_token = token_response.json()['access_token']
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        #create group
        groups_url = f"{os.getenv('KEYCLOAK_URL')}/admin/realms/{os.getenv('REALM')}/groups"
        group_data = {
            "name": group_name,
            "attributes": {
                "address": [address]
            }
        }
        keycloak_response = requests.post(groups_url, headers=headers, json=group_data)

        if keycloak_response.status_code == 201:
            logger.info(f"Group '{group_name}' has been added.")
            group_id = get_groupid_by_name(group_name)
            add_user_to_group_response = add_user_to_group(user_id, group_id)
            if add_user_to_group_response.status_code == 200:
                response = Response({'message': f"Group '{group_name}' has been added."})
                return response
            else:
                response = Response({'message': f"Failed to add user with ID {user_id} to group with ID {group_id}. Status code: {add_user_to_group_response.status_code}"}, status=add_user_to_group_response.status_code)
                return response
        else:
            logger.info(f"Failed to add group '{group_name}'. Status code: {keycloak_response.status_code}")
            response = Response({'message': f"Failed to create group '{group_name}"}, status=500)
            response.status_code = keycloak_response.status_code
            return response
    else:
        logger.info(f"Failed to obtain access token. Status code: {token_response.status_code}")
        response = Response({'message': f"Failed to obtain access token. Status code: {token_response.status_code}"}, status=500)
        return response

def delete_keycloak_group(group_id:str) -> Response:
    """
    Deletes a Keycloak group. When using, make sure the user has the required permissions.
    
    Args:
        group_id(str): The ID of the group to be deleted.

    Returns:
        Response: A Response object containing the result of the deletion.
        """
    token_response = get_admin_token()
    response = Response()

    if token_response.status_code == 200:
        access_token = token_response.json()['access_token']
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        group_url = f"{os.getenv('KEYCLOAK_URL')}/admin/realms/{os.getenv('REALM')}/groups/{group_id}"
        keycloak_response = requests.delete(group_url, headers=headers)

        if keycloak_response.status_code == 204:
            logger.info(f"Group with ID {group_id} has been deleted.")
            response = Response({'message': f"Group with ID {group_id} has been deleted."})
        else:
            logger.info(f"Failed to delete group with ID {group_id}. Status code: {keycloak_response.status_code}")
            response = Response({'message': f"Failed to delete group with ID {group_id}. Status code: {keycloak_response.status_code}"})
    else:
        logger.info(f"Failed to obtain access token. Status code: {token_response.status_code}")
        response = Response({'message': f"Failed to obtain access token. Status code: {token_response.status_code}"})

    return response

def get_user_id(user_access_token: str) -> str:
    """
    Retrieves the ID of a user by the user access token.

    Args:
        user_access_token(id): The access token of the user.
    
    Returns:
        user_id(str): The ID of the user.
    """
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {user_access_token}'
    }

    userinfo_url = f"{os.getenv('KEYCLOAK_URL')}/realms/{os.getenv('REALM')}/protocol/openid-connect/userinfo"    
    try:
        keycloak_response = requests.get(userinfo_url, headers=headers)
    except Exception as e:
        logger.error("Error occurred while retrieving user info from Keycloak: " + str(e))
        raise e
    

    try:        
        user_id = keycloak_response.json().get("user_id")

    except Exception as e:
        logger.error("Error occurred while parsing JSON response: " + str(e))
        raise e
    
    if user_id is not None:
        return user_id
    else:
        raise ValueError("User ID not in response. Check Keycloak configuration.")

def get_user_groups_by_user_id(user_id:str) -> list[str]:
    """
    Retrieves the groups of a user by the user ID.
    
    Args:
        user_id: The ID of the user.
        
    Returns:
        list[str]: The groups of the user.
    """
    token_response = get_admin_token()
    groups = []

    if token_response.status_code == 200:
        access_token = token_response.json()['access_token']
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        groups_url = f"{os.getenv('KEYCLOAK_URL')}/admin/realms/{os.getenv('REALM')}/users/{user_id}/groups"
        keycloak_response = requests.get(groups_url, headers=headers)

        if keycloak_response.status_code == 200:
            data = keycloak_response.json()
            for group in data:
                groups.append(group["id"])
        else:
            logger.info(f"Failed to retrieve groups. Status code: {keycloak_response.status_code}")
    else:
        logger.info(f"Failed to obtain access token. Status code: {token_response.status_code}")

    return groups

def get_user_groups(user_access_token:str) -> list[str]:
    """
    Function to retrieve the groups of a user.
    
    Args:
        user_access_token: The access token of the user.
        
    Returns:
        list[str]: The groups of the user.
    """
    user_id = get_user_id(user_access_token)
    return get_user_groups_by_user_id(user_id)


def get_user_roles(user_access_token:str)->list[str]:
    """
    Function to retrieve the roles of a user.
    
    Args:
        user_access_token: The access token of the user.
        
    Returns:
        list[str]: The roles of the user.
    """
    userinfo_url = f"{os.getenv('KEYCLOAK_URL')}/realms/{os.getenv('REALM')}/protocol/openid-connect/userinfo"
    headers = {
        "Authorization": f"Bearer {user_access_token}",
        "Content-Type": "application/json"
    }
    userinfo_response = requests.get(userinfo_url, headers=headers)
    if userinfo_response.status_code == 200:
        userinfo = userinfo_response.json()
        roles = userinfo.get("realm_access", {}).get("roles", [])
        if roles == []:
            logger.info("No roles found in user info.")
        return roles
    else:
        logger.info(f"Failed to retrieve user info. Status code: {userinfo_response.status_code}")
        return []
from rest_framework import serializers

class KeycloakGroupSerializer(serializers.Serializer):
    """
    Serializer for the KeycloakGroup model.

    This serializer is responsible for converting KeycloakGroup objects to JSON format and vice versa.

    Attributes:
        id (str): The id of the KeycloakGroup.
        name (str): The name of the KeycloakGroup.
    """
    id = serializers.CharField()
    name = serializers.CharField()
from rest_framework import serializers

from ..models.ovo_hunter_model import OvoHunterModel

class OvoHunterSerializer(serializers.ModelSerializer):

    class Meta:
        model = OvoHunterModel
        fields = "__all__"
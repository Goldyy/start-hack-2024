import logging
import random

from rest_framework import viewsets

from ..models.ovo_hunter_model import OvoHunterModel
from ..serializers.ovo_hunter_serializer import OvoHunterSerializer

logger = logging.getLogger(__name__)

class OvoHunterViewset(viewsets.ModelViewSet):

    def perform_create(self, serializer):      
        logger.info("Adding OVO-Hunter.")  
        serializer.validated_data['is_impressed_by'] = "Moritz"        
        serializer.validated_data['nickname'] = random.choice(["CakeLover", "BananaLover", "AppleLover"])      
        serializer.save()            

    def perform_update(self, serializer):        
        logger.info("Updating OVO-Hunter.")
        serializer.validated_data['is_impressed_by'] = "Moritz"        
        serializer.validated_data['nickname'] = random.choice(["CakeLover", "BananaLover", "AppleLover"])      
        serializer.save()        

    def perform_destroy(self, instance):        
        logger.info("Removing OVO-Hunter.")        
        instance.delete()
        

    queryset = OvoHunterModel.objects.all()
    serializer_class = OvoHunterSerializer
    http_method_names = ["get", "post", "put", "delete"]
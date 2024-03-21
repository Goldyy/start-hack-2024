from django.shortcuts import render
from rest_framework import views, status, viewsets
from rest_framework.generics import RetrieveAPIView
from .services import StreamProcessorThread, StreamProcessManager
from rest_framework.response import Response
from .serializers import DeviceLocationSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import DeviceLocation
from rest_framework.decorators import action
from drf_yasg import openapi
import logging

logger = logging.getLogger(__name__)


class DeviceLocationManagerApiView(views.APIView):
    """
    This endpoint is responsible for managing the stream processor thread.

    Before the applications listens to the stream of data from the Cisco Firehose API, the stream processor thread
    must be started by making a request to the POST endpoint.
    To stop the stream processor thread, make a request to the DELETE endpoint.
    """


    def post(self, request):
        """
        This endpoint starts the stream processor thread. The thread must be startet before retrieval of location data. \n

        The stream processor thread listens to the datastream of the Cisco Firehose API and stores the latest
        location of the devices in the database. The location data is extracted from events with the type 'DEVICE_LOCATION_UPDATE'.
        """
        logger.trace("Starting stream processor thread")

        manager = StreamProcessManager()
        manager.set_stream_processor()
        stream_processor = manager.get_stream_processor()
        stream_processor.start()

        return Response({"message": "Stream processor started successfully."}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        """
        This endpoint stops the stream processor thread. \n

        After stopping the thread, the application will no longer listen to the datastream of the Cisco Firehose API and won't update
        the location data in the database.
        """
        logger.trace("Stopping stream processor thread")

        manager = StreamProcessManager()
        stream_processor = manager.get_stream_processor()
        if stream_processor:
            stream_processor.stop()
            return Response({"message": "Stream processor stopped successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Stream processor is not running."}, status=status.HTTP_400_BAD_REQUEST)
        
class DeviceLocationRetrieveView(RetrieveAPIView):
    """
    This enpoint delivers the location data of a device with the given MAC address.
    """
    queryset = DeviceLocation.objects.all()
    serializer_class = DeviceLocationSerializer
    lookup_field = "mac_address"

class DeviceLocationViewSet(viewsets.ModelViewSet):
    """
    This enpoint delivers the location data of all devices or a single device with the given id.
    """
    queryset = DeviceLocation.objects.all()
    serializer_class = DeviceLocationSerializer
    http_method_names = ["get"]
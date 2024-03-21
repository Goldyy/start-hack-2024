import threading
import requests
import json
import os
from apps.location.models import DeviceLocation
import logging
import requests
import socket
logger = logging.getLogger(__name__)



class StreamProcessorThread(threading.Thread):
    """
    This class is responsible for processing the stream of data from the Cisco Firehose API.

    Attributes:
        api_endpoint (str): The endpoint of the Cisco Firehose API.
        api_key (str): The API key to authenticate with the Cisco Firehose API.
        _stop_event (threading.Event): A threading event to signal the thread to stop.
        daemon (bool): A boolean to set the thread as a daemon thread.
        event_type (str): The type of event to process from the Cisco Firehose API.
    """

    def __init__(self):
        logger.trace("Initializing StreamProcessor object")
        threading.Thread.__init__(self)
        self.api_endpoint = os.getenv("CISCO_FIREHOSE_API_ENDPOINT")
        self.api_key = os.getenv("CISCO_API_KEY")
        self._stop_event = threading.Event()
        self.daemon = True  # Daemonize the thread so it exits when the main thread exits
        self.event_type="DEVICE_LOCATION_UPDATE"

    def _get_ip_address_workaround(self):
        """
        Workaround to get the IP address of the host machine.
        This is copied from the initial template of the STARTHACK CISCO project.

        Args:
            None
        
        Returns:
            None
        """

        # work around to get IP address on hosts with non resolvable hostnames
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IP_ADRRESS = s.getsockname()[0]
        s.close()
        url = 'http://' + str(IP_ADRRESS) + '/update/'

    def stop(self):
        """
        Set the stop event to stop the thread.
        
        Args:
            None
            
        Returns:
            None"""
        self._stop_event.set()

    def stopped(self):
        """
        Check if the stop event is set.
        
        Args:
            None
        
        Returns:
            bool: True if the stop event is set, False otherwise."""
        return self._stop_event.is_set()

    def run(self):
        """
        Processes the stream of data from the Cisco Firehose API and stores the latest DeviceLocation in the database.
        
        The data from the Firehose API stream is read in a new thread. Whenever a new event of the type DEVICE_LOCATION_UPDATE is found,
        the datapoints are extracted and stored in the database.

        The database is updated with the latest DeviceLocation for each device.

        Args:
            None

        Returns:
            None
        """

        self._get_ip_address_workaround()
        try:
            s = requests.Session()
            s.headers = {'X-API-Key': self.api_key}
            with s.get(self.api_endpoint, stream=True) as response:
                for line in response.iter_lines():
                    logger.trace("Reading line from stream.")
                    if line:
                        if self.stopped():
                            logger.trace("Stopping Stream Thread.")
                            s.close()
                            break

                        event = json.loads(line.decode('utf-8'))
                        event_type = event.get('eventType')
                        event_update = event.get('deviceLocationUpdate')
                        if event_type == self.event_type:   
                            logger.debug(f"Found Event with type {self.event_type}")
                            mac_address = event_update.get('device').get('macAddress')
                            ipv4_address = event_update.get('ipv4')
                            last_seen = event_update.get('lastSeen')
                            confidence_factor = event_update.get('confidenceFactor')
                            x_pos = event_update.get('xPos')
                            y_pos = event_update.get('yPos')

                            if mac_address and ipv4_address and last_seen and confidence_factor and x_pos and y_pos:
                                logger.debug(f"Creating or updating DeviceLocation with MAC address {mac_address}")
                                DeviceLocation.create_or_update(mac_address, ipv4_address, confidence_factor, x_pos, y_pos)
                                logger.debug(f"DeviceLocation with MAC address {mac_address} created or updated.")

        except Exception as e:
            print("Error in stream processing:", e)


from django.db import models

class DeviceLocation(models.Model):
    """
    This class is responsible for storing the location of a device represented by a DeviceLocation object.

    Attributes:
        mac_address (str): The MAC address of the device.
        ipv4_address (str): The IPv4 address of the device.
        confidence_factor (float): The confidence factor of the location of the device.
        x_pos (str): The x position of the device.
        y_pos (str): The y position of the device.
        created_at (datetime): The date and time the DeviceLocation was created.
        last_updated (datetime): The date and time the DeviceLocation was last updated.
    
    """

    mac_address = models.CharField(max_length=250, null=True, blank=True, unique=True)
    ipv4_address = models.CharField(max_length=250, null=True, blank=True)
    confidence_factor = models.FloatField()
    x_pos = models.CharField()
    y_pos = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def create_or_update(mac_address, ipv4_address, confidence_factor, x_pos, y_pos):
        """
        Creates or updates a DeviceLocation object. If the DeviceLocation object with the given mac_address exists, it is updated.
        Otherwise, a new DeviceLocation object is created.

        Args:
            mac_address (str): The MAC address of the device.
            ipv4_address (str): The IPv4 address of the device.
            confidence_factor (float): The confidence factor of the location of the device.
            x_pos (str): The x position of the device.
            y_pos (str): The y position of the device.

        Returns:
            None
        """
        try:
            result = DeviceLocation.objects.get(mac_address=mac_address)
            result.confidence_factor = confidence_factor
            result.x_pos = x_pos
            result.y_pos = y_pos
            result.save()
        except Exception as e:
            device_location = DeviceLocation(
                mac_address=mac_address,
                ipv4_address=ipv4_address,
                confidence_factor=confidence_factor,
                x_pos=x_pos,
                y_pos=y_pos
            )
            device_location.save()

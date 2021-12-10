from django.db import models


class DeviceType(models.Model):
    name = models.CharField(max_length=100)
    mask = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Device(models.Model):
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.serial_number

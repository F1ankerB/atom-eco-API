from django.db import models

class WasteType(models.Model):
    WASTE_CHOICES = (
        ('bio', 'Bio waste'),
        ('glass', 'Glass'),
        ('plastic', 'Plastic'),
    )
    name = models.CharField(max_length=50, choices=WASTE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Organization(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

from math import radians, sin, cos, sqrt, atan2
class Storage(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def distance_to_organization(self, organization_id):
        organization = Organization.objects.get(id=organization_id)
        return self.haversine_distance(self.latitude, self.longitude, organization.latitude, organization.longitude)

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        # Радиус Земли в километрах
        R = 6371.0

        # Преобразование градусов в радианы
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

    capacity = models.IntegerField()

    waste_types = models.ManyToManyField(WasteType, through='StorageCapacity')

    def __str__(self):
        return self.name

    def available_capacity(self, waste_type):

        storage_capacity = self.storagecapacity_set.filter(waste_type=waste_type).first()
        if storage_capacity:
            return storage_capacity.remaining_capacity
        return 0

class StorageCapacity(models.Model):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    waste_type = models.ForeignKey(WasteType, on_delete=models.CASCADE)
    max_capacity = models.IntegerField()
    current_capacity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.storage.name} - {self.waste_type.name}"

    @property
    def remaining_capacity(self):
        return self.max_capacity - self.current_capacity

    def add_waste(self, amount):
        if self.current_capacity + amount > self.max_capacity:
            raise ValueError("Exceeded maximum capacity for this waste type")
        self.current_capacity += amount
        self.save()

class WasteTransfer(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    waste_type = models.ForeignKey(WasteType, on_delete=models.CASCADE)
    amount = models.IntegerField()
    transfer_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        storage_capacity = StorageCapacity.objects.filter(storage=self.storage, waste_type=self.waste_type).first()
        if not storage_capacity:
            raise ValueError("This storage does not accept this type of waste")
        storage_capacity.add_waste(self.amount)
        super().save(*args, **kwargs)

import uuid

from django.db import models

class POI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    opening_hours = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'poi'

    def __str__(self):
        return self.name

class POIPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poi = models.ForeignKey(POI, related_name="photos",on_delete=models.CASCADE)
    photo_url = models.CharField(max_length=5000)
    size = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'poi_photo'

    def __str__(self):
        return self.photo_url
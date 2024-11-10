import uuid

from django.db import models

from poi.models import POI
from user.models import User


class Itinerary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries', db_column='user_id')
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()

    class Meta:
        db_table = 'itinerary'

    def __str__(self):
        return self.name

class Day(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    itinerary_id = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='days', db_column='itinerary_id')
    number_day = models.IntegerField()

    class Meta:
        db_table = 'day'

    def __str__(self):
        return self

class ItineraryPOI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    day_id = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='itineraryPOIS', db_column='day_id')
    destination_id = models.ForeignKey(POI, on_delete=models.CASCADE, related_name='itineraryPOIS', db_column='destination_id')
    order = models.IntegerField()
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()

    class Meta:
        db_table = 'itinerary_poi'

    def __str__(self):
        return self


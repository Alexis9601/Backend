from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from itinerary.services.itinerary_services import get_itineraries


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_today_itineraries(request):
    return get_itineraries(request.user)
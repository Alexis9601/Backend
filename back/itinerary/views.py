from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from itinerary.services.itinerary_services import get_itineraries, generate, save, get_by_day_id, get_all_by_user


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_today_itineraries(request):
    return get_itineraries(request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_itineraries(request):
    return generate(request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_itinerary(request):
    return save(request)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_day(request, id):
    return get_by_day_id(id)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_itineraries(request):
    return get_all_by_user(request.user)
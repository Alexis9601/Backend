from django.utils import timezone
from rest_framework.response import Response

from itinerary.models import Itinerary, ItineraryPOI


def get_itineraries(user):
    today = timezone.now().date()

    # Filtrar los ItineraryPOI que tengan arrival_time y departure_time dentro del día actual
    # y que pertenezcan a itinerarios del usuario autenticado
    today_pois = ItineraryPOI.objects.filter(
        day_id__itinerary_id__user_id=user,
        arrival_time__date=today,
        departure_time__date=today
    )

    # Crear un diccionario para agrupar los ItineraryPOI por itinerario
    itineraries = {}
    for poi in today_pois:
        itinerary = poi.day_id.itinerary_id
        if itinerary.id not in itineraries:
            itineraries[itinerary.id] = {
                'id': itinerary.id,
                'name': itinerary.name,
                'created_at': itinerary.created_at,
                'user_id': itinerary.user_id.id,
                'arrival_time': None,  # Se establecerá más adelante
                'departure_time': None,  # Se establecerá más adelante
                'pois': []
            }
        itineraries[itinerary.id]['pois'].append({
            'id': poi.id,
            'order': poi.order,
            'arrival_time': poi.arrival_time.strftime('%d/%m/%Y %I:%M %p'),
            'departure_time': poi.departure_time.strftime('%d/%m/%Y %I:%M %p'),
            'destination_id': poi.destination_id.id
        })

    # Establecer arrival_time y departure_time generales
    for itinerary in itineraries.values():
        pois = itinerary['pois']
        if pois:
            # Ordenar los POIs por el campo 'order'
            pois_sorted = sorted(pois, key=lambda x: x['order'])
            # El arrival_time general es el arrival_time del primer POI
            itinerary['arrival_time'] = pois_sorted[0]['arrival_time']
            # El departure_time general es el departure_time del último POI
            itinerary['departure_time'] = pois_sorted[-1]['departure_time']

    # Convertir el diccionario a una lista para devolverla como respuesta
    return Response(list(itineraries.values()))

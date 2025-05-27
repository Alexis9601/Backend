from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework.response import Response
from django.utils.timezone import make_aware

from itinerary.models import Itinerary, ItineraryPOI, Day
from poi.models import POI, POIPhoto
import random

def get_day_from_model(day):
    return {
        "id": day.id,
        "number": day.number_day,
        "itinerary_pois": [],
    }

def get_itinerary_pois(poi, itinerary_poi):
    photos = POIPhoto.objects.filter(poi=poi).values_list('photo_url', flat=True)
    return {
        "id": poi.id,
        "name": poi.name,
        "latitude": poi.latitude,
        "longitude": poi.longitude,
        "address": poi.address,
        'order': itinerary_poi.order,
        'arrival_time': itinerary_poi.arrival_time.strftime('%d/%m/%Y %I:%M %p'),
        'departure_time': itinerary_poi.departure_time.strftime('%d/%m/%Y %I:%M %p'),
        "category": poi.category,
        "rating": poi.rating,
        "photos": photos,
        "description": poi.description,
    }

def get_itinerary_from_model(itinerary):
    return {
        "id": itinerary.id,
        "name": itinerary.name,
        "arrival_time": itinerary.arrival_time.strftime('%d/%m/%Y'),
        "departure_time": itinerary.departure_time.strftime('%d/%m/%Y'),
        "days": [],
    }

def get_itineraries(user):
    today = timezone.now().date()

    today_pois = ItineraryPOI.objects.filter(
        day_id__itinerary_id__user_id=user,
        arrival_time__date=today,
        departure_time__date=today
    )

    itineraries = {}
    for poi in today_pois:
        itinerary = poi.day_id.itinerary_id
        if itinerary.id not in itineraries:
            itineraries[itinerary.id] = {
                'id': itinerary.id,
                'name': itinerary.name,
                'created_at': itinerary.created_at,
                'user_id': itinerary.user_id.id,
                'arrival_time': None,
                'departure_time': None,
                'day_id': poi.day_id.id,
                'pois': []
            }
        itineraries[itinerary.id]['pois'].append({
            'id': poi.id,
            'order': poi.order,
            'arrival_time': poi.arrival_time.strftime('%d/%m/%Y %I:%M %p'),
            'departure_time': poi.departure_time.strftime('%d/%m/%Y %I:%M %p'),
            'destination_id': poi.destination_id.id
        })

    for itinerary in itineraries.values():
        pois = itinerary['pois']
        if pois:
            pois_sorted = sorted(pois, key=lambda x: x['order'])
            itinerary['arrival_time'] = pois_sorted[0]['arrival_time']
            itinerary['departure_time'] = pois_sorted[-1]['departure_time']

    return Response(list(itineraries.values()))


def generate(request):
    start_date_str = request.data.get('startDate')
    start_time_str = request.data.get('startTime')
    end_date_str = request.data.get('endDate')
    end_time_str = request.data.get('endTime')
    latitude = request.data.get('location', {}).get('latitude')
    longitude = request.data.get('location', {}).get('longitude')
    categories = request.data.get('categories', [])

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        end_time = datetime.strptime(end_time_str, "%H:%M").time()

        num_days = (end_date - start_date).days + 1

        itineraries = []

        for i in range(5):
            itinerary = {
                "name": f"Itinerario {i + 1}",
                "startDate": start_date_str,
                "endDate": end_date_str,
                "days": [],
            }

            for day in range(num_days):
                current_day_date = start_date + timedelta(days=day)
                day_start_datetime = datetime.combine(current_day_date, start_time)
                day_end_datetime = datetime.combine(current_day_date, end_time)
                total_hours = (day_end_datetime - day_start_datetime).seconds // 3600

                pois = list(POI.objects.all())
                random.shuffle(pois)
                num_selected = random.randint(3, 5)
                selected_pois = pois[:num_selected]

                day_destinations = []
                current_time = day_start_datetime

                for poi in selected_pois:
                    arrival_time = current_time
                    departure_time = arrival_time + timedelta(hours=1)
                    current_time = departure_time
                    photos = POIPhoto.objects.filter(poi=poi).values_list('photo_url', flat=True)

                    day_destinations.append({
                        "id": poi.id,
                        "name": poi.name,
                        "latitude": poi.latitude,
                        "longitude": poi.longitude,
                        "address": poi.address,
                        "arrival_time": arrival_time.strftime("%d/%m/%Y %I:%M %p"),
                        "departure_time": departure_time.strftime("%d/%m/%Y %I:%M %p"),
                        "category": poi.category,
                        "rating": poi.rating,
                        "photos": photos,
                        "description": poi.description,
                    })

                itinerary["days"].append({
                    "number": day + 1,
                    "itinerary_pois": day_destinations
                })

            itineraries.append(itinerary)

        return Response({
            "success": True,
            "itineraries": itineraries,
            "error": None
        }, status=200)

    except Exception as e:
        return Response({
            "success": False,
            "itineraries": None,
            "error": "No se pudieron generar los itinerarios"
        }, status=400)

def save(request):
    try:
        itinerary = Itinerary.objects.create(
            name=request.data["name"],
            arrival_time=make_aware(datetime.strptime(request.data["startDate"], "%Y-%m-%d")),
            departure_time=make_aware(datetime.strptime(request.data["endDate"], "%Y-%m-%d")),
            user_id = request.user
        )

        json_itinerary = get_itinerary_from_model(itinerary)

        days = []

        for day_data in request.data["days"]:
            day = Day.objects.create(
                itinerary_id=itinerary,
                number_day=day_data["number"]
            )

            json_day = get_day_from_model(day)

            for index, destination_data in enumerate(day_data["itinerary_pois"], start=1):
                poi = POI.objects.get(id=destination_data["id"])
                itinerary_poi = ItineraryPOI.objects.create(
                    day_id=day,
                    destination_id=poi,
                    arrival_time=make_aware(datetime.strptime(destination_data["arrival_time"], "%d/%m/%Y %I:%M %p")),
                    departure_time=make_aware(datetime.strptime(destination_data["departure_time"], "%d/%m/%Y %I:%M %p")),
                    order=index
                )
                json_day["itinerary_pois"].append(get_itinerary_pois(poi, itinerary_poi))
            days.append(json_day)
        json_itinerary["days"] = days
        #print(json_itinerary)
        return Response({
            "success": True,
            "itinerary": json_itinerary,
            "error": None
        }, status=200)
    except Exception as e:
        print(e)
        return Response({
            "success": False,
            "itinerary": None,
            "error": "No se pudo guardar el itinerario"
        }, status=400)

def get_by_day_id(id):
    try:
        day = Day.objects.get(id=id)
        json_day = get_day_from_model(day)
        if day :
            itinerary_pois = list(ItineraryPOI.objects.filter(day_id=day))
            for itinerary_poi in itinerary_pois:
                poi = POI.objects.get(id = itinerary_poi.destination_id.id)
                json_day["itinerary_pois"].append(get_itinerary_pois(poi, itinerary_poi))
            return Response({
                "success": True,
                "day": json_day,
                "error": None
            }, status=200)
        else :
            return Response({
                "success": False,
                "day": None,
                "error": "No se encontro un día asociado al id enviado"
            }, status=400)

    except Exception as e:
        print(e)
        return Response({
            "success": False,
            "day": None,
            "error": "Ocurrio un error al obtener la información del día"
        }, status=400)

def get_all_by_user(user):
    try:
        json_itineraries = []
        itineraries = list(Itinerary.objects.filter(user_id=user))
        for itinerary in itineraries:
            json_itinerary = get_itinerary_from_model(itinerary)
            days = list(Day.objects.filter(itinerary_id=itinerary))
            for day in days:
                json_day = get_day_from_model(day)
                itinerary_pois = list(ItineraryPOI.objects.filter(day_id=day))
                for itinerary_poi in itinerary_pois:
                    poi = POI.objects.get(id=itinerary_poi.destination_id.id)
                    json_day["itinerary_pois"].append(get_itinerary_pois(poi, itinerary_poi))
                json_itinerary["days"].append(json_day)
            json_itineraries.append(json_itinerary)
        return Response({
            "success": True,
            "itineraries": json_itineraries,
            "error": None
        }, status=200)
    except Exception as e:
        print(e)
        return Response({
            "success": False,
            "itineraries": None,
            "error": "Ocurrio un error al obtener los itinerarios"
        }, status=400)

def delete_by_id(id):
    if not id:
        return Response({
            "success": False,
            "error": "El campo id es obligatorio."
        }, status=400)
    try:
        itinerary = Itinerary.objects.get(id=id)
    except Itinerary.DoesNotExist:
        return Response({
            "success": False,
            "message": "No se pudó obtener el itinerario."
        }, status=400)
    itinerary.delete()
    return Response({
            "success": True,
            "message": None
    }, status=200)

import hashlib

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

from user.models import User
from user.serializers import UserRegistrationSerializer, UserSerializer
import logging
logger = logging.getLogger(__name__)


def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user_data = {
            "id": user.id,
            "user_name": user.user_name,
            "email": user.email
        }
        return Response({
            'message': 'Usuario registrado exitosamente',
            'user': user_data
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({"errors": serializer.errors, "message": "Error en los datos proporcionados"}, status=status.HTTP_400_BAD_REQUEST)


def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        if user.status != "ACTIVE":
            return Response({'message': 'Usuario no activado'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        expires_in = (access_token['exp'] - timezone.now().timestamp())
        return Response({
            'access': str(access_token),
            'expires_in': int(expires_in)
        }, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

def basic_info(user):
    return Response({
        'id': user.id,
        'fullname': user.full_name,
        'name': user.user_name,
        'last_name': user.user_lastname,
        'photo': user.photo,
        'email': user.email,
        'birthdate': user.birthdate.strftime('%d/%m/%Y'),
    }, status=200)

def update_user(user, data):
    user_name = data.get('name', None)
    user_last_name = data.get('last_name', None)
    photo = data.get('photo', None)
    updated = False
    if user_name is not None:
        user.user_name = user_name
        updated = True
    if user_last_name is not None:
        user.user_lastname = user_last_name
        updated = True
    if photo is not None:
        user.photo = photo
        updated = True
    if updated:
        user.save()
        return Response({
            'message': 'Información de usuario actualizada con éxito',
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response({
        'message': 'No se logró actualizar la información del usuario.',
        'user': None
    }, status=status.HTTP_400_BAD_REQUEST)

def update_password(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            "success": False,
            "error": "No se pudo encontrar al usuario solicitado."
        }, status=400)
    user.password = password
    user.save()
    return Response({
        "success": True,
        "error": None
    }, status=200)

def get_string_hash(password):
    hash_obj = hashlib.sha256(password.encode())
    hash_hex = hash_obj.hexdigest()
    return hash_hex
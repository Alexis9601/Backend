import hashlib

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserRegistrationSerializer


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
            return Response({'messsage': 'Usuario no activado'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'messsage': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

def get_string_hash(password):
    hash_obj = hashlib.sha256(password.encode())
    hash_hex = hash_obj.hexdigest()
    return hash_hex
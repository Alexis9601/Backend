from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserRegistrationSerializer
from .services.otpServices import create_otp


@api_view(['POST'])
def user_registration(request):
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


@api_view(['POST'])
def generate_otp(request):
    user_id = request.data.get('user_id')
    result = create_otp(user_id)

    return Response({
        "message": result["message"]
    }, status=result["status"])
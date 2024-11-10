from datetime import timedelta

from django.utils import timezone
from rest_framework.response import Response
from user.models import User
import random
import string
from validation_code.models import ValidationCode
from emails.services.email_services import send_otp_email


def generate_otp(length=6):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_otp(user_id):
    if not user_id:
         return Response({
            "message": "El campo user_id es obligatorio."
         }, status=400)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({
            "message": "Usuario no encontrado."
        }, status=404)

    if user.status != 'PENDING':
        return Response({
            "message": "El usuario no puede generar un otp."
        }, status=400)

    otp_code = generate_otp()
    validation_code = ValidationCode.objects.filter(user_id=user.id).first()

    if validation_code:
        validation_code.code = otp_code
        validation_code.created_at = timezone.now()
        validation_code.save()
    else:
        validation_code = ValidationCode.objects.create(user_id=user, code=otp_code)
        validation_code.save()

    mail_data = {
        "otp": otp_code,
        "user_name": user.user_name,
        "email": user.email
    }

    #send_otp_email(mail_data)
    return Response({
        "message": "OTP generado exitosamente."
    }, status=201)

def otp_validation(user_id, otp):
    if not user_id:
         return Response({
            "message": "El campo user_id es obligatorio."
         }, status=400)
    if not otp:
         return Response({
            "message": "El campo otp es obligatorio."
         }, status=400)
    validation_code = ValidationCode.objects.filter(user_id=user_id).first()
    if not validation_code:
        return Response({
            "message": "No existe un código asociado al usuario."
        }, status=400)
    time_since_created = timezone.now() - validation_code.created_at
    if time_since_created >= timedelta(minutes=5):
        validation_code.delete()
        return Response({
            "message": "El código ha expirado, por favor genere uno nuevo."
        }, status=400)
    if otp == validation_code.code:
        try:
            user = User.objects.get(id=user_id)
            user.status = 'ACTIVE'
            user.save()
            validation_code.delete()
            return Response({
                "message": "Usuario registrado correctamente."
            }, status=200)
        except User.DoesNotExist:
            return Response({
                "message": "Ocurrio un error al activar el usuario."
            }, status=500)
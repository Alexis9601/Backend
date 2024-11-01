from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from db.models import User, ValidationCode
import random
import string

def generate_otp(length=6):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_otp(user_id):
    if not user_id:
        return {
            "message": "El campo user_id es obligatorio.",
            "status": 400
        }

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return {
            "message": "Usuario no encontrado.",
            "status": 404
        }

    if user.status != 'PENDING':
        return {
            "message": "El usuario no puede generar un otp",
            "status": 400
        }

    otp_code = generate_otp()

    validation_code = ValidationCode.objects.create(user_id=user, code=otp_code)
    validation_code.save()

    mail_data = {
        "otp": otp_code,
        "user_name": user.user_name,
        "email": user.email
    }

    send_welcome_email(mail_data)

    return {
        "message": "OTP generado exitosamente.",
        "status": 201
    }

def send_welcome_email(mail_data):
    html_body = render_to_string("template.html", mail_data)
    email = EmailMultiAlternatives(
        subject='{otp} es tu código de AppName'.format(otp = mail_data["otp"]),
        body="",
        from_email='hello@trial-x2p03476qn7gzdrn.mlsender.net',
        to=[mail_data["email"]],
    )
    email.attach_alternative(html_body, "text/html")
    email.send()

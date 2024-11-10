from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.Serializer):
    user_name = serializers.CharField(
        max_length=255,
        error_messages={
            "required": "El nombre es obligatorio.",
            "blank": "El nombre no puede estar vacío."
        }
    )
    user_lastname = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True
    )
    birthdate = serializers.DateField(
        error_messages={
            "required": "La fecha de nacimiento es obligatoria.",
            "blank": "La fecha de nacimiento no puede estar vacía."
        }
    )
    password = serializers.CharField(
        write_only=True,
        error_messages={
            "required": "La contraseña es obligatoria.",
            "blank": "La contraseña no puede estar vacía."
        }
    )
    email = serializers.CharField(
        max_length=255,
        error_messages={
            "required": "El correo es obligatorio.",
            "blank": "El correo no puede estar vacío."
        }
    )
    photo = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True  # Este campo es opcional, por lo tanto, puede estar vacío si no se proporciona.
    )

    def validate_password(self, value):
        if not value.strip():
            raise serializers.ValidationError("La contraseña no puede estar vacía.")
        if len(value) < 6:
            raise serializers.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un usuario registrado con este correo electrónico.")
        return value

    def create(self, validated_data):
        user = User.objects.create(
            user_name=validated_data['user_name'],
            email=validated_data['email'],
            user_lastname=validated_data['user_lastname'],
            birthdate=validated_data['birthdate'],
            password=validated_data['password'],
            status='PENDING'
        )
        if 'photo' in validated_data:
            user.photo = validated_data['photo']
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_name', 'user_lastname', 'email', 'photo']
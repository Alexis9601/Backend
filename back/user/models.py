import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, user_name, user_lastname, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(user_name=user_name, user_lastname=user_lastname, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, user_lastname, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_name, user_lastname, email, password, **extra_fields)

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=255)
    user_lastname = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    photo = models.TextField(null=True, blank=True)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True, blank=True)  # Agrega este campo

    objects = UserManager()

    USERNAME_FIELD = 'email'  # El campo que se usará para autenticar
    REQUIRED_FIELDS = ['user_name', 'user_lastname']  # Campos requeridos para crear un superusuario

    @property
    def full_name(self):
        if self.user_lastname:
            return f"{self.user_name} {self.user_lastname}"
        return self.user_name

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email
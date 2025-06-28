# users/models.py

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class Pole(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    color = models.CharField(max_length=7, default="#000000")

    def __str__(self):
        return self.name
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L’utilisateur doit avoir une adresse e-mail")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modèle customisé pointant sur la table existante `users` en MySQL.
    """
    id          = models.AutoField(primary_key=True)
    username    = models.CharField(max_length=150, unique=True)
    email       = models.EmailField(max_length=254, unique=True)
    password    = models.CharField(max_length=128)
    is_staff    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    # Les deux nouveaux champs ajoutés en SQL :
    last_login  = models.DateTimeField(null=True)   # correspond à la colonne SQL
    is_superuser = models.BooleanField(default=False)
    pole = models.ForeignKey(
        'tickets.Pole',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = "users"

    objects = UserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'
        managed  = True   # Django ne recrée pas la table

    def __str__(self):
        return self.username

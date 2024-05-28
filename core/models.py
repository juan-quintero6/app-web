from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20)  # Puede ser 'conductor', 'cliente' o 'administrador'

class Conductor(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    # Otros campos específicos de un conductor

class Cliente(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    # Otros campos específicos de un cliente

class Administrador(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, primary_key=True)
    # Otros campos específicos de un administrador

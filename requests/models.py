from core.models import Cliente
from django.db import models

# Create your models here.


class Evento(models.Model):
    id_usuario = models.IntegerField()
    evento = models.CharField(max_length=20)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=150)
    estado = models.CharField(max_length=10, default='Abierto')
    seguimiento_creado = models.BooleanField(default=False)

    # pylint: disable=invalid-str-returned
    def __str__(self):
        return self.evento

class Seguimiento(models.Model):
    id_usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_seguimiento = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Seguimiento de {self.id_usuario} para {self.id_evento}'    

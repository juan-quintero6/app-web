from django.db import models

# Create your models here.


class Solicitud(models.Model):
    id_cliente = models.IntegerField()
    estado = models.CharField(max_length=10, default='En espera')

    nombre_producto = models.CharField(max_length=20)
    origen = models.CharField(max_length=150)
    destino = models.CharField(max_length=150)
    fecha_entrega = models.DateField()
    descripcion = models.CharField(max_length=150)
    receptor = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10)
    telefono = models.IntegerField(max_length=10)

    # pylint: disable=invalid-str-returned
    def __str__(self):
        return self.nombre_producto

class Envio(models.Model):
    id_conductor = models.IntegerField(default=1)
    calificacion = models.IntegerField()
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='envios')

    # pylint: disable=invalid-str-returned
    def __str__(self):
        return str(self.calificacion)

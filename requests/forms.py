from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Solicitud
import datetime

class SolicitudForm(forms.ModelForm):
    # Campo personalizado para la fecha de entrega con widget de tipo 'date'
    fecha_entrega = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Solicitud
        fields = ['nombre_producto', 'origen', 'destino',
                  'fecha_entrega', 'descripcion', 'receptor',
                  'cedula', 'telefono']
        labels = {
            'origen': 'Punto de origen:',
            'destino': 'Punto de destino:',
            'fecha_entrega': 'Fecha de entrega:',
            'receptor': 'Nombre de la persona que recibe:',
            'cedula': 'Número de cédula:',
            'telefono': 'Teléfono de contacto:',
        }

    def clean_fecha_entrega(self):
        # Validación personalizada para la fecha de entrega
        fecha_entrega = self.cleaned_data.get('fecha_entrega')
        
        # Obtener la zona horaria deseada (UTC-5:00)
        tz = timezone.get_fixed_timezone(-300)  # UTC-5:00

        # Obtener la fecha y hora actual en la zona horaria deseada
        now = datetime.datetime.now(tz)

        # Comparar con la fecha de entrega ingresada
        if fecha_entrega < now.date():
            raise ValidationError(
                "La fecha de entrega debe ser a partir de hoy en la zona horaria UTC/GMT -5:00.")

        return fecha_entrega

    def clean_nombre_producto(self):
        # Validación para el nombre del producto
        nombre_producto = self.cleaned_data.get('nombre_producto')
        if not nombre_producto.isalpha():
            raise ValidationError("El nombre del producto solo debe contener letras.")
        return nombre_producto

    def clean_receptor(self):
        # Validación para el nombre del receptor
        receptor = self.cleaned_data.get('receptor')
        if not receptor.replace(' ', '').isalpha():
            raise ValidationError("El nombre del receptor solo debe contener letras.")
        return receptor

    def clean_cedula(self):
        # Validación para la cédula
        cedula = self.cleaned_data.get('cedula')
        if not cedula.isdigit():
            raise ValidationError("La cédula debe contener solo números.")
        return cedula

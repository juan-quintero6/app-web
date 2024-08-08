from django import forms
from django.core.exceptions import ValidationError
from .models import Evento
import re
from datetime import date

class EventoForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Evento
        fields = ['evento', 'fecha', 'descripcion']
        labels = {
            'evento': 'Evento:',
            'fecha': 'Fecha de evento:',
            'descripcion': 'Descripción:',
        }
        widgets = {
            'evento': forms.TextInput(attrs={'placeholder': 'EVXXXX-MXX-AXX-S'})
        }

    def clean_evento(self):
        evento = self.cleaned_data.get('evento')
        if not re.match(r'^EV\d{4}-M\d{2}-A\d{2}-S$', evento):
            raise ValidationError("El evento debe tener el formato EVXXXX-MXX-AXX-S")
        
        # Obtén el evento en edición
        instance = self.instance
        if instance.pk:
            # Excluye el evento actual de la validación
            if Evento.objects.filter(evento=evento).exclude(pk=instance.pk).exists(): # pylint: disable=no-member
                raise ValidationError("Este evento ya existe.")
        else:
            # Para nuevos eventos, verifica que no exista
            if Evento.objects.filter(evento=evento).exists(): # pylint: disable=no-member
                raise ValidationError("Este evento ya existe.")
        
        return evento

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha > date.today():
            raise ValidationError("La fecha de evento no puede ser posterior a la fecha actual.")
        return fecha

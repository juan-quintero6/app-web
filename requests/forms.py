from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Evento
import datetime

class EventoForm(forms.ModelForm):
    # Campo personalizado para la fecha de entrega con widget de tipo 'date'
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Evento
        fields = ['evento', 'fecha', 'descripcion']
        labels = {
            'evento': 'Evento:',
            'fecha': 'Fecha de evento:',
            'descripcion': 'Descripción::',
        }

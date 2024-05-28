from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    ROLE_CHOICES = [
        ('administrador', 'Administrador'),
        ('conductor', 'Conductor'),
        ('cliente', 'Cliente'),
    ]
    rol = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, required=True, label='Rol')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'rol', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado')
        return email

class TokenForm(forms.Form):
    token = forms.CharField(label='Token', max_length=20)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
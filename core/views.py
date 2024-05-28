from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth import authenticate
from .forms import CustomUserCreationForm, TokenForm, UserProfileForm
from .models import Perfil, Administrador, Conductor, Cliente
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User


@login_required
def home(request):
    user = request.user
    if hasattr(user, 'perfil'):
        if user.perfil.tipo == 'cliente':
            return redirect(reverse('create_solicitud'))
        elif user.perfil.tipo == 'administrador':
            return redirect('/admin/')
        elif user.perfil.tipo == 'conductor':
            return redirect(reverse('c_read_solicitud'))
    else:
        return render(request, 'core/home.html')

@login_required
def products(request):
    return render(request, 'core/products.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(request.POST)
        if user_creation_form.is_valid():
            with transaction.atomic():
                user = user_creation_form.save(commit=False)
                tipo_usuario = user_creation_form.cleaned_data['rol']
                if tipo_usuario == 'administrador':
                    request.session['admin_user_data'] = user_creation_form.cleaned_data
                    return redirect('token_verification')
                else:
                    user.save()
                    perfil = Perfil.objects.create(usuario=user, tipo=tipo_usuario) # pylint: disable=no-member
                    if tipo_usuario == 'conductor':
                        Conductor.objects.create(perfil=perfil) # pylint: disable=no-member
                    elif tipo_usuario == 'cliente':
                        Cliente.objects.create(perfil=perfil) # pylint: disable=no-member
                    login(request, user)
                    return redirect('home')
    else:
        user_creation_form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': user_creation_form})

@login_required
def token_verification(request):
    if request.method == 'POST':
        token_form = TokenForm(request.POST)
        if token_form.is_valid():
            token = token_form.cleaned_data['token']
            if token == 'GT-AD-XXXX':
                user_data = request.session.get('admin_user_data')
                if user_data:
                    with transaction.atomic():
                        user = User.objects.create_user(
                            username=user_data['username'],
                            first_name=user_data['first_name'],
                            last_name=user_data['last_name'],
                            email=user_data['email'],
                            password=user_data['password1']
                        )
                        perfil = Perfil.objects.create(usuario=user, tipo='administrador') # pylint: disable=no-member
                        Administrador.objects.create(perfil=perfil) # pylint: disable=no-member
                        user.is_staff = True
                        user.is_superuser = True
                        user.save()
                        login(request, user)
                        return redirect('/admin/')
            else:
                return render(request, 'registration/token_verification.html', {'form': token_form, 'error': 'Token incorrecto'})
    else:
        token_form = TokenForm()
    return render(request, 'registration/token_verification.html', {'form': token_form})


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'core/edit_profile.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from django.http import HttpResponse
from .models import Solicitud, Envio
from .forms import SolicitudForm
from core.models import Perfil

@login_required
def home(request):
    """
    Renderiza la página de inicio.
    """
    return render(request, 'home.html')

@login_required
def c_home(request):
    """
    Renderiza la página principal del cliente.
    """
    return render(request, 'c-home.html')

@login_required
def c_read_solicitud(request):
    """
    Renderiza la lista de solicitudes de carga para un cliente.
    """
    solicitudes = Solicitud.objects.filter(estado='En espera')  # pylint: disable=no-member
    return render(request, 'c_read_solicitud.html', {'solicitudes': solicitudes})

@login_required
def c_read_envio(request):
    """
    Renderiza la lista de envíos para un conductor.
    """
    perfil = Perfil.objects.get(usuario=request.user)  # pylint: disable=no-member

    user_id = perfil.usuario.id
    envios = Envio.objects.filter(id_conductor=user_id)  # pylint: disable=no-member
    return render(request, 'c_read_envio.html', {'envios': envios})

@login_required
def detail_solicitud(request, pk):
    """
    Renderiza los detalles de una solicitud de carga.
    """
    solicitud = get_object_or_404(Solicitud, pk=pk)
    return render(request, 'c_detail_solicitud.html', {'solicitud': solicitud})

@login_required
def accept_solicitud(request, pk):
    """
    Procesa la aceptación de una solicitud de carga.
    """
    solicitud = get_object_or_404(Solicitud, pk=pk)
    
    if request.method == 'POST':
        solicitud.estado = 'En proceso'
        solicitud.save()

        # Crear un nuevo objeto Envio
        envio = Envio(  # pylint: disable=no-member
            id_conductor=request.user.id,  # Asigna el id del usuario autenticado como id_conductor
            calificacion=0,  # Inicializa con una calificación predeterminada
            solicitud=solicitud
        )
        envio.save()

        origin = solicitud.origen
        destination = solicitud.destino
        id_solicitud = solicitud.id
        return redirect(reverse('envio') + f'?origin={origin}&destination={destination}&id={id_solicitud}')
    
    return render(request, 'c_read_solicitud.html', {'solicitud': solicitud})

@login_required
def start_journey(request, pk):
    """
    Marca una solicitud de carga como en marcha.
    """
    solicitud = get_object_or_404(Solicitud, pk=pk)
    
    if request.method == 'POST':
        solicitud.estado = 'En marcha'
        solicitud.save()
        return HttpResponse(status=204)  # No Content response
    
    return HttpResponse(status=405)  # Method Not Allowed response

@login_required
def delivered(request, pk):
    """
    Marca una solicitud de carga como entregada.
    """
    solicitud = get_object_or_404(Solicitud, pk=pk)
    
    if request.method == 'POST':
        solicitud.estado = 'Entregado'
        solicitud.save()
        return redirect(c_read_envio)  # No Content response
    
    return HttpResponse(status=405)  # Method Not Allowed response

@login_required
def envio(request):
    """
    Renderiza la página de envío.
    """
    return render(request, 'index.html')

@login_required
def create_solicitud(request):
    """
    Crea una nueva solicitud de carga.
    """
    perfil = Perfil.objects.get(usuario=request.user)  # pylint: disable=no-member

    user_id = perfil.usuario.id

    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)  # No guardar aún en la base de datos
            solicitud.id_cliente = user_id  # Asignar la ID del usuario autenticado al campo id_cliente
            solicitud.save() 
            return redirect('read_solicitud')
    else:
        form = SolicitudForm()
    return render(request, 'create_solicitud.html', {'form': form})

@login_required
def read_solicitud(request):
    """
    Renderiza la lista de solicitudes de carga del cliente.
    """
    perfil = Perfil.objects.get(usuario=request.user)  # pylint: disable=no-member

    user_id = perfil.usuario.id
    solicitudes = Solicitud.objects.filter(id_cliente=user_id, estado='En espera')  # pylint: disable=no-member
    return render(request, 'read_solicitud.html', {'solicitudes': solicitudes})

@login_required
def edit_solicitud_view(request, pk):
    """
    Renderiza el formulario para editar una solicitud de carga.
    """
    solicitud = get_object_or_404(Solicitud, pk=pk)
    if request.method == 'POST':
        form = SolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            return redirect('read_solicitud')
    else:
        form = SolicitudForm(instance=solicitud)
    return render(request, 'edit_solicitud.html', {'form': form})

@login_required
def delete_solicitud_view(request, pk):
    """
    Renderiza la confirmación para eliminar una solicitud de carga.
    """
    solicitud = get_object_or_404(Solicitud, pk=pk)
    if request.method == 'POST':
        solicitud.delete()
        return redirect('read_solicitud')
    return render(request, 'delete_solicitud.html', {'solicitud': solicitud})

@login_required
def read_envio(request):
    """
    Renderiza la lista de envíos del cliente.
    """
    client_id = request.user.id
    solicitudes = Solicitud.objects.filter(id_cliente=client_id).exclude(estado='En espera')  # pylint: disable=no-member
    return render(request, 'read_envio.html', {'solicitudes': solicitudes})

@login_required
def logout_view(request):
    """
    Realiza el logout del usuario.
    """
    logout(request)
    return redirect('register')

@login_required
def edit_user(request):
    """
    Redirige a la página de edición de perfil.
    """
    return redirect(reverse('edit_profile'))

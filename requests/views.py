from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from django.http import HttpResponse
from .models import Evento, Seguimiento
from .forms import EventoForm
from django.contrib import messages
from core.models import Perfil, Cliente
from django.utils import timezone

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
def start_journey(request, pk):
    """
    Marca una solicitud de carga como en marcha.
    """
    solicitud = get_object_or_404(Evento, pk=pk)
    
    if request.method == 'POST':
        solicitud.estado = 'En marcha'
        solicitud.save()
        return HttpResponse(status=204)  # No Content response
    
    return HttpResponse(status=405)  # Method Not Allowed response

@login_required
def create_evento(request):
    """
    Crea una nueva solicitud de carga.
    """
    perfil = Perfil.objects.get(usuario=request.user)  # pylint: disable=no-member

    user_id = perfil.usuario.id

    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)  # No guardar aún en la base de datos
            evento.id_usuario = user_id  # Asignar la ID del usuario autenticado al campo id_cliente
            evento.save() 
            return redirect('read_evento')
    else:
        form = EventoForm()
    return render(request, 'create_evento.html', {'form': form})

@login_required
def read_evento(request):
    """
    Renderiza la lista de eventos del usuario
    """
    perfil = Perfil.objects.get(usuario=request.user)  # pylint: disable=no-member

    user_id = perfil.usuario.id
    eventos = Evento.objects.filter(id_usuario=user_id, estado='Abierto')  # pylint: disable=no-member
    return render(request, 'read_evento.html', {'eventos': eventos})

@login_required
def create_seguimiento(request, id_usuario, id_evento):
    cliente = get_object_or_404(Cliente, pk=id_usuario)
    evento = get_object_or_404(Evento, pk=id_evento, id_usuario=id_usuario)
    cantidad_inicial = 1

    if not evento.seguimiento_creado:
        Seguimiento.objects.create( # pylint: disable=no-member
            id_usuario=cliente,
            id_evento=evento,
            cantidad=cantidad_inicial,
            fecha_seguimiento=timezone.now()
        )
        evento.seguimiento_creado = True
        evento.save()

    return redirect('read_seguimiento')

@login_required
def read_seguimiento(request):
    """
    Renderiza la lista de seguimientos de eventos abiertos del cliente.
    """
    perfil = Perfil.objects.get(usuario=request.user)  # pylint: disable=no-member
    user_id = perfil.usuario.id

    # Filtrar seguimientos donde el evento asociado esté 'Abierto'
    seguimientos = Seguimiento.objects.filter(id_usuario=user_id, id_evento__estado='Abierto')  # pylint: disable=no-member
    return render(request, 'read_seguimiento.html', {'seguimientos': seguimientos})


@login_required
def gestionar_seguimiento(request, id_seguimiento): 
    seguimiento = get_object_or_404(Seguimiento, id=id_seguimiento) 
    return render(request, 'gestionar_seguimiento.html', {'seguimiento': seguimiento})

@login_required
def actualizar_seguimiento(request, id_seguimiento):
    seguimiento = get_object_or_404(Seguimiento, id=id_seguimiento)

    # Comprobar si la fecha de seguimiento es hoy
    if seguimiento.fecha_seguimiento == timezone.now().date():
        # Si la fecha de seguimiento ya es hoy, mostrar mensaje de aviso
        messages.warning(request, 'Ya has realizado un seguimiento el día de hoy.')
        return redirect('gestionar_seguimiento', id_seguimiento=id_seguimiento)

    # Si la fecha de seguimiento no es hoy, proceder con la actualización
    seguimiento.cantidad += 1
    seguimiento.fecha_seguimiento = timezone.now()
    seguimiento.save()
    messages.success(request, 'Seguimiento actualizado con éxito.')
    return redirect('gestionar_seguimiento', id_seguimiento=id_seguimiento)

@login_required
def cerrar_evento(request, id_evento):
    """
    Cierra el evento y actualiza su estado.
    """
    evento = get_object_or_404(Evento, id=id_evento)
    seguimientos = Seguimiento.objects.filter(id_evento=evento) # pylint: disable=no-member

    # Verifica si hay seguimientos asociados y cierra el evento
    if seguimientos.exists():
        evento.estado = 'Cerrado'
        evento.save()
        return redirect('read_evento')
    else:
        return HttpResponse("No se puede cerrar el evento porque no tiene seguimientos asociados.", status=400)

@login_required
def edit_evento_view(request, pk):
    """
    Renderiza el formulario para editar una solicitud de carga.
    """
    solicitud = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            return redirect('read_evento')
    else:
        form = EventoForm(instance=solicitud)
    return render(request, 'edit_evento.html', {'form': form})

@login_required
def delete_evento_view(request, pk):
    """
    Renderiza la confirmación para eliminar una solicitud de carga.
    """
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        evento.delete()
        return redirect('read_evento')
    return render(request, 'delete_evento.html', {'evento': evento})

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

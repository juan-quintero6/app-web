from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('c', views.c_home, name='c-home'),
    path('crear-evento/', views.create_evento, name='create_evento'),
    path('mis-eventos/', views.read_evento, name='read_evento'),
    path('editar-evento/<int:pk>/',
         views.edit_evento_view, name='edit_evento'),
    path('eliminar-evento/<int:pk>/',
         views.delete_evento_view, name='delete_evento'),
    path('read_evento/', views.read_evento, name='read_evento'),
    path('create_seguimiento/<int:id_usuario>/<int:id_evento>/', views.create_seguimiento, name='create_seguimiento'),
    path('read_seguimiento/', views.read_seguimiento, name='read_seguimiento'),
    path('gestionar_seguimiento/<int:id_seguimiento>/', views.gestionar_seguimiento, name='gestionar_seguimiento'),
    path('actualizar_seguimiento/<int:id_seguimiento>/', views.actualizar_seguimiento, name='actualizar_seguimiento'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_user/', views.edit_user, name='edit_user'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('c', views.c_home, name='c-home'),
    path('c_read_solicitud/', views.c_read_solicitud, name='c_read_solicitud'),
    path('c_read_envio/', views.c_read_envio, name='c_read_envio'),
    path('detail_solicitud/<int:pk>/', views.detail_solicitud, name='c_detail_solicitud'),
    path('accept/<int:pk>/', views.accept_solicitud, name='accept_solicitud'),
    path('start/<int:pk>/', views.start_journey, name='start_journey'),
    path('finish/<int:pk>/', views.delivered, name='delivered'),
    path('envio/', views.envio, name='envio'),
    path('crear-solicitud/', views.create_solicitud, name='create_solicitud'),
    path('mis-solicitudes/', views.read_solicitud, name='read_solicitud'),
    path('editar-solicitud/<int:pk>/',
         views.edit_solicitud_view, name='edit_solicitud'),
    path('eliminar-solicitud/<int:pk>/',
         views.delete_solicitud_view, name='delete_solicitud'),
    path('read_solicitud/', views.read_solicitud, name='read_solicitud'),
    path('read_envio/', views.read_envio, name='read_envio'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_user/', views.edit_user, name='edit_user'),
]

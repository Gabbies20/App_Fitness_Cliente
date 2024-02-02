from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('lista_ejercicios',views.ejercicios_lista_api,name='lista'),
    path('ejercicios/busqueda',views.ejercicio_busqueda_simple,name='ejercicio_busqueda_simple'),
    path('ejercicios/busqueda_avanzada',views.ejercicio_busqueda_avanzada,name='ejercicio_busqueda_avanzada'),
    path('lista_entrenamientos',views.entrenamientos_lista_api,name='lista_entrenamientos'),
]

from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    #EJERCICIOS:
    path('lista_ejercicios',views.ejercicios_lista_api,name='lista'),
    path('ejercicios/busqueda',views.ejercicio_busqueda_simple,name='ejercicio_busqueda_simple'),
    path('ejercicios/busqueda_avanzada',views.ejercicio_busqueda_avanzada,name='ejercicio_busqueda_avanzada'),
    #ENTRENAMIENTOS:
    path('lista_entrenamientos',views.entrenamientos_lista_api,name='lista_entrenamientos'),
    path('entrenamientos/busqueda',views.entrenamiento_busqueda_simple,name='entrenamiento_busqueda_simple'),
]

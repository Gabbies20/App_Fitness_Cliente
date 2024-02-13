from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    #EJERCICIOS:
    path('lista_ejercicios',views.ejercicios_lista_api,name='lista'),
    path('ejercicios/busqueda',views.ejercicio_busqueda_simple,name='ejercicio_busqueda_simple'),
    path('ejercicios/busqueda_avanzada',views.ejercicio_busqueda_avanzada,name='ejercicio_busqueda_avanzada'),
    path('crear',views.views.ejercicio_crear,name='ejercicio_crear')
    #ENTRENAMIENTOS:
    path('lista_entrenamientos',views.entrenamientos_lista_api,name='lista_entrenamientos'),
    path('entrenamientos/busqueda',views.entrenamiento_busqueda_simple,name='entrenamiento_busqueda_simple'),
    path('entrenamientos/busqueda_avanzada',views.entrenamiento_busqueda_avanzada,name='entrenamiento_busqueda_avanzada'),
    #COMENTARIOS:
    path('lista_comentarios',views.comentarios_lista_api,name='lista_comentarios'),
    path('comentarios/busqueda',views.comentario_busqueda_simple,name='comentario_busqueda_simple'),
    path('comentarios/busqueda_avanzada',views.comentario_busqueda_avanzada,name='comentario_busqueda_avanzada'),
]

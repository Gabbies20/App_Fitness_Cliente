from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    #EJERCICIOS:
    path('lista_ejercicios',views.ejercicios_lista_api,name='lista'),
    path('ejercicios/busqueda',views.ejercicio_busqueda_simple,name='ejercicio_busqueda_simple'),
    path('ejercicios/busqueda_avanzada',views.ejercicio_busqueda_avanzada,name='ejercicio_busqueda_avanzada'),
    path('ejercicios/crear',views.ejercicio_crear,name='ejercicio_crear'),
    path('ejercicio/<int:ejercicio_id>',views.ejercicio_obtener,name='ejercicio_mostrar'),
    path('ejercicio/editar/<int:ejercicio_id>',views.ejercicio_editar,name='ejercicio_editar'),
    path('ejercicio/editar/nombre/<int:ejercicio_id>',views.ejercicio_editar_nombre,name='ejercicio_editar_nombre'),
    path('ejercicio/eliminar/<int:ejercicio_id>',views.ejercicio_eliminar,name='ejercicio_eliminar'),
    #ENTRENAMIENTOS:
    path('lista_entrenamientos',views.entrenamientos_lista_api,name='lista_entrenamientos'),
    path('entrenamientos/busqueda',views.entrenamiento_busqueda_simple,name='entrenamiento_busqueda_simple'),
    path('entrenamientos/busqueda_avanzada',views.entrenamiento_busqueda_avanzada,name='entrenamiento_busqueda_avanzada'),
    path('entrenamientos/crear',views.entrenamiento_crear,name='entrenamiento_crear'),
    path('entrenamiento/<int:entrenamiento_id>',views.entrenamiento_obtener,name='entrenamiento_mostrar'),
    path('entrenamiento/editar/<int:entrenamiento_id>',views.entrenamiento_editar,name='entrenamiento_editar'),
    path('entrenamiento/editar/descripcion/<int:entrenamiento_id>',views.entrenamiento_editar_descripcion,name='entrenamiento_editar_nombre'),
    path('entrenamiento/eliminar/<int:entrenamiento_id>',views.entrenamiento_eliminar,name='entrenamiento_eliminar'),
    #COMENTARIOS:
    path('lista_comentarios',views.comentarios_lista_api,name='lista_comentarios'),
    path('comentarios/busqueda',views.comentario_busqueda_simple,name='comentario_busqueda_simple'),
    path('comentarios/busqueda_avanzada',views.comentario_busqueda_avanzada,name='comentario_busqueda_avanzada'),
    path('comentarios/crear',views.comentario_crear,name='comentario_crear'),
    path('comentario/<int:comentario_id>',views.comentario_obtener,name='comentario_mostrar'),
    path('comentario/editar/<int:comentario_id>',views.comentario_editar,name='comentario_editar'),
    path('comentario/editar/nombre/<int:comentario_id>',views.comentario_editar_nombre,name='comentario_editar_nombre'),
    path('comentario/eliminar/<int:comentario_id>',views.comentario_eliminar,name='comentario_eliminar'),
    
    #REGISTRO - LOGIN Y LOGOUT:
    path('registrar', views.registrar_usuario, name='registrar_usuario'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]

from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('lista_ejercicios',views.ejercicios_lista_api,name='lista')
]

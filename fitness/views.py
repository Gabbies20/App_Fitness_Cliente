from django.shortcuts import render,redirect,HttpResponse
from .forms import *
# Create your views here.
#Vistas API


import requests
#import environ
import os
from pathlib import Path


#.ENV:
#BASE_DIR = Path(__file__).resolve().parent.parent
#env = environ.Env()
#environ.Env.read_env(os.path.join(BASE_DIR, '.env'))



# Create your views here.
def index(request):
  
    return render(request, 'fitness/index2.html')

def crear_cabecera():
    return {'Authorization': 'Bearer CLSw8ZZaTtNb7oKIAb9ttWgN8EZlPE'}


def ejercicios_lista_api(request):
    #Obtenemos los ejercicios.
    headers = {'Authorization':'Bearer CLSw8ZZaTtNb7oKIAb9ttWgN8EZlPE'}
    response = requests.get('http://127.0.0.1:8000/api/v1/ejercicios',headers=headers)
    #Transformamos la respuesta de json.
    ejercicios = response.json()
    return render(request, 'fitness/lista_api.html',{'ejercicios_mostrar':ejercicios})

#Debi acceder a la URL y no me muestra nada, de forma interna me esta dando un error 400. Ahora al crear 'headers' con su respectivo token me muestra ya los libros.
def ejercicio_busqueda_simple(request):
    formulario = BusquedaEjercicioForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/ejercicios/busqueda_simple',
            headers = headers,
            params = formulario.cleaned_data
        )
        ejercicios = response.json()
        return render(request,'fitness/ejercicio/lista_mejorada.html',{'ejercicios_mostrar':ejercicios})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
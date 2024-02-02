from django.shortcuts import render,redirect,HttpResponse
from .forms import *
# Create your views here.
#Vistas API


import requests
from requests.exceptions import HTTPError
#import environ
import os
from pathlib import Path


#.ENV:
#BASE_DIR = Path(__file__).resolve().parent.parent
#environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
#env = environ.Env()



# Create your views here.
def index(request):
  
    return render(request, 'fitness/index2.html')

def crear_cabecera():
    return {'Authorization': 'DXsWFMq1D1ZiXm45oo6RSaqx82mnLH'}


"""
VISTAS DE EJERCICIO:
"""
def ejercicios_lista_api(request):
    #Obtenemos los ejercicios.
    headers = {'Authorization':'Bearer KympJJ2dEtlQ3FVqTI9rpMV7m4rTFW'}
    response = requests.get('http://127.0.0.1:8000/api/v1/ejercicios',headers=headers)
    #response = requests.get('http://gabrielapinzon.pythonanywhere.com/api/v1/ejercicios',headers=headers)
    #Transformamos la respuesta de json.
    ejercicios = response.json()
    return render(request, 'fitness/lista_api.html',{'ejercicios_mostrar':ejercicios})

#Debi acceder a la URL y no me muestra nada, de forma interna me esta dando un error 400. Ahora al crear 'headers' con su respectivo token me muestra ya los ejercicios.
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

def ejercicio_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaEjercicioAvanzadaForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                'http://127.0.0.1:8000/api/v1/ejercicios/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                ejercicios = response.json()
                return render(request, 'fitness/ejercicio/lista_mejorada.html',
                              {"ejercicios_mostrar":ejercicios})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(http_err == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'fitness/ejercicio/busqueda_avanzada.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaEjercicioAvanzadaForm(None)
    return render(request, 'fitness/ejercicio/busqueda_avanzada.html',{"formulario":formulario})
    
    
"""
   VISTAS ENTRENAMIENTOS: 
"""
def entrenamientos_lista_api(request):
    #Obtenemos todos los entrenamientos.
    response = request.get('http://127.0.0.1:8000/api/v1/entrenamientos')
    #Transformamos la respuesta e JSON y lo cargo en un objeto python.
    # La función json() es una conveniencia proporcionada por la biblioteca requests para convertir el contenido JSON de la respuesta en un objeto Python.
    entrenamientos = response.json()
    return render(request,'fitness/lista_api_entrenamientos.html',{'entrenamientos_mostrar':entrenamientos})
    











#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)
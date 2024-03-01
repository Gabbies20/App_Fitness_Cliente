from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from .helper import helper
import json
from requests.exceptions import HTTPError
import requests
import environ
import os
from pathlib import Path


#ENV:
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()


# Create your views here.
def index(request):
    return render(request, 'fitness/index2.html')

def crear_cabecera():
    return {
        'Authorization': 'Bearer '+env("TOKEN_ADMIN"),
        "Content-Type": "application/json"
    }


"""
VISTAS DE EJERCICIO:
"""
def ejercicios_lista_api(request):
    #Obtenemos los ejercicios.
    #headers = {'Authorization':'Bearer sem6IlXzR1ER9DcjyLd0FOVuwRurdk'}
    headers = crear_cabecera()
    #Debi acceder a la URL y no me muestra nada, de forma interna me esta dando un error 400. Ahora al crear 'headers' con su respectivo token me muestra ya los ejercicios.
    response = requests.get('http://127.0.0.1:8000/api/v1/ejercicios',headers=headers)
    #response = requests.get('http://gabrielapinzon.pythonanywhere.com/api/v1/ejercicios',headers=headers)
    #Transformamos la respuesta de json.
    ejercicios = response.json()
    return render(request, 'fitness/lista_api.html',{'ejercicios_mostrar':ejercicios})


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
        return render(request,'fitness/ejercicio/lista_busqueda.html',{'ejercicios_mostrar':ejercicios})
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
    
    
def ejercicio_crear(request):
    if(request.method == 'POST'):
        try:
            formulario = EjercicioForm(request.POST)
            headers = {
                'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                'Content-Type':'application/json'
            }   
            datos = formulario.data.copy()
            datos['usuarios'] =request.POST.getlist('usuarios')
        
            response = requests.post(
                'http://127.0.0.1:8000/api/v1/ejercicios/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect('lista')
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la peticiiiiiiiiiiión: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'fitness/ejercicio/create.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    else:
         formulario = EjercicioForm(None)
    return render(request, 'fitness/ejercicio/create.html',{"formulario":formulario})

def ejercicio_obtener(request, ejercicio_id):
    print(ejercicio_id)
    ejercicio = helper.obtener_ejercicio(ejercicio_id)
    return render(request, 'fitness/ejercicio/ejercicio_mostrar.html',{'ejercicio':ejercicio})

def ejercicio_editar(request,ejercicio_id):
    
    datosFormulario = None
    
    if request.method == 'POST':
        datosFormulario = request.POST
        
    ejercicio = helper.obtener_ejercicio(ejercicio_id)
    formulario = EjercicioForm(datosFormulario,
                                initial ={
                                    'nombre': ejercicio['nombre'],
                                    'descripcion': ejercicio['descripcion'],
                                    'tipo_ejercicio': ejercicio['tipo_ejercicio'],
                                    'usuarios': [usuario['id'] for usuario in ejercicio['usuarios']]

                                })
    
    """
    if (request.method == "POST"):
            try:
                formulario = EjercicioForm(request.POST)
                headers = {
                    'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                    'Content-Type':'application/json'
                }   
                datos = formulario.data.copy()
                datos['usuarios'] =request.POST.getlist('usuarios')
            
                response = requests.put(
                    'http://127.0.0.1:8000/api/v1/ejercicios/editar/'+str(ejercicio_id),
                    headers=headers,
                    data=json.dumps(datos)
                )
                if(response.status_code == requests.codes.ok):
                    messages.success(request, 'Se ha editado correctamente el ejercicio seleccionado.')
                    return redirect('lista')
                else:
                    print(response.status_code)
                    response.raise_for_status()
            except HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if(response.status_code == 400):
                    errores = response.json()
                    for error in errores:
                        formulario.add_error(error,errores[error])
                    return render(request, 
                                'fitness/ejercicio/create.html',
                                {"formulario":formulario})
                else:
                    return mi_error_500(request)
            except Exception as err:
                print(f'Ocurrió un error: {err}')
                return mi_error_500(request)
    return render(request, 'fitness/ejercicio/actualizar.html',{"formulario":formulario})"""
    
    if (request.method == "POST"):
            try:
                formulario = EjercicioForm(request.POST)
                headers = {
                    'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                    'Content-Type':'application/json'
                }
                datos = request.POST.copy()

                response = requests.put(
                    'http://127.0.0.1:8000/api/v1/ejercicios/editar/'+ str(ejercicio_id), headers=headers, data=json.dumps(datos)
                )
                if(response.status_code == requests.codes.ok):
                    # Redirecciono al listado completo de recintos
                    return redirect("lista")
                else:
                    print(response.status_code)
                    response.raise_for_status()
            except HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if(response.status_code == 400):
                    errores = response.json()
                    for error in errores:
                        formulario.add_error(error,errores[error])
                    return render(request, 
                            'fitness/ejercicio/actualizar.html',
                            {"formulario":formulario,"ejercicio":ejercicio})
                else:
                    return mi_error_500(request)
            except Exception as err:
                print(f'Ocurrió un error: {err}')
                return mi_error_500(request)
    return render(request, 'fitness/ejercicio/actualizar.html',{"formulario":formulario,"ejercicio":ejercicio})


def ejercicio_editar_nombre(request,ejercicio_id):
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    ejercicio = helper.obtener_ejercicio(ejercicio_id)
    formulario = EjercicioActualizarNombreForm(datosFormulario,
            initial={
                'nombre': ejercicio['nombre'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = EjercicioActualizarNombreForm(request.POST)
            headers = {
                    'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                    'Content-Type':'application/json'
                }
            datos = request.POST.copy()
            response = requests.patch(
                'http://127.0.0.1:8000/api/v1/ejercicios/actualizar/nombre/'+str(ejercicio_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("ejercicio_mostrar",ejercicio_id=ejercicio_id)
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'fitness/ejercicio/actualizar_nombre.html',
                            {"formulario":formulario,"ejercicio":ejercicio})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'fitness/ejercicio/actualizar_nombre.html',{"formulario":formulario,"ejercicio":ejercicio})


def ejercicio_eliminar(request,ejercicio_id):
    try:
        headers = {
                    'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                    'Content-Type':'application/json'
                }
        response = requests.delete(
            'http://127.0.0.1:8000/api/v1/ejercicios/eliminar/'+str(ejercicio_id),
            headers=headers,
        )
        if(response.status_code == requests.codes.ok):
            return redirect("lista")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('lista')






"""
   VISTAS ENTRENAMIENTOS: 
"""
def entrenamientos_lista_api(request):
    #Obtenemos todos los entrenamientos.
    headers = {'Authorization':'Bearer KympJJ2dEtlQ3FVqTI9rpMV7m4rTFW'}
    response = requests.get('http://127.0.0.1:8000/api/v1/entrenamientos',headers=headers)
    #Transformamos la respuesta e JSON y lo cargo en un objeto python.
    # La función json() es una conveniencia proporcionada por la biblioteca requests para convertir el contenido JSON de la respuesta en un objeto Python.
    entrenamientos = response.json()
    return render(request,'fitness/lista_api_entrenamientos.html',{'entrenamientos_mostrar':entrenamientos})
    


def entrenamiento_busqueda_simple(request):
    formulario = BusquedaEntrenamientoForm(request.GET)
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get('http://127.0.0.1:8000/api/v1/entrenamientos/busqueda_simple',
        headers=headers,
        params=formulario.data
        )
        entrenamientos = response.json()
        return render(request,'fitness/entrenamiento/lista_busqueda.html',{'entrenamientos_mostrar':entrenamientos})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
"""
def entrenamiento_busqueda_simple(request):
    formulario = BusquedaEntrenamientoForm(request.GET)
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get('http://127.0.0.1:8000/api/v1/entrenamientos/busqueda_simple',
                                headers=headers,
                                params={'textoBusqueda': formulario.data.get('textoBusqueda')}
                                )
        entrenamientos = response.json()
        
        # Obtener los nombres de los ejercicios asociados a cada entrenamiento
        for entrenamiento in entrenamientos:
            ejercicios = []
            if 'ejercicios' in entrenamiento:  # Verificar si 'ejercicios' está presente en el diccionario
                for entrenamiento_ejercicio in entrenamiento['ejercicios']:
                    if 'ejercicio' in entrenamiento_ejercicio:  # Verificar si 'ejercicio' está presente en el diccionario
                        ejercicios.append(entrenamiento_ejercicio['ejercicio']['nombre'])
                entrenamiento['nombres_ejercicios'] = ejercicios
        
        return render(request, 'fitness/entrenamiento/lista_busqueda.html', {'entrenamientos_mostrar': entrenamientos})
    if "HTTP_REFERER" in request.META:
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
"""
    
    
    
def entrenamiento_busqueda_avanzada(request):
    if len(request.GET)>0:
        formulario = BusquedaEntrenamientoAvanzadaForm(request.GET)
        try:
            headers = crear_cabecera()
            response = requests.get(
                'http://127.0.0.1:8000/api/v1/entrenamientos/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )
            if(response.status_code==requests.codes.ok):
                entrenamientos = response.json()
                return render(request, 'fitness/entrenamiento/lista_mejorada.html', {'entrenamientos_mostrar': entrenamientos})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error HTTP: {http_err}')
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'fitness/entrenamiento/busqueda_avanzada.html',{'formulario':formulario,'errores':errores})
            else:
                raise mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            raise mi_error_500("No se pudo completar la solicitud")
    else:
        formulario=BusquedaEntrenamientoAvanzadaForm(None)
        return render(request, 'fitness/entrenamiento/busqueda_avanzada.html', {'formulario': formulario})
    
    

"""COMENTARIOS"""
def comentarios_lista_api(request):
    headers = {'Authorization':'Bearer KympJJ2dEtlQ3FVqTI9rpMV7m4rTFW'}
    response = requests.get('http://127.0.0.1:8000/api/v1/comentarios',headers=headers)
    comentarios = response.json()
    return render(request, 'fitness/comentario/lista_comentarios.html',{'comentarios_mostrar':comentarios})



def comentario_busqueda_simple(request):
    formulario = BusquedaComentarioForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/comentarios/busqueda_simple',
            headers = headers,
            params = formulario.cleaned_data
        )
        comentarios = response.json()
        return render(request,'fitness/comentario/lista_busqueda.html',{'comentarios_mostrar':comentarios})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
def comentario_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaComentarioAvanzadoForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                'http://127.0.0.1:8000/api/v1/comentario/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                ejercicios = response.json()
                return render(request, 'fitness/comentario/lista_mejorada.html',
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
                            'fitness/comentario/busqueda_avanzada.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaComentarioAvanzadoForm(None)
    return render(request, 'fitness/comentario/busqueda_avanzada.html',{"formulario":formulario})
    
    
    
    
def comentario_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaComentarioAvanzadoForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                'http://127.0.0.1:8000/api/v1/comentario/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                ejercicios = response.json()
                return render(request, 'fitness/comentario/lista_mejorada.html',
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
                            'fitness/comentario/busqueda_avanzada.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaComentarioAvanzadoForm(None)
    return render(request, 'fitness/comentario/busqueda_avanzada.html',{"formulario":formulario})
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def registrar_usuario(request):
    pass


def login(request):
    pass


def logout(request):
    pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)
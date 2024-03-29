import errno
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
from django.http import Http404, JsonResponse
from datetime import datetime


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
    #headers = {'Authorization':'Bearer sem6IlXzR1ER9DcjyLd0FOVuwRurdk'}
    headers = crear_cabecera()
    response = requests.get('https://gabrielapinzon.pythonanywhere.com/api/v1/ejercicios',headers=headers)
    #response = requests.get('http://gabrielapinzon.pythonanywhere.com/api/v1/ejercicios',headers=headers)
    ejercicios = response.json()
    return render(request, 'fitness/lista_api.html',{'ejercicios_mostrar':ejercicios})


def ejercicio_busqueda_simple(request):
    formulario = BusquedaEjercicioForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get(
            'https://gabrielapinzon.pythonanywhere.com/api/v1/ejercicios/busqueda_simple',
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
                'https://gabrielapinzon.pythonanywhere.com/api/v1/ejercicios/busqueda_avanzada',
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
            
            #Crea una instancia del formulario EjercicioForm utilizando los datos proporcionados en request.POST. Esto captura todos los campos del formulario y los convierte en un objeto de formulario Django.
            formulario = EjercicioForm(request.POST)
            headers = {
                'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                'Content-Type':'application/json'
            }   
            
            
            #Copia los datos del formulario en un nuevo diccionario llamado datos. Además, se obtiene la lista de usuarios seleccionados en el formulario y se agrega al diccionario datos.
            datos = formulario.data.copy()
            datos['usuarios'] =request.POST.getlist('usuarios')
            datos['grupos_musculares'] = request.POST.getlist('grupos_musculares')
            
        
            response = requests.post(
                'https://gabrielapinzon.pythonanywhere.com/api/v1/ejercicios/crear',
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
    #Obtenemos el ejercicio por la API.
    ejercicio = helper.obtener_ejercicio(ejercicio_id)
    #Especificamos cada uno de los valores que vamos a rellenar.
    formulario = EjercicioForm(datosFormulario,
                                initial ={
                                    'nombre': ejercicio['nombre'],
                                    'descripcion': ejercicio['descripcion'],
                                    'tipo_ejercicio': ejercicio['tipo_ejercicio'],
                                    'grupos_musculares': [grupo['id'] for grupo in ejercicio['grupos_musculares']],
                                    'usuarios': [usuario['usuario']['id'] for usuario in ejercicio['usuarios']]

                                })
    
    if (request.method == "POST"):
            try:
                formulario = EjercicioForm(request.POST)
                headers = {
                    'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                    'Content-Type':'application/json'
                }
                datos = request.POST.copy()

                response = requests.put(
                    'https://gabrielapinzon.pythonanywhere.com/api/v1/ejercicios/editar/'+ str(ejercicio_id), headers=headers, data=json.dumps(datos)
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
                'https://gabrielapinzon.pythonanywhere.com/api/v1/ejercicios/actualizar/nombre/'+str(ejercicio_id),
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
            'https://gabrielapinzon.pythonanywhere.com/api/v1/ejercicios/eliminar/'+str(ejercicio_id),
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
    headers = crear_cabecera()
    response = requests.get('https://gabrielapinzon.pythonanywhere.com/api/v1/entrenamientos',headers=headers)
    entrenamientos = response.json()
    return render(request,'fitness/lista_api_entrenamientos.html',{'entrenamientos_mostrar':entrenamientos})
    


def entrenamiento_busqueda_simple(request):
    formulario = BusquedaEntrenamientoForm(request.GET)
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get('https://gabrielapinzon.pythonanywhere.com/api/v1/entrenamientos/busqueda_simple',
        headers=headers,
        params=formulario.data
        )
        entrenamientos = response.json()
        return render(request,'fitness/entrenamiento/lista_busqueda.html',{'entrenamientos_mostrar':entrenamientos})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")

    
def entrenamiento_busqueda_avanzada(request):
    if len(request.GET)>0:
        formulario = BusquedaEntrenamientoAvanzadaForm(request.GET)
        try:
            headers = crear_cabecera()
            response = requests.get(
                'https://gabrielapinzon.pythonanywhere.com/api/v1/entrenamientos/busqueda_avanzada',
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

def entrenamiento_crear(request):
    
    if (request.method == "POST"):
        try:
            formulario = EntrenamientoForm(request.POST)
            headers =  {
                        'Authorization': 'Bearer '+env("TOKEN_CLIENTE"),
                        "Content-Type": "application/json" 
                    } 
            datos = formulario.data.copy()
            datos["ejercicios"] = request.POST.getlist("ejercicios")
            
            response = requests.post(
                'https://gabrielapinzon.pythonanywhere.com/api/v1/entrenamientos/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("lista_entrenamientos")
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
                            'fitness/entrenamiento/create.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
      
    else:
         formulario = EntrenamientoForm(None)
    return render(request, 'fitness/entrenamiento/create.html',{"formulario":formulario})

def entrenamiento_obtener(request, entrenamiento_id):
    entrenamiento = helper.obtener_entrenamiento(entrenamiento_id)
    return render(request, 'fitness/entrenamiento/entrenamiento_mostrar.html',{'entrenamiento':entrenamiento})


def entrenamiento_editar(request,entrenamiento_id):
    
    datosFormulario = None
    
    if request.method == 'POST':
        datosFormulario = request.POST
        
    entrenamiento = helper.obtener_entrenamiento(entrenamiento_id)
    formulario = EntrenamientoForm(datosFormulario,
                                initial ={
                                    'usuario':entrenamiento['usuario'],
                                    'nombre': entrenamiento['nombre'],
                                    'descripcion': entrenamiento['descripcion'],
                                    'duracion':entrenamiento['duracion'],
                                    'tipo':entrenamiento['tipo'],
                                    'ejercicios': [ejercicio['id'] for ejercicio in entrenamiento['ejercicios']]

                                })
    
    if (request.method == "POST"):
            try:
                formulario = EntrenamientoForm(request.POST)
                headers = {
                    'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                    'Content-Type':'application/json'
                }
                datos = request.POST.copy()
                datos["ejercicios"] = request.POST.getlist("ejercicios")

                response = requests.put(
                    'https://gabrielapinzon.pythonanywhere.com/api/v1/entrenamientos/editar/'+ str(entrenamiento_id), headers=headers, data=json.dumps(datos)
                )
                if(response.status_code == requests.codes.ok):
                    # Redirecciono al listado completo de recintos
                    return redirect("lista_entrenamientos")
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
                            'fitness/entrenamiento/actualizar.html',
                            {"formulario":formulario,"entrenamiento":entrenamiento})
                else:
                    return mi_error_500(request)
            except Exception as err:
                print(f'Ocurrió un error: {err}')
                return mi_error_500(request)
    return render(request, 'fitness/entrenamiento/actualizar.html',{"formulario":formulario,"entrenamiento":entrenamiento})

def entrenamiento_editar_descripcion(request,entrenamiento_id):
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    entrenamiento = helper.obtener_entrenamiento(entrenamiento_id)
    
    formulario = EntrenamientoActualizarNombreForm(datosFormulario,
            initial={
                'descripcion': entrenamiento['descripcion'],
            }
    
    )
    
    if (request.method == "POST"):
        try:
            formulario = EntrenamientoActualizarNombreForm(request.POST)
            headers = {
                    'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                    'Content-Type':'application/json'
                }
            datos = request.POST.copy()
            response = requests.patch(
                'https://gabrielapinzon.pythonanywhere.com/api/v1/entrenamientos/actualizar/descripcion/'+str(entrenamiento_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect('lista_entrenamientos')
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
                            'fitness/entrenamiento/actualizar_nombre.html',
                            {"formulario":formulario,"entrenamiento":entrenamiento})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'fitness/entrenamiento/actualizar_nombre.html',{"formulario":formulario,"entrenamiento":entrenamiento})

def entrenamiento_eliminar(request,entrenamiento_id):
    try:
        headers = {
                    'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                    'Content-Type':'application/json'
                }
        response = requests.delete(
            'https://gabrielapinzon.pythonanywhere.com/api/v1/entrenamientos/eliminar/'+str(entrenamiento_id),
            headers=headers,
        )
        if(response.status_code == requests.codes.ok):
            return redirect("lista_entrenamientos")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('lista_entrenamientos')



""" 
    VISTAS DE COMENTARIOS:
"""
def comentarios_lista_api(request):
    headers = crear_cabecera()
    response = requests.get('https://gabrielapinzon.pythonanywhere.com/api/v1/comentarios',headers=headers)
    comentarios = response.json()
    return render(request, 'fitness/comentario/lista_comentarios.html',{'comentarios_mostrar':comentarios})



def comentario_busqueda_simple(request):
    formulario = BusquedaComentarioForm(request.GET)
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get(
            'https://gabrielapinzon.pythonanywhere.com/api/v1/comentarios/busqueda_simple',
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
                'https://gabrielapinzon.pythonanywhere.com/api/v1/comentarios/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                comentarios = response.json()
                return render(request, 'fitness/comentario/busqueda_avanzada.html',
                              {"comentarios_mostrar":comentarios})
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
    
    
def comentario_crear(request):
    if (request.method == "POST"):
        try:
            #Aquí creo una instancia de LibroForm utilizando los datos proporcionados en request.POST. Esto captura todos los campos y los convierte en un objeto de formulario -django.
            formulario = ComentarioForm(request.POST)
            print("Datos del formulario:",formulario.data)
            
            #Se definen los encabezados HTTP que se utilizarán en la solicitud. Esto incluye el token de autorización (probablemente obtenido de una variable de entorno) y el tipo de contenido, que se establece en application/json.
            headers =  {
                        'Authorization': 'Bearer '+env("TOKEN_CLIENTE"),
                        "Content-Type": "application/json" 
                    } 
            
            #Se copian los datos del formulario en un nuevo diccionario llamado datos.Esto se hace para poder realizar manipulaciones en estos datos sin afectar el objeto del formulario original.
            datos = formulario.data.copy()
            
            #Se combinan los campos de fecha(año,mes y dia) en un solo campo y se convierte en cadena.
            datos["fecha"] = str(
                                            datetime.date(year=int(datos['fecha_year']),
                                                        month=int(datos['fecha_month']),
                                                        day=int(datos['fecha_day']))
                                             )
            # Obtener el ID del usuario seleccionado en el formulario
            usuario_id = datos.get('usuario')
            if usuario_id:
                datos['usuario'] = int(usuario_id)
            # Imprimir los datos que se enviarán en la solicitud POST
            print('los datos son', datos)

            
            
            #Se realiza una solicitud POST a la URL https://gabrielapinzon.pythonanywhere.com/api/v1/comentarios con los encabezados y datos proporcionados. Se utiliza requests.post para enviar la solicitud HTTP.
            response = requests.post(
                'https://gabrielapinzon.pythonanywhere.com/api/v1/comentarios/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("lista_comentarios")
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
                            'fitness/comentario/create.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    else:
         formulario = ComentarioForm(None)
    return render(request, 'fitness/comentario/create.html',{"formulario":formulario})

def comentario_obtener(request,comentario_id):
    print(comentario_id)
    comentario = helper.obtener_comentario(comentario_id)
    return render(request,'fitness/comentario/mostrar_comentario.html',{'comentario':comentario})
    
    
    
def comentario_editar(request,comentario_id):
    datosFormulario = None
    
    if request.method == 'POST':
        datosFormulario = request.POST
        
    #Obtenemos el comentario especifico llamando al metodo de nuetsra clase helper.
    comentario = helper.obtener_comentario(comentario_id)
    print(comentario)
    formulario = ComentarioForm(datosFormulario,
                                initial ={
                                    'usuario':comentario['usuario']['id'],
                                    'entrenamiento': comentario['entrenamiento']['id'],
                                    'texto': comentario['texto'],
                                    'fecha': comentario['fecha']
                                    
                                })
    
    if (request.method == "POST"):
            try:
                formulario = ComentarioForm(request.POST)
                headers = {
                    'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                    'Content-Type':'application/json'
                }
                datos = request.POST.copy()
                datos["fecha"] = str(
                                            datetime.date(year=int(datos['fecha_year']),
                                                        month=int(datos['fecha_month']),
                                                        day=int(datos['fecha_day']))
                                             )

                response = requests.put(
                    'https://gabrielapinzon.pythonanywhere.com/api/v1/comentarios/editar/'+ str(comentario_id), headers=headers, data=json.dumps(datos)
                )
                if(response.status_code == requests.codes.ok):
                    # Redirecciono al listado completo de comentarios.
                    return redirect("lista_comentarios")
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
                            'fitness/comentario/actualizar.html',
                            {"formulario":formulario,"comentario":comentario})
                else:
                    return mi_error_500(request)
            except Exception as err:
                print(f'Ocurrió un error: {err}')
                return mi_error_500(request)
    return render(request, 'fitness/comentario/actualizar.html',{"formulario":formulario,"comentario":comentario})


def comentario_editar_nombre(request,comentario_id):
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    comentario = helper.obtener_comentario(comentario_id)
    formulario = ComentarioActualizarTextoForm(datosFormulario,
            initial={
                'texto': comentario['texto'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = ComentarioActualizarTextoForm(request.POST)
            headers = {
                    'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                    'Content-Type':'application/json'
                }
            datos = request.POST.copy()
            response = requests.patch(
                'https://gabrielapinzon.pythonanywhere.com/api/v1/comentarios/actualizar/nombre/'+str(comentario_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect('lista_comentarios')
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
                            'fitness/comentario/actualizar_nombre.html',
                            {"formulario":formulario,"comentario":comentario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'fitness/comentario/actualizar_nombre.html',{"formulario":formulario,"comentario":comentario})


def comentario_eliminar(request,comentario_id):
    try:
        headers = {
                    'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                    'Content-Type':'application/json'
                }
        response = requests.delete(
            'https://gabrielapinzon.pythonanywhere.com/api/v1/comentarios/eliminar/'+str(comentario_id),
            headers=headers,
        )
        if(response.status_code == requests.codes.ok):
            return redirect("lista_comentarios")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('lista_comentarios')




#FUNCIONALIDADES DE MIS COMPAÑEROS:
#MANUEL:
def obtener_ejercicios_entrenamiento(request, entrenamiento_id):
    try:
        headers = {
                    'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                    'Content-Type':'application/json'
                }
        response = requests.get(
            'https://gabrielapinzon.pythonanywhere.com/api/v1/entrenamiento-ejercicios/'+str(entrenamiento_id),
            headers=headers,
        )
        ejercicios= response.json()
        if(response.status_code == requests.codes.ok):
            print(response.text)
            return render(request,'fitness/entrenamiento/ejercicios.html',{'ejercicios_mostrar':ejercicios})
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('lista_comentarios')


def mostrar_ejercicios_entrenamiento(request, entrenamiento_id):
    try:
        headers = {
                    'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                    'Content-Type':'application/json'
                }
        response = requests.get(
            'https://gabrielapinzon.pythonanywhere.com/api/v1/entrenamiento-ejercicios/'+str(entrenamiento_id),
            headers=headers,
        )
        ejercicios= response.json()
        if(response.status_code == requests.codes.ok):
            print(response.text)
            return render(request, 'fitness/entrenamiento/eleccion_ejercicios.html', {'ejercicios_mostrar': ejercicios})

        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)


def elegir_ejercicios(request):
    headers = crear_cabecera()
    response = requests.get('https://gabrielapinzon.pythonanywhere.com/api/v1/ejercicios',headers=headers)
    ejercicios = response.json()
    return render(request, 'fitness/eleccion_ejercicios.html',{'ejercicios_mostrar':ejercicios})


def historial_usuario(request):
    usuario_id = request.session.get('usuario', {}).get('id')
    if usuario_id is None:
        mensaje='No hay un usuario registrado con ese nombre.'
        return render(request, 'fitness/historial_usuario.html', {'mensaje':mensaje})
    headers = crear_cabecera()
    try:
        response = requests.get(f'https://gabrielapinzon.pythonanywhere.com/api/v1/historiales/{usuario_id}', headers=headers)
        
        historial = response.json()
        tiempo_total = 0
        calorias_total = 0
        for ejercicio in historial:
            fecha_str = ejercicio.get('fecha')
            print(fecha_str)
            if fecha_str:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%S%z')  # Analizar la fecha desde una cadena ISO 8601
                ejercicio['fecha'] = fecha.strftime('%Y-%m-%d %H:%M:%S')  # Formato deseado 

            #Calculo del tiempo y calorias de cada ejercicio:
            tiempo_total += ejercicio['duracion']
            calorias_total += ejercicio['calorias']
        calorias_total = int(calorias_total)
        print(tiempo_total)
        print(calorias_total)
        if(response.status_code == requests.codes.ok):
            print(response.text)
            return render(request, 'fitness/usuario/historial_usuario.html', {'historial_mostrar': historial,'tiempo':tiempo_total,'calorias':calorias_total})
        else:
            #print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    
def perfil_usuario(request):
    usuario_id = request.session.get('usuario', {}).get('id')
    print(f'Solicitando perfil de usuario para usuario ID {usuario_id}')
    if usuario_id is None:
        mensaje='No hay un usuario registrado con ese nombre.'
        return render(request, 'fitness/usuario/perfil_usuario.html', {'mensaje':mensaje})
    headers = crear_cabecera()
    try:
        response = requests.get(f'https://gabrielapinzon.pythonanywhere.com/api/v1/perfil-usuario/{usuario_id}', headers=headers)
        print(f'https://gabrielapinzon.pythonanywhere.com/api/v1/perfil-usuario/{usuario_id}')

        perfil_user = response.json()
        perfil_user = response.json()
        print('Respuesta de la API:', perfil_user)
        for perfil in perfil_user:
            fecha_creacion = perfil['usuario']['date_joined']
            print(fecha_creacion)
            if fecha_creacion:
                fecha = datetime.strptime(fecha_creacion, '%Y-%m-%dT%H:%M:%S%z')  # Analizar la fecha desde una cadena ISO 8601
                perfil['usuario']['date_joined'] = fecha.strftime('%Y-%m-%d %H:%M:%S') 
        print(perfil_user)
        if(response.status_code == requests.codes.ok):
            print(response.text)
            return render(request, 'fitness/usuario/perfil_usuario.html', {'perfil_mostrar': perfil_user})
        else:
            #print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)

def actualizar_perfil(request):
    usuario_id = request.session.get('usuario', {}).get('id')
    datosFormulario = None
    if request.method == 'POST':
        datosFormulario = request.POST
    #Obtenemos el ejercicio por la API.
    perfil = helper.obtener_usuario(usuario_id)
    #Especificamos cada uno de los valores que vamos a rellenar.
    formulario = ActualizarPerfilForm(datosFormulario,
                                initial ={
                                    'altura': perfil['altura'],
                                    'email': perfil['email'],
                                    'peso': perfil['peso'],
                                })
    
    if (request.method == "POST"):
            try:
                formulario = ActualizarPerfilForm(request.POST)
                headers = {
                    'Authorization': 'Bearer ' + env('TOKEN_CLIENTE'),
                    'Content-Type':'application/json'
                }
                datos = request.POST.copy()

                response = requests.put(
                    'https://gabrielapinzon.pythonanywhere.com/api/v1/usuario/'+ str(usuario_id), headers=headers, data=json.dumps(datos)
                )
                if(response.status_code == requests.codes.ok):
                    # Redirecciono al listado completo de recintos
                    return redirect("perfil-usuario")
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
                            'fitness/usuario/actualizar.html',
                            {"formulario":formulario,"perfil":perfil})
                else:
                    return mi_error_500(request)
            except Exception as err:
                print(f'Ocurrió un error: {err}')
                return mi_error_500(request)
    return render(request, 'fitness/usuario/actualizar.html',{"formulario":formulario,"perfil":perfil})

def musculos_busqueda_simple(request):
    formulario = BusquedaEjerciciosMusculoForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get(
            'https://gabrielapinzon.pythonanywhere.com/api/v1/ejercicios/musculos/busqueda',
            headers=headers,
            params=formulario.cleaned_data
        )
        ejercicios = response.json()
        return render(request, 'fitness/musculos/ejercicios.html',{"ejercicios_mostrar":ejercicios})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")





















































#REGISTRO:
def registrar_usuario(request):
    if(request.method=='POST'):
        try:
            formulario = RegistroForm(request.POST)
            if(formulario.is_valid()):
                headers = {
                    "Content-Type": "application/json"
                }
                response = requests.post(
                    'https://gabrielapinzon.pythonanywhere.com/api/v1/registrar/usuario',
                    headers=headers,
                    data=json.dumps(formulario.cleaned_data)
                )
                if(response.status_code == requests.codes.ok):
                    usuario = response.json()
                    token_acceso = helper.obtener_token_session(
                            formulario.cleaned_data.get("username"),
                            formulario.cleaned_data.get("password1")
                            )
                    request.session["usuario"]=usuario
                    request.session["token"] = token_acceso
                    return redirect("index")
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
                            'registration/signup.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)            
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})


def login(request):
    if (request.method == "POST"):
        formulario = LoginForm(request.POST)
        try:
            token_acceso = helper.obtener_token_session(
                                formulario.data.get("usuario"),
                                formulario.data.get("password")
                                )
            request.session["token"] = token_acceso
            
          
            headers = {'Authorization': 'Bearer '+token_acceso} 
            response = requests.get('https://gabrielapinzon.pythonanywhere.com/api/v1/usuario/token/'+token_acceso,headers=headers)
            usuario = response.json()
            request.session["usuario"] = usuario
            
            return  redirect("index")
        except Exception as excepcion:
            print(f'Hubo un error en la petición: {excepcion}')
            formulario.add_error("usuario",excepcion)
            formulario.add_error("password",excepcion)
            return render(request, 
                            'registration/login.html',
                            {"form":formulario})
    else:  
        formulario = LoginForm()
    return render(request, 'registration/login.html', {'form': formulario})


    
def logout(request):
    request.session.clear()
    return redirect('index')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)
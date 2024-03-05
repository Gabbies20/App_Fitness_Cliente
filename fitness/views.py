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
    #headers = {'Authorization':'Bearer sem6IlXzR1ER9DcjyLd0FOVuwRurdk'}
    headers = crear_cabecera()
    response = requests.get('http://127.0.0.1:8000/api/v1/ejercicios',headers=headers)
    #response = requests.get('http://gabrielapinzon.pythonanywhere.com/api/v1/ejercicios',headers=headers)
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
    headers = crear_cabecera()
    response = requests.get('http://127.0.0.1:8000/api/v1/entrenamientos',headers=headers)
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

def entrenamiento_crear(request):
    
    if (request.method == "POST"):
        try:
            formulario = EntrenamientoForm(request.POST)
            headers =  {
                        'Authorization': 'Bearer '+env("TOKEN_CLIENTE"),
                        "Content-Type": "application/json" 
                    } 
            datos = formulario.data.copy()
            datos["usuarios"] = request.POST.getlist("usuarios")
            datos["ejercicios"] = request.POST.getlist("ejercicios")
            
            response = requests.post(
                'http://127.0.0.1:8000/api/v1/entrenamientos/crear',
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
    print(entrenamiento_id)
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

                response = requests.put(
                    'http://127.0.0.1:8000/api/v1/entrenamientos/editar/'+ str(entrenamiento_id), headers=headers, data=json.dumps(datos)
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

def entrenamiento_editar_nombre(request,entrenamiento_id):
    pass

def entrenamiento_eliminar(request,entrenamiento_id):
    pass



""" 
    VISTAS DE COMENTARIOS:
"""
def comentarios_lista_api(request):
    headers = crear_cabecera()
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
                'http://127.0.0.1:8000/api/v1/comentarios/busqueda_avanzada',
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
            formulario = ComentarioForm(request.POST)
            print("Datos del formulario:",formulario.data)
            headers =  {
                        'Authorization': 'Bearer '+env("TOKEN_CLIENTE"),
                        "Content-Type": "application/json" 
                    } 
            datos = formulario.data.copy()
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

            
            response = requests.post(
                'http://127.0.0.1:8000/api/v1/comentarios/crear',
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
    return render(request,'fitness/comentario/comentario_mostrar.html',{'comentario':comentario})
    
    
    
    
def comentario_editar(request,comentario_id):
    pass
    
    
def registrar_usuario(request):
    if(request.method=='POST'):
        try:
            formulario = RegistroForm(request.POST)
            if(formulario.is_valid()):
                headers = {
                    "Content-Type": "application/json"
                }
                response = requests.post(
                    'http://127.0.0.1:8000/api/v1/registrar/usuario',
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
            response = requests.get('http://127.0.0.1:8000/api/v1/usuario/token/'+token_acceso,headers=headers)
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
import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)

  
class helper:
    
    def obtener_usuarios_select():
        #Obtenemos todos los usuarios:
        headers = {'Authorization': 'Bearer ' +env("TOKEN_CLIENTE")}
        response = requests.get('http://127.0.0.1:8000/api/v1/usuarios',headers=headers)
        usuarios = response.json()
        
        lista_usuarios = [('','Ninguna')]
        for usuario in usuarios:
            lista_usuarios.append((usuario['id'],usuario['username']))
        return lista_usuarios
    
    
    def obtener_grupos_musculares():
        headers = {'Authorization': 'Bearer ' +env("TOKEN_CLIENTE")}
        response = requests.get('http://127.0.0.1:8000/api/v1/grupos-musculares',headers=headers)
        grupos_musculares = response.json()
        
        lista_grupos = [('','Ninguno')]
        for grupo in grupos_musculares:
            lista_grupos.append((grupo['id'],grupo['nombre']))
        return lista_grupos
        
    def obtener_ejercicio(id):
        #Obtenemos todos los ejercicios.
        headers = {'Authorization':'Bearer '+env('TOKEN_CLIENTE')}
        response = requests.get('http://127.0.0.1:8000/api/v1/ejercicio/'+str(id),headers=headers)
        ejercicio = response.json()
        return ejercicio
    
    def obtener_usuario(id):
        #Obtenemos todos los ejercicios.
        headers = {'Authorization':'Bearer '+env('TOKEN_CLIENTE')}
        response = requests.get('http://127.0.0.1:8000/api/v1/usuario/'+str(id),headers=headers)
        usuario = response.json()
        return usuario
    
    def obtener_ejercicios_select():
        #Obtenemos todos los usuarios:
        headers = {'Authorization': 'Bearer ' +env("TOKEN_CLIENTE")}
        response = requests.get('http://127.0.0.1:8000/api/v1/ejercicios',headers=headers)
        ejercicios = response.json()
        
        lista_ejercicios = [('','Ninguna')]
        for ejercicio in ejercicios:
            lista_ejercicios.append((ejercicio['id'],ejercicio['nombre']))
        return lista_ejercicios
    
    def obtener_entrenamiento(id):
        #Obtenemos todos los entrenamientos.
        headers = {'Authorization':'Bearer '+env('TOKEN_CLIENTE')}
        response = requests.get('http://127.0.0.1:8000/api/v1/entrenamiento/'+str(id),headers=headers)
        entrenamiento = response.json()
        return entrenamiento 
    
    def obtener_comentario(id):
        #Obtener todos los comentarios.
        headers ={'Authorization':'Bearer '+env('TOKEN_CLIENTE')}
        response = requests.get('http://127.0.0.1:8000/api/v1/comentario/'+str(id),headers=headers)
        comentario = response.json()
        #print(comentario)
        return comentario

    def obtener_entrenamiento_select():
        #Obtenemos todos los usuarios:
        headers = {'Authorization': 'Bearer ' +env("TOKEN_CLIENTE")}
        response = requests.get('http://127.0.0.1:8000/api/v1/entrenamientos',headers=headers)
        entrenamientos = response.json()
        
        lista_entrenamientos = [('','Ninguna')]
        for entrenamiento in entrenamientos:
            #print(entrenamiento)
            lista_entrenamientos.append((entrenamiento['id'],entrenamiento['nombre']))
        return lista_entrenamientos
    
    
    def obtener_token_session(usuario,password):
            token_url = 'http://127.0.0.1:8000/oauth2/token/'
            data = {
                'grant_type': 'password',
                'username': usuario,
                'password': password,
                'client_id': 'gabriela',
                'client_secret': 'gabriela',
            }

            response = requests.post(token_url, data=data)
            respuesta = response.json()
            if response.status_code == 200:
                return respuesta.get('access_token')
            else:
                raise Exception(respuesta.get("error_description"))
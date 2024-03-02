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
    
    def obtener_ejercicio(id):
        #Obtenemos todos los ejercicios.
        headers = {'Authorization':'Bearer '+env('TOKEN_CLIENTE')}
        response = requests.get('http://127.0.0.1:8000/api/v1/ejercicio/'+str(id),headers=headers)
        ejercicio = response.json()
        return ejercicio
    
    def obtener_entrenamiento(id):
        #Obtenemos todos los entrenamientos.
        headers = {'Authorization':'Bearer '+env('TOKEN_CLIENTE')}
        response = requests.get('http://127.0.0.1:8000/api/v1/entrenamiento/'+str(id),headers=headers)
        entrenamiento = response.json()
        return entrenamiento 
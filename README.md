# App_Fitness_Cliente
import requests
from django.http import JsonResponse

def obtener_entrenamientos_desde_api(url):
    try:
        response = requests.get(url)
        # Verificar si la solicitud fue exitosa
        response.raise_for_status()

        # Verificar el tipo de contenido de la respuesta
        content_type = response.headers.get('Content-Type')
        if 'application/json' in content_type:
            # Si el contenido es JSON, cargamos y devolvemos los datos
            return response.json()
        else:
            # Si el contenido no es JSON, devolvemos un mensaje de error
            return {'error': 'El contenido de la respuesta no es JSON'}

    except requests.exceptions.RequestException as e:
        # Si hay algún error en la solicitud, devolvemos un mensaje de error
        return {'error': f'Error al obtener datos de la API: {str(e)}'}


def entrenamientos_lista_api(request):
    url_api = 'http://127.0.0.1:8000/api/v1/entrenamientos'
    entrenamientos = obtener_entrenamientos_desde_api(url_api)

    if 'error' in entrenamientos:
        # Si ocurrió un error al obtener los datos de la API, devolvemos un mensaje de error
        return JsonResponse(entrenamientos, status=500)

    return render(request, 'fitness/lista_api_entrenamientos.html', {'entrenamientos_mostrar': entrenamientos})

--------------
En este ejemplo, la función obtener_entrenamientos_desde_api() se encarga de realizar la solicitud a la API y manejar diferentes escenarios:

Si la solicitud es exitosa y el contenido es JSON, carga y devuelve los datos en formato JSON.
Si la solicitud es exitosa pero el contenido no es JSON, devuelve un mensaje de error indicando que el contenido no es JSON.
Si ocurre algún error durante la solicitud, devuelve un mensaje de error con detalles sobre el error.
Luego, en la vista entrenamientos_lista_api(), verificamos si hay algún error en la respuesta de la API. Si hay un error, devolvemos un JsonResponse con un mensaje de error y un código de estado HTTP 500 (Error del servidor). De lo contrario, pasamos los datos obtenidos a la plantilla para su renderización.

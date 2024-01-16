from django.shortcuts import render,redirect
from django.views.defaults import page_not_found

from django.contrib import messages
from django.db.models import Q,F
from .forms import *
from datetime import datetime
from django.contrib.auth.models import Group
from django.contrib.auth import login
import requests
from django.core import serializers


# Create your views here.
def index(request):
  
    return render(request, 'fitness/index2.html')


def ejercicios_lista_api(request):
    #Obtenemos los ejercicios.
    response = requests.get('http://127.0.0.1:8000/api/v1/ejercicios')
    #Transformamos la respuesta de json.
    ejercicios = response.json()
    return render(request, 'fitness/lista_api.html',{'ejercicios_mostrar':ejercicios})


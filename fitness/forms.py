from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime


class BusquedaEjercicioForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    


    """class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo_ejercicio = models.CharField(max_length=20)
    usuarios = models.ManyToManyField(Usuario, through='HistorialEjercicio')
    #usuarios_votos = models.ManyToManyField(Usuario,through='Voto',related_name='usuarios_votos')

    def __str__(self) -> str:
        return self.nombre
    """
class BusquedaEjercicioAvanzadaForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    
    textoBusqueda = forms.CharField(required=False)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)


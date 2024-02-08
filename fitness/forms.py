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

class BusquedaEntrenamientoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    

class BusquedaEntrenamientoAvanzadaForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
    TIPOS= [
        ('AER','Aerobico'),
        ('FUE', 'Fuerza o Anaerobico'),
        ('FUN','Funcional'),
        ('HIT','Hit'),
        ('POT','Potencia'),
    ]
    
    tipos = forms.MultipleChoiceField(choices=TIPOS,
                                    required=False,
                                    widget=forms.CheckboxSelectMultiple)
    
    #usuario = forms.CharField(required=True)
    nombre = forms.CharField(required=True)
    descripcion = forms.Textarea(required=True)
    duracion = forms.IntegerField()
    
from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime
from.helper import helper

#EJERCICIOS:
class BusquedaEjercicioForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
 
class BusquedaEjercicioAvanzadaForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    
    textoBusqueda = forms.CharField(required=False)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)

class EjercicioForm(forms.Form):
    nombre = forms.CharField(required=True)
    descripcion = forms.CharField(widget=forms.Textarea, required=True)
    tipo_ejercicio = forms.CharField(required=True)
    
    def ___init__(self, *args, **kwargs):
        super(EjercicioForm,self).__init__(*args,**kwargs)
        
        usuariosDisponibles = helper.obtener_usuarios_select()
        self.fields['usuarios'] = forms.ChoiceField(
            choices=usuariosDisponibles,
            widget=forms.Select,
            required=True,
        )
        
        
    
    
#ENTRENAMIENTOS:
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
    nombre = forms.CharField(required=False)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)
    duracion = forms.IntegerField()
    
"""class BusquedaAvanzadaEntrenamientoForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    tipos = forms.MultipleChoiceField(choices =Entrenamiento.TIPOS,
                                      required=False,
                                      widget=forms.CheckboxSelectMultiple())
    duracion = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'min': 1, 'max': 100, 'class': 'tu-clase-css'})
    )
"""

#COMENTARIOS:
class BusquedaComentarioForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    

class BusquedaComentarioAvanzadoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    fecha = forms.DateField(label='Fecha:',
                            required=False,
                            widget=forms.SelectDateWidget(years=range(1950,2025)))


    
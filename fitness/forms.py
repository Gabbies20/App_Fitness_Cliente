from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime
from.helper import helper
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
    
    def __init__(self, *args, **kwargs):
        super(EjercicioForm,self).__init__(*args,**kwargs)
        
        usuariosDisponibles = helper.obtener_usuarios_select()
        self.fields['usuarios'] = forms.ChoiceField(
            choices=usuariosDisponibles,
            widget=forms.Select,
            required=True,
        )
    
class EjercicioActualizarNombreForm(forms.Form):
    nombre = forms.CharField(label='Nombre',
                             required=True,
                             max_length=200,
                             help_text="200 caracteres como máximo") 
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
    
class EntrenamientoForm(forms.Form):
    nombre = forms.CharField(label='Nombre',
                             required=True,
                             max_length=200,
                             help_text='200 caracteres como máximo')
    descripcion = forms.CharField(label='Descripción',
                                  required=False,
                                  widget=forms.Textarea())
    duracion = forms.IntegerField()
    
    TIPOS = [
        ('AER','Aeróbico'),
        ('FUE','Fuerza o Anaeróbico'),
        ('FUN','Funcional'),
        ('HIT','Hit'),
        ('POT','Potencia')
    ]
    
    tipo = forms.ChoiceField(choices=TIPOS,
                             initial='ES')
    
    def __init__(self, *args, **kwargs):
        super(EntrenamientoForm,self).__init__(*args,**kwargs)
        
        usuariosDisponibles = helper.obtener_usuarios_select()
        self.fields['usuario'] = forms.ChoiceField(
            choices=usuariosDisponibles,
            widget=forms.Select,
            required=True,
        )
        
        ejerciciosDisponibles = helper.obtener_ejercicios_select()
        self.fields['ejercicios'] = forms.ChoiceField(
            choices=ejerciciosDisponibles,
            widget=forms.Select,
            required=True
            
        )
    
class EntrenamientoActualizarNombreForm(forms.Form):
    descripcion = forms.CharField(label='Descripción',
                             required=True,
                             max_length=500,
                             help_text="500 caracteres como máximo")



#COMENTARIOS:
class BusquedaComentarioForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    

class BusquedaComentarioAvanzadoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    fecha = forms.DateField(label='Fecha:',
                            required=False,
                            widget=forms.SelectDateWidget(years=range(1950,2025)))


class ComentarioForm(forms.Form):
    texto = forms.CharField(label='Texto',
                             required=True,
                             max_length=200,
                             help_text='200 caracteres como máximo')
    fecha = forms.DateField(label='Fecha',
                            initial=datetime.date.today,
                            widget=forms.SelectDateWidget()
                            )
    
    def __init__(self, *args, **kwargs):
        super(ComentarioForm,self).__init__(*args,**kwargs)
        
        usuariosDisponibles = helper.obtener_usuarios_select()
        self.fields['usuario'] = forms.ChoiceField(
            choices=usuariosDisponibles,
            widget=forms.Select,
            required=True,
        )
        
        entrenamientosDisponibles = helper.obtener_entrenamiento_select()
        self.fields['entrenamiento'] = forms.ChoiceField(
            choices=entrenamientosDisponibles,
            required=True,
            help_text='Mantén pulsada la tecla para seleccionar los entrenamientos.'
        )
        
    
    
    
class ComentarioActualizarTextoForm(forms.Form):
    texto = forms.CharField(label='Texto',
                             required=True,
                             max_length=200,
                             help_text="200 caracteres como máximo") 


class RegistroForm(UserCreationForm):
    roles = (
                (2,'cliente'),
                (3,'entrenador')
    )
    
    rol = forms.ChoiceField(choices=roles)
    class Meta:
        model = User
        fields = ('username','email','password1','password2','rol')
        
        
class LoginForm(forms.Form):
    usuario = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
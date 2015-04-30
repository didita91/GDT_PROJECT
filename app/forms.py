# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
from app.models import *
from app.helper import *
import datetime
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UsuariosForm(forms.Form):
#	def custom_validate_email(value):
 #   		if custom_check:
  #      		raise forms.ValidationError('Email format is incorrect')
   	username = forms.CharField(max_length=30, label='USUARIO')
	first_name = forms.CharField(max_length=30, label='NOMBRE')
	last_name = forms.CharField(max_length=30, label='APELLIDO')
	email = forms.EmailField(max_length=75, label='EMAIL',validators=[validate_email])
	password = forms.CharField(max_length=128, label='CONTRASEÑA', widget=forms.PasswordInput())
	password2 = forms.CharField(max_length=128, label='CONFIRMAR CONTRASEÑA', widget=forms.PasswordInput())

	def clean_password2(self):
		#comprobar que las contrasenas dadas sean iguales
		if 'password' in self.cleaned_data:
			password = self.cleaned_data['password']
			password2 = self.cleaned_data['password2']
			if password == password2:
				return password2
		raise forms.ValidationError('Las contrasenas no coinciden')

	def clean_username(self):
		#controlar que ya no existe el nombre de usuario
		if 'username' in self.cleaned_data:
			usuarios = User.objects.all()
			nuevo = self.cleaned_data['username']
			for i in usuarios:
				if i.username == nuevo:
					raise forms.ValidationError('Ya existe ese nombre de usuario. Elija otro')
			return nuevo
	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("Ya esta registrado este email.")
		return email
class ModUsuariosForm(forms.Form):
    #Modificar datos del usuario
	first_name = forms.CharField(max_length=30, label='NOMBRE')
	last_name = forms.CharField(max_length=30, label='APELLIDO')
	email = forms.EmailField(max_length=75, label='EMAIL')

class CambiarPasswordForm(forms.Form):
    #Cambiar contraseñas
	password1 = forms.CharField(widget = forms.PasswordInput, max_length=128, label = u'ESCRIBA SU NUEVA CONTRASEÑA')
	password2 = forms.CharField(widget = forms.PasswordInput, max_length=128, label = u'REPITA SU NUEVA CONTRASEÑA')

	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
			if password1 == password2:
				return password2
		raise forms.ValidationError('Las contraseñas no coinciden')

class AsignarRolesForm(forms.Form):
    #Asignar roles
	roles = forms.ModelMultipleChoiceField(queryset = None, label = 'ROLES DISPONIBLES', required=False)

	def __init__(self, cat, *args, **kwargs):
		super(AsignarRolesForm, self).__init__(*args, **kwargs)
		self.fields['roles'].queryset = Rol.objects.filter(categoria = cat)



class RolesForm(forms.Form):
    #Formulario de roles
	nombre = forms.CharField(max_length=50, label='NOMBRE')
	descripcion = forms.CharField(widget=forms.Textarea(), required=False, label='DESCRIPCIÓN')
	categoria = forms.CharField(max_length=1, widget=forms.Select(choices=CATEGORY_CHOICES), label='ELIJA UNA CATEGORIA')


	def clean_nombre(self):
		if 'nombre' in self.cleaned_data:
			roles = Rol.objects.all()
			nombre = self.cleaned_data['nombre']
			for i in roles:
				if nombre == i.nombre:
					raise forms.ValidationError('Ya existe ese nombre de rol. Elija otro')
			return nombre


class PermisosForm(forms.Form):
	permisos = forms.ModelMultipleChoiceField(queryset = Permiso.objects.filter(categoria = 1),  required = False)

class PermisosProyectoForm(forms.Form):

	permisos = forms.ModelMultipleChoiceField(queryset = Permiso.objects.filter(categoria = 2), widget = forms.CheckboxSelectMultiple, required = False, label = u'PERMISOS')


class ModRolesForm(forms.Form):
	descripcion = forms.CharField(widget=forms.Textarea(), required=False, label='DESCRIPCIÓN')


class FilterForm(forms.Form):
    filtro = forms.CharField(max_length = 30, label = 'BUSCAR', required=False)
    paginas = forms.CharField(max_length=2, widget=forms.Select(choices=(('5','5'),('10','10'),('15','15'),('20','20'))), label='MOSTRAR')

class FilterForm2(forms.Form):
    filtro1 = forms.CharField(max_length = 30, label = 'BUSCAR', required=False)
    paginas1 = forms.CharField(max_length=2, widget=forms.Select(choices=(('5','5'),('10','10'),('15','15'),('20','20'))), label='MOSTRAR')
    filtro2 = forms.CharField(max_length = 30, label = 'BUSCAR', required=False)
    paginas2 = forms.CharField(max_length=2, widget=forms.Select(choices=(('5','5'),('10','10'),('15','15'),('20','20'))), label='MOSTRAR')




class ProyectosForm(forms.Form):
    """Formulario para la creacion de proyectos."""
    nombre = forms.CharField(max_length=50, label='NOMBRE')
    usuario_scrum = forms.ModelChoiceField(queryset=None, label='SCRUM MASTER')
    product_owner = forms.ModelChoiceField(queryset=None, label='PRODUCT OWNER')
    descripcion = forms.CharField(widget=forms.Textarea(), required=False, label='DESCRIPCIÓN')
    fecha_inicio = forms.DateField(required=False, label='FECHA DE INICIO')
    sprint = forms.IntegerField(min_value=1,max_value=100)
    def __init__(self,*args, **kwargs):
                super(ProyectosForm, self).__init__(*args, **kwargs)
                self.fields['usuario_scrum'].queryset = RolUsuario.objects.filter()
                self.fields['product_owner'].queryset = ProductOwner.objects.filter()
    def clean_nombre(self):
        if 'nombre' in self.cleaned_data:
                nuevo = self.cleaned_data['nombre']
                proyectos = Proyecto.objects.all()
                nuevo = self.cleaned_data['nombre']
                for proyecto in proyectos:
                        if proyecto.nombre == nuevo:
                                raise forms.ValidationError('Ya existe ese nombre. Elija otro')
                return nuevo



class UsuarioProyectoForm(forms.Form):
    usuario = forms.ModelChoiceField(queryset = None)
    #roles = forms.ModelMultipleChoiceField(queryset = Rol.objects.filter(categoria=2).exclude(id=2), widget = forms.CheckboxSelectMultiple, required=False)

    proyecto = Proyecto()

    def __init__(self, proyecto,*args, **kwargs):
        super(UsuarioProyectoForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.filter(~Q(id = proyecto.usuario_scrum.usuario.id))

    #El problema se encontraba en el if no estaba igualando correctamente
    def clean_usuario(self):
        if 'usuario' in self.cleaned_data:
            usuarios_existentes = UsuarioRolProyecto.objects.filter()
            print "probandoooo"
            for i in usuarios_existentes:
                print i.usuario
                if(i.usuario == self.cleaned_data['usuario']):
                    print "teeeeeeeest"
                    raise forms.ValidationError('Ya existe este usuario')
            return self.cleaned_data['usuario']

class ModProyectosForm(forms.Form):
    """Formulario para la creacion de proyectos."""
    nombre = forms.CharField(max_length=50, label='NOMBRE')
    #usuario_scrum = forms.ModelChoiceField(queryset=User.objects.all(), label='SCRUM')
    descripcion = forms.CharField(widget=forms.Textarea(), required=False, label='DESCRIPCIÓN')
    #fecha_inicio = forms.DateField(required=False, label='FECHA DE INICIO')

    def __init__(self, proyecto, *args, **kwargs):
        super(ModProyectosForm, self).__init__(*args, **kwargs)
        self.proyecto = proyecto

    def clean_nombre(self):
        if 'nombre' in self.cleaned_data:
            nuevo = self.cleaned_data['nombre']
            if nuevo != self.proyecto.nombre:
                proyectos = Proyecto.objects.all()
                nuevo = self.cleaned_data['nombre']
                for proyecto in proyectos:
                    if proyecto.nombre == nuevo:
                        raise forms.ValidationError('Ya existe ese nombre. Elija otro')
            return nuevo
class FlujosForm(forms.Form):
    #Formulario de flujos
    nombre = forms.CharField(required=True, max_length=50, label='NOMBRE')

    def clean_nombre(self):
		if 'nombre' in self.cleaned_data:
			flujo = Flujo.objects.all()
			nombre = self.cleaned_data['nombre']
			for i in flujo:
				if nombre == i.nombre:
					raise forms.ValidationError('Ya existe ese nombre de rol. Elija otro')
			return nombre

class ActividadesForm(forms.Form):
    """Formulario para la creacion de proyectos."""
    nombre = forms.CharField(max_length=50, label='NOMBRE')


    def clean_nombre(self):
        if 'nombre' in self.cleaned_data:
                acti = Actividades.objects.all()
                nuevo = self.cleaned_data['nombre']
                for activ in acti:
                        if activ.nombre == nuevo:
                                raise forms.ValidationError('Ya existe ese nombre. Elija otro')
                return nuevo
class ModActividadesForm(forms.Form):
    #Modificar datos del usuario
        nombre = forms.CharField(max_length=30, label='NOMBRE')
	

        
class AddActividadesForm(forms.Form):
    #Asignar roles
    actividades = forms.ModelMultipleChoiceField(queryset = None, label = 'ACTIVIDADES DISPONIBLES', required=False)
    def __init__(self, proyecto, *args, **kwargs):
        super(AddActividadesForm, self).__init__(*args, **kwargs)
        self.fields['actividades'].queryset = Actividades.objects.filter(proyecto=proyecto)
#************************************************USER STORY*************************************************
class UserStoryForm(forms.Form):
    nombre = forms.CharField(required=True,max_length=50, label= 'NOMBRE')
    prioridad = forms.IntegerField(min_value=1,max_value=10)
    valor_negocio=forms.IntegerField(min_value=1,max_value=10) #del 1 al 10 donde 10 es de mas valor que 1
    valor_tecnico=forms.IntegerField(min_value=1,max_value=10) #del 1 al 10 donde 10 es de mas valor que 1
    duracion= forms.IntegerField(min_value=1,max_value=100) #Duracion estimativa en dias de la historia de usuario
    descripcion= forms.CharField(widget=forms.Textarea(), required=False, label='Descripcion')

    def clean_nombre(self):
		if 'nombre' in self.cleaned_data:
			roles = UserStory.objects.all()
			nombre = self.cleaned_data['nombre']
			for i in roles:
				if nombre == i.nombre:
					raise forms.ValidationError('Ya existe ese nombre de rol. Elija otro')
			return nombre

#************
class AdjuntoForm(forms.Form):
    archivo = forms.FileField(required = False)

class ModUserStoryForm(forms.Form):
    #Modificar datos del usuario
       nombre = forms.CharField(max_length=30, label='NOMBRE')
       descripcion= forms.CharField(widget=forms.Textarea(), required=False, label='Descripcion')
 
#**********************EQUIPO DE TRABAJO EN SPRINT
class MiembroEquipoForm(forms.Form):
    usuario = forms.ModelChoiceField(required=True, queryset = None)
    proyecto = Proyecto()
    sprint = 1
    horas=forms.IntegerField(min_value=1, max_value=1000)

    def __init__(self, proyecto, *args, **kwargs):
        super(MiembroEquipoForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].queryset = UsuarioRolProyecto.objects.filter(proyecto=proyecto.id)
    def clean_usuario(self):
		if 'usuario' in self.cleaned_data:
			roles = UsuarioRolProyecto.objects.all(usuario=self)
			nombre = self.cleaned_data['usuario']
			for i in roles:
				if nombre == i.usuario:
					raise forms.ValidationError('Ya existe ese nombre de rol. Elija otro')
			return nombre

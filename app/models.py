# -*- coding: iso-8859-15 -*-
from django.db import models
from django.contrib.auth.models import User
#from Proyecto.models import Proyecto
# Create your models here.

""" Categorias de Rol """
CATEGORY_CHOICES = (
                 ('1', 'Rol de Sistema'),
		         ('2', 'Rol de Proyecto'),

             )
""" Estados de Actividades """
status_activity = (
                 ('1', 'To Do'),
		         ('2', 'Doing'),
                 ('3', 'Done'),
             )

"""Estados de los UserStories"""
STATUS_CHOICES = (
 	            ('En Espera', 'En Espera'),
 	            ('En Proceso', 'En Proceso'),
                ('Aprobado', 'Aprobado'),
                ('Inactivo', 'Inactivo')
                )
SPRINT_STATUS = (
 	            ('Iniciado', 'Iniciado'),
 	            ('Terminado', 'Terminado'),

                )
class Permiso(models.Model):

    """
    Contiene datos de permisos para cada usuario
    - nombre: nombre del permiso
    - categoria: se refiere al tipo de rol al que puede pertenecer, puede ser rol de sistema o rol de proyecto
    """
    nombre = models.CharField(unique=True, max_length = 50)
    categoria = models.IntegerField(max_length=1, choices=CATEGORY_CHOICES)

    def __unicode__(self):
        return self.nombre


class Rol(models.Model):

    """
    Contiene datos de cada rol
    - nombre: nombre del permiso
    - categoria: puede ser de sistema o de proyecto
    - descripcion: informacion sobre el rol
    - fecHor_creacion: fecha y hora de creacion del rol
    - usuario_creador: usuario responsable de la creacion del rol
    - permisos: permisos admitidos para el rol
    """
    nombre = models.CharField(unique=True, max_length=50)
    categoria = models.IntegerField(max_length=1, choices=CATEGORY_CHOICES)
    descripcion = models.TextField(null=True, blank=True)
    fecHor_creacion = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True, editable=False)
    usuario_creador = models.ForeignKey(User, null=True)
    permisos = models.ManyToManyField(Permiso, through='RolPermiso')

    def __unicode__(self):
        return self.nombre



class RolPermiso(models.Model):
    """
    Clasifica los permisos que pertenecen a rol sistema o rol proyecto
    """
    rol = models.ForeignKey(Rol)
    permiso = models.ForeignKey(Permiso)



class UsuarioRolSistema(models.Model):
    """
    Tabla que contiene la lista de usuarios pertenecientes a cada rol
    """

    usuario = models.ForeignKey(User)
    rol = models.ForeignKey(Rol)

    class Meta:
        unique_together = [("usuario", "rol")]

class RolUsuario(models.Model):
	usuario =models.ForeignKey(User)
	def __unicode__(self):
		return self.usuario.username
class ProductOwner(models.Model):
        usuario =models.ForeignKey(User)
        def __unicode__(self):
                return self.usuario.username


class Proyecto(models.Model):
    """
    Contiene los datos de cada proyecto
    """
    nombre = models.CharField(unique=True, max_length=50)
    usuario_scrum = models.ForeignKey(RolUsuario)
    descripcion = models.TextField(null=True, blank= True)
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    duracion_sprint= models.PositiveIntegerField(null=True)
    def __unicode__(self):
        return self.nombre
class UsuarioRolProyecto(models.Model):
    """
    Contiene la lista de usuarios con sus roles en cada proyecto
    """
    usuario = models.ForeignKey(User)
    rol = models.ForeignKey(Rol, null=True)
    proyecto = models.ForeignKey(Proyecto)
    eq= models.IntegerField(max_length=15,null=True)
    class Meta:
        unique_together = [("usuario", "rol", "proyecto","eq")]
    def __unicode__(self):
        return self.usuario

class Flujo(models.Model):

    nombre = models.CharField( max_length=50)
    proyecto = models.ForeignKey(Proyecto)
    def __unicode__(self):
        return self.nombre


class Actividades(models.Model):

    nombre = models.CharField( max_length=50)
    estado = models.IntegerField(max_length=1, default=1)
    proyecto = models.ForeignKey(Proyecto)
    def __unicode__(self):
        return self.nombre

class ActividadesFlujo(models.Model):
    actividades = models.ForeignKey(Actividades, null=True)
    flujo = models.ForeignKey(Flujo)
    proyecto = models.ForeignKey(Proyecto)
    class Meta:
        unique_together = [("actividades", "flujo","proyecto")]
    def __unicode__(self):
        return self.actividades.nombre

#---------------------------CONFIGURACION DE SPRINT
class Equipo(models.Model):
    usuario = models.ForeignKey(UsuarioRolProyecto)
    horas = models.PositiveIntegerField()#horas de trabajo de ese miembro
    sprint = models.PositiveIntegerField()#sprint en el que se encuentra
    proyecto = models.ForeignKey(Proyecto)

    def __unicode__(self):
        return self.usuario
#***************************************USER STORY**********************************************
class UserStory(models.Model):
        nombre = models.CharField( max_length=50)
        estado = models.CharField(max_length=10, choices=STATUS_CHOICES)
        version = models.PositiveIntegerField()
        prioridad = models.IntegerField(max_length=3) #del 1 al 100 donde 1 es mas prioritario
        habilitado = models.BooleanField(default=True)
        valor_negocio=models.IntegerField(max_length=2) #del 1 al 10 donde 10 es de mas valor que 1
        valor_tecnico=models.IntegerField(max_length=2) #del 1 al 10 donde 10 es de mas valor que 1
        duracion=models.IntegerField(max_length=2) #Duracion estimativa en dias de la historia de usuario
        descripcion = models.TextField(null=True, blank= True)
        proyecto = models.ForeignKey(Proyecto,null=True) #Proyecto al cual pertenece
        flujo= models.ForeignKey(Flujo,null=True)
        responsable = models.ForeignKey(User,null=True)
        horas = models.PositiveIntegerField(null=True)#horas de trabajo de ese miembro
        actividad= models.ForeignKey(ActividadesFlujo,null=True)
        estado_actividad= models.IntegerField(default=1)
        def __unicode__(self):
                return self.nombre



class ResponsableUS(models.Model):
    usuario = models.ForeignKey(Equipo)
    us = models.ForeignKey(UserStory)
    def __unicode__(self):
        return unicode(self.usuario)

class flujoUS(models.Model):
    flujo=models.ForeignKey(Flujo)
    us = models.ForeignKey(UserStory)
    def __unicode__(self):
        return unicode(self.flujo)


class UsSprint(models.Model):
    us=models.ForeignKey(UserStory)
    sprint=models.IntegerField()
    estado = models.CharField(max_length=10, choices=SPRINT_STATUS)
    def __unicode__(self):
        return unicode(self.us)

#ARCHIVO ADJUNTO
class Documento(models.Model):
    """Clase que representa el tipo de archivo a adjuntar a un user story"""
    docfile = models.FileField(upload_to='documentos/%Y/%m/%d')
     #claves foraneas
    us = models.ForeignKey(UserStory)


class Historial(models.Model):
    """Clase que representa el historial de los user stories"""
    #usuario = models.ForeignKey(User)
    fecha_creacion = models.DateField(auto_now =False, auto_now_add=True, editable=False)
   # descripcion = models.TextField(null=True,blank=True)
    #claves foraneas
    #user_story = models.OneToOneField(UserStory, parent_link=False)
    user_story = models.ForeignKey(UserStory)
    documento=models.ForeignKey(Documento,null=True)

class RegistroHistorial(models.Model):
    """Clase que representa el Registro de tareas de los user stories"""
    #version = models.PositiveIntegerField()
    prioridad = models.IntegerField()
    descripcion = models.TextField(null=True, blank=True)
    habilitado = models.BooleanField()
    fecha_modificacion = models.DateTimeField(auto_now=True, auto_now_add=False, editable=False)
    #claves foraneas
    historial = models.ForeignKey(Historial)
    us= models.ForeignKey(UserStory)

class Sprint(models.Model):
    """ Clase de Sprint, tiene los campos: Estado, proyecto y nro. de sprint"""
    estado = models.CharField(max_length=10, choices=SPRINT_STATUS)
    proyecto = models.ForeignKey(Proyecto)
    nro_sprint=models.PositiveIntegerField()


class Tarea(models.Model):
    """Clase para el registro de una tarea, posee los siguientes campos:
    descripcion: de la tarea realizada
    nombre: dado a la tarea
    tiempo: invertido en su realizacion
    us: user story al que se le agrega la tarea
    """
    descripcion =  models.TextField(null=True, blank=True)
    nombre = models.CharField(max_length = 100)
    tiempo = models.PositiveIntegerField()#
    #claves foraneas
    us = models.ForeignKey(UserStory)
    habilitado = models.BooleanField(default = True)
    def __unicode__(self):
                return self.nombre
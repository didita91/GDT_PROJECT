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
notificar= (( 'Si', 'Si'),
            )
""" Estados de Actividades """
status_activity = (
                 ('To Do', 'To Do'),
		         ('Doing', 'Doing'),
                 ('Done', 'Done'),
             )
cambio_estado = (
                 ('Done', 'Done'),

             )

"""Estados de los UserStories"""
STATUS_CHOICES = (
 	            ('En Espera', 'En Espera'),
 	            ('En Proceso', 'En Proceso'),
                ('Aprobado', 'Aprobado'),
                ('Inactivo', 'Inactivo')
                )
SPRINT_STATUS = (
                ('Preconfigurado', 'Preconfigurado'),
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
	"""
	Relación existente entre un usuario y su rol
	"""
	usuario =models.ForeignKey(User)
	def __unicode__(self):
		return self.usuario.username

class ProductOwner(models.Model):
    """
    Tabla que contiene el nombre del usuario Product Owner
    """
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
    estado=models.CharField(max_length=50,null=True)
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
    """
    Contiene datos del flujo
    """

    nombre = models.CharField( max_length=50)
    proyecto = models.ForeignKey(Proyecto)
    def __unicode__(self):
        return self.nombre


class Actividades(models.Model):
    """
    Contiene datos de las actividades
    """
    nombre = models.CharField( max_length=50)
    estado = models.CharField(max_length=10, default='-')
    proyecto = models.ForeignKey(Proyecto)

    def __unicode__(self):

        return self.nombre

class ActividadesFlujo(models.Model):
    """
    Contiene la relación entre flujo y actividades
    """
    actividades = models.ForeignKey(Actividades, null=True)
    flujo = models.ForeignKey(Flujo)
    proyecto = models.ForeignKey(Proyecto)
    ultimo= models.IntegerField(default=0)
    class Meta:
        unique_together = [("actividades", "flujo","proyecto")]
    def __unicode__(self):
        return self.actividades.nombre

#---------------------------CONFIGURACION DE SPRINT
class Equipo(models.Model):
    """
    Contiene datos de los equipos participantes del sprint
    """
    usuario = models.ForeignKey(UsuarioRolProyecto)
    horas = models.PositiveIntegerField()#horas de trabajo de ese miembro
    sprint = models.PositiveIntegerField()#sprint en el que se encuentra
    proyecto = models.ForeignKey(Proyecto)

    def __unicode__(self):
        return self.usuario.usuario
#***************************************USER STORY**********************************************
class UserStory(models.Model):
        """
        Contiene datos del user story
        """
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
        estado_actividad= models.CharField(max_length=10,default='-')
        hora_acumulada=models.IntegerField(max_length=2,null=True)
        tiempo=models.DateField(null=True)
        def __unicode__(self):
                return self.nombre



class ResponsableUS(models.Model):
    """
    Contiene datos del responsable del user story
    """
    usuario = models.ForeignKey(Equipo)
    us = models.ForeignKey(UserStory)
    def __unicode__(self):
        return unicode(self.usuario)

class flujoUS(models.Model):
    """
    Contiene relación entre flujo y user story
    """
    flujo=models.ForeignKey(Flujo)
    us = models.ForeignKey(UserStory)
    def __unicode__(self):
        return unicode(self.flujo)





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
    fecha= models.DateField()
    #claves foraneas
    us = models.ForeignKey(UserStory)
    fluactpro = models.ForeignKey(ActividadesFlujo)

    habilitado = models.BooleanField(default = True)

    def __unicode__(self):
                return self.nombre

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
    #tarea = models.ForeignKey(Tarea)
    documento=models.ForeignKey(Documento,null=True)
class Adjunto(models.Model):
    #archivo = models.FileField(upload_to='items')
    nombre = models.CharField(null=True,max_length = 100)
    contenido = models.TextField(null=True)
    tamano = models.IntegerField(null=True)
    mimetype = models.CharField(null=True,max_length = 255)
    #claves foraneas
    us = models.ForeignKey(UserStory,null=True)
    habilitado = models.BooleanField(default = True)

class RegistroHistorial(models.Model):
    """Clase que representa el Registro de tareas de los user stories"""
    #version = models.PositiveIntegerField()
    prioridad = models.IntegerField()
    descripcion = models.TextField(null=True, blank=True)
    habilitado = models.BooleanField()
    fecha_modificacion = models.DateTimeField(auto_now=True, auto_now_add=False, editable=False)
    #claves foraneas
    historial = models.ForeignKey(Historial)
    tarea=models.ForeignKey(Tarea)
    us= models.ForeignKey(UserStory)
    adjunto= models.ForeignKey(Adjunto,null=True)


class Sprint(models.Model):
    """ Clase de Sprint, tiene los campos: Estado, proyecto y nro. de sprint"""
    estado = models.CharField(max_length=10, choices=SPRINT_STATUS)
    proyecto = models.ForeignKey(Proyecto)
    nro_sprint=models.PositiveIntegerField()
    fecha_inicio= models.DateField(null=True)
    fecha_fin=models.DateField(null=True)
    duracion= models.PositiveIntegerField(null=True)
    disponibilidad= models.PositiveIntegerField(null=True)
    horastotales=models.PositiveIntegerField(null=True)


class Release(models.Model):
    us = models.ForeignKey(UserStory)
    def __unicode__(self):
                return self.us

class HistorialUS(models.Model):
    us= models.ForeignKey(UserStory)
    estado=  models.CharField(null=True,max_length = 100)

    flujo= models.ForeignKey(Flujo,null=True)

    actividad= models.ForeignKey(ActividadesFlujo,null=True)
    responsable= models.ForeignKey(User,null=True)
    estado_actividad=  models.CharField(null=True,max_length = 100)


    fecha = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True, editable=False)

    def __unicode__(self):
        return self.us

class UsSprint(models.Model):
    """
    Contiene datos de los user stories que se encuentran en un sprint
    """
    us=models.ForeignKey(UserStory)
    sprint=models.ForeignKey(Sprint)
    estado = models.CharField(max_length=10, choices=SPRINT_STATUS)
    proyecto=models.ForeignKey(Proyecto)
    def __unicode__(self):
        return unicode(self.us)

class Notificaciones(models.Model):
    activado = models.BooleanField()
    proyecto = models.ForeignKey(Proyecto)
    usuario = models.ForeignKey(User)

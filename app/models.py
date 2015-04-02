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
	class Meta:
		unique_together = [("usuario")]


class Proyecto(models.Model):
        nombre = models.CharField(unique=True, max_length=50)
        usuario_scrum = models.ForeignKey(RolUsuario)
        descripcion = models.TextField(null=True, blank= True)
        fecha_inicio = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
        def __unicode__(self):
                return self.nombre
class UsuarioRolProyecto(models.Model):
    usuario = models.ForeignKey(User)
    rol = models.ForeignKey(Rol, null=True)
    proyecto = models.ForeignKey(Proyecto)

    class Meta:
        unique_together = [("usuario", "rol", "proyecto")]

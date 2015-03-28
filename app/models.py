# -*- coding: iso-8859-15 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY_CHOICES = (
                 ('1', 'Rol de Sistema'),
                
             )    

COMPLEXITY_CHOICES = (
                      ('1', '1'),
                      ('2', '2'),
                      ('3', '3'),
                      ('4', '4'),
                      ('5', '5'),
                      ('6', '6'),
                      ('7', '7'),
                      ('8', '8'),
                      ('9', '9'),
                      ('10', '10'),
 	        )    
"""
    Contiene datos de permisos para cada usuario
    - nombre: nombre del permiso
    - categoria: se refiere al tipo de rol al que puede pertenecer, puede ser rol de sistema o rol de proyecto
"""
class Permiso(models.Model):
    nombre = models.CharField(unique=True, max_length = 50)
    categoria = models.IntegerField(max_length=1, choices=CATEGORY_CHOICES)
    
    def __unicode__(self):
        return self.nombre


"""
    Contiene datos de cada rol
    - nombre: nombre del permiso
    - categoria: puede ser de sistema o de proyecto
    - descripcion: informacion sobre el rol
    - fecHor_creacion: fecha y hora de creacion del rol
    - usuario_creador: usuario responsable de la creacion del rol
    - permisos: permisos admitidos para el rol
"""
class Rol(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    categoria = models.IntegerField(max_length=1, choices=CATEGORY_CHOICES)
    descripcion = models.TextField(null=True, blank=True)
    fecHor_creacion = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True, editable=False)
    usuario_creador = models.ForeignKey(User, null=True)
    permisos = models.ManyToManyField(Permiso, through='RolPermiso')
    
    def __unicode__(self):
        return self.nombre


"""
    Clasifica los permisos que pertenecen a rol sistema o rol proyecto
"""
class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol)
    permiso = models.ForeignKey(Permiso)


"""
    Tabla que contiene la lista de usuarios pertenecientes a cada rol
"""
class UsuarioRolSistema(models.Model):
    usuario = models.ForeignKey(User)
    rol = models.ForeignKey(Rol)
    
    class Meta:
        unique_together = [("usuario", "rol")]
        


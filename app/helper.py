from app.models import *
from datetime import datetime, timedelta
from django.core.mail.message import EmailMultiAlternatives
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.html import strip_tags

def get_permisos_sistema(user):
    roles = UsuarioRolSistema.objects.filter(usuario = user).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    return permisos

def get_permisos_proyecto(user, proyecto):
    roles = UsuarioRolProyecto.objects.filter(usuario = user, proyecto = proyecto)
    permisos_obj = []
    for i in roles:
       permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    return permisos
def registrar_historial_documento(user_story,documento):
    reg=Historial()
    reg.user_story=user_story
    reg.documento=documento
    reg.save()

def registrar_historial(user_story,historial,tarea,adjunto):
    """Se ingresa la version antigua al registro"""
    reg = RegistroHistorial()
    reg.version = 1
    reg.prioridad = user_story.prioridad
    reg.descripcion = tarea.descripcion
    reg.tarea=tarea
    reg.adjunto= adjunto
    #reg.descripcion_larga = itm.descripcion_larga
    reg.habilitado = user_story.habilitado
    reg.us = user_story
    #reg.tipo = itm.tipo
    #reg.fecha_modificacion = datetime.datetime.today()
    reg.historial = historial
    reg.save()
    user_story.save()           

def funcion_sprint(sprint):
    fecha_ini= datetime(sprint.fecha_inicio.year,sprint.fecha_inicio.month,sprint.fecha_inicio.day)
    fecha_fin= fecha_ini + timedelta(weeks=sprint.duracion) - timedelta(days=3)
    sprint.fecha_fin=fecha_fin
    sprint.save()




from app.models import *
import datetime

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

def registrar_historial(user_story,historial,tarea):
    """Se ingresa la version antigua al registro"""
    reg = RegistroHistorial()
    reg.version = 1
    reg.prioridad = user_story.prioridad
    reg.descripcion = tarea.descripcion
    #reg.descripcion_larga = itm.descripcion_larga
    reg.habilitado = user_story.habilitado
    reg.us = user_story
    #reg.tipo = itm.tipo
    #reg.fecha_modificacion = datetime.datetime.today()
    reg.historial = historial
    reg.save()
    user_story.save()           


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
    roles = UsuarioRolProyecto.objects.filter(usuario = user, proyecto = proyecto).only('rol')
    permisos_obj = []
   # for i in roles:
    #    permisos_obj.extend(i.rol.permisos.filter(rolpermiso__fase = proyecto.fase))
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    return permisos

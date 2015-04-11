__author__ = 'tere'
#-*- coding: utf-8 -*-
from django.conf.urls import *
from django.views.generic import *
from django.contrib.auth.models import User
from django.template import *
import os.path
from app.forms import *
from app.models import *
from app.views import *
from Proyecto.views import *
from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
	url(r'^proyectos/$', admin_proyectos),
	url(r'^proyectos/crear/$', crear_proyecto),
    url(r'^proyectos/mod&id=(?P<proyecto_id>\d+)/$', mod_proyecto),
    url(r'^proyectos/del&id=(?P<proyecto_id>\d+)/$', del_proyecto),
    url(r'^flujos/$', admin_flujos),

	url(r'^proyectos/admin&id=(?P<proyecto_id>\d+)/$', administrar_proyecto),
	url(r'^proyectos/miembros&id=(?P<proyecto_id>\d+)/$', admin_usuarios_proyecto),
    url(r'^proyectos/miembros&id=(?P<proyecto_id>\d+)/nuevo/$', add_usuario_proyecto),
	url(r'^proyectos/miembros&id=(?P<proyecto_id>\d+)/cambiar&id=(?P<user_id>\d+)/$', cambiar_rol_usuario_proyecto),
	url(r'^proyectos/miembros&id=(?P<proyecto_id>\d+)/del&id=(?P<user_id>\d+)/$', eliminar_miembro_proyecto),


)


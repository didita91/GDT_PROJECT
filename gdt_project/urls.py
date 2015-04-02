# -*- coding: utf-8 -*-
from django.conf.urls import *
from django.views.generic import *
from django.contrib.auth.models import User
from django.template import *
import os.path
from app.forms import *
from app.models import *
from app.views import *
from Proyecto.views import *
urlpatterns = patterns('',
    (r'^$', index_view),
    (r'^principal', principal),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/login/$', login_redirect),
    (r'^terminar/$', terminar),
    (r'^logout/$', logout_pagina),
    (r'^changepass/$', cambiar_password),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
       {'document_root': os.path.abspath('site_media')}),

    # usuarios
    (r'^usuarios/$', admin_usuarios),
    (r'^usuarios/crear/$', add_user),
    (r'^usuarios/mod&id=(?P<usuario_id>\d+)/$', mod_user),
    (r'^usuarios/rol&id=(?P<usuario_id>\d+)/$', asignar_roles_sistema),
    (r'^usuarios/del&id=(?P<usuario_id>\d+)/$', borrar_usuario),



    # roles
    (r'^roles/$', admin_roles),
    (r'^roles/sist/$',admin_roles_sist),
    (r'^roles/proy/$', admin_roles_proy),
    (r'^roles/crear/$', crear_rol),
    (r'^roles/mod&id=(?P<rol_id>\d+)/$', mod_rol),
    (r'^roles/permisos&id=(?P<rol_id>\d+)/$', admin_permisos),
    (r'^roles/del&id=(?P<rol_id>\d+)/$', borrar_rol),

    (r'^', include('Proyecto.urls')),

)




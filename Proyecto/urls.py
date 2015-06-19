
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
    url(r'^flujos&id=(?P<proyecto_id>\d+)/$', admin_flujos),
    url(r'^flujos&id=(?P<proyecto_id>\d+)/crear/$', crear_flujos),
    url(r'^flujos&id=(?P<proyecto_id>\d+)/crear_actividades/$', crear_actividades),
    url(r'^flujos&id=(?P<proyecto_id>\d+)/add_actividades&id=(?P<flujo_id>\d+)$', add_actividades),
    url(r'^flujos&id=(?P<proyecto_id>\d+)/ver_actividades&id=(?P<flujo_id>\d+)$', ver_actividades),
    url(r'^flujos&id=(?P<proyecto_id>\d+)/mod_actividades&id=(?P<acti_id>\d+)$', mod_actividades),
    url(r'^proyectos/admin&id=(?P<proyecto_id>\d+)/$', administrar_proyecto),
	url(r'^proyectos/miembros&id=(?P<proyecto_id>\d+)/$', admin_usuarios_proyecto),
    url(r'^proyectos/miembros&id=(?P<proyecto_id>\d+)/nuevo/$', add_usuario_proyecto),
	url(r'^proyectos/miembros&id=(?P<proyecto_id>\d+)/cambiar&id=(?P<user_id>\d+)/$', cambiar_rol_usuario_proyecto),
	url(r'^proyectos/miembros&id=(?P<proyecto_id>\d+)/del&id=(?P<user_id>\d+)/$', eliminar_miembro_proyecto),
 #USER STORIES
     url(r'^userstories&id=(?P<proyecto_id>\d+)/$', admin_us),
     url(r'^userstories&id=(?P<proyecto_id>\d+)/crear/$', crear_user_story),
     url(r'^userstories&id=(?P<proyecto_id>\d+)/mod_us&id=(?P<us_id>\d+)/$', mod_user_story),
#HISTORIAL
     url(r'^userstories&id=(?P<proyecto_id>\d+)/historial&id=(?P<us_id>\d+)/$',ver_historial),
#TAREA
     # url(r'^list/$', 'list', name='list'),0
     # url(r'^userstories&id=(?P<proyecto_id>\d+)/adj&id=(?P<us_id>\d+)/nuevo/$',list,name='list'),
     url(r'^userstories&id=(?P<proyecto_id>\d+)/adj&id=(?P<us_id>\d+)/nuevo/$',add_tarea),
#CONFIGURACION DE PROYECTO INICIO
     url(r'^configuracion&id=(?P<proyecto_id>\d+)/confsprint&id=(?P<sprint_id>\d+)$',conf_proyecto),

         url(r'^configuracion&id=(?P<proyecto_id>\d+)/sprint/$',conf_inicio_sprint),
             url(r'^configuracion&id=(?P<proyecto_id>\d+)/grafico/$',grafico),



     url(r'^configuracion/equipo&id=(?P<proyecto_id>\d+)/sprint&id=(?P<sprint_id>\d+)/$', admin_equipo),
     url(r'^configuracion/equipo&id=(?P<proyecto_id>\d+)/nuevo&id=(?P<sprint_id>\d+)/$',add_miembro_equipo),
     url(r'^configuracion/equipo&id=(?P<proyecto_id>\d+)/responsable&id=(?P<us_id>\d+)/sprint&id=(?P<sprint_id>\d+)$',responsable_us),
     url(r'^configuracion&id=(?P<proyecto_id>\d+)/flujo&id=(?P<us_id>\d+)/sprint&id=(?P<sprint_id>\d+)$',asignar_flujoUS),
     url(r'^configuracion&id=(?P<proyecto_id>\d+)/sprint&id=(?P<sprint_id>\d+)$',iniciarsprint),
         url(r'^configuracion&id=(?P<proyecto_id>\d+)/terminarsprint&id=(?P<sprint_id>\d+)$',terminarsprint),
         url(r'^configuracion&id=(?P<proyecto_id>\d+)/prolongarsprint&id=(?P<sprint_id>\d+)$',prolongarsprint),
         url(r'^configuracion&id=(?P<proyecto_id>\d+)/cancelarproyecto$',cancelar_proyecto),
             url(r'^configuracion&id=(?P<proyecto_id>\d+)/finalizarproyecto$', finalizar_proyecto),
    #REPORTES
  url(r'^proyectos/admin&id=(?P<proyecto_id>\d+)/reporte/$',generar_reporte),


        url(r'^configuracion&id=(?P<proyecto_id>\d+)/flujouser/$',flujo_user_sprint),
    #HISTORIAL
     url(r'^userstories&id=(?P<proyecto_id>\d+)/historial&id=(?P<us_id>\d+)/$',ver_historial),
         url(r'^userstories&id=(?P<proyecto_id>\d+)/historialrelease&id=(?P<us_id>\d+)/$',ver_historial_release),

            url(r'^configuracion&id=(?P<proyecto_id>\d+)/act_cambiar&id=(?P<act_id>\d+)/us&id=(?P<us_id>\d+)/flujo&id=(?P<flujo_id>\d+)/$',cambiar_actividad),

        url(r'^configuracion&id=(?P<proyecto_id>\d+)/estado_cambiar&id=(?P<act_id>\d+)/us&id=(?P<us_id>\d+)/flujo&id=(?P<flujo_id>\d+)/$',cambiar_estado),

     url(r'^configuracion&id=(?P<proyecto_id>\d+)/cambiarhoraestimada&id=(?P<us_id>\d+)/sprint&id=(?P<sprint_id>\d+)$',cambiar_hora_estimada),
        url(r'^configuracion&id=(?P<proyecto_id>\d+)/act_flujo&id=(?P<flujo_id>\d+)/us&id=(?P<us_id>\d+)/$',actividad_flujo),
#url(r'^userstories&id=(?P<proyecto_id>\d+)/adjunto&id=(?P<us_id>\d+)/$',add_adjunto),
    url(r'^sprint&id=(?P<proyecto_id>\d+)/$',sprint_admin),
        url(r'^userstories&id=(?P<proyecto_id>\d+)/backlog/$',us_backlog),
     url(r'^configuracion&id=(?P<proyecto_id>\d+)/sprint_bk/$',sprint_bk),
         url(r'^configuracion&id=(?P<proyecto_id>\d+)/tablero/$',ver_tablero),

         url(r'^configuracion&id=(?P<proyecto_id>\d+)/sprint_bk&id=(?P<sprint_id>\d+)/us/$',sprint_us),
             url(r'^configuracion&id=(?P<proyecto_id>\d+)/enviararelease&id=(?P<us_id>\d+)/$',enviar_a_release),
                url(r'^configuracion&id=(?P<proyecto_id>\d+)/release/$',release),
                    url(r'^configuracion&id=(?P<proyecto_id>\d+)/revisarus&id=(?P<us_id>\d+)/$',revisar_us),


             url(r'^configuracion&id=(?P<proyecto_id>\d+)/cambiaractividad&id=(?P<us_id>\d+)/flujo&id=(?P<flujo_id>\d+)/actividad&id=(?P<act_id>\d+)/$',recambiar_actividad),


            url(r'^configuracion&id=(?P<proyecto_id>\d+)/addussprint&id=(?P<us_id>\d+)/sprint&id=(?P<sprint_id>\d+)$',add_us_sprint),

     url(r'^configuracion&id=(?P<proyecto_id>\d+)/historialus&id=(?P<us_id>\d+)/$',ver_historial_us),

  url(r'^userstories&id=(?P<proyecto_id>\d+)/adj&id=(?P<us_id>\d+)/$',admin_adjuntos),
    url(r'^userstories&id=(?P<proyecto_id>\d+)/adj&id=(?P<us_id>\d+)/nuevoadjunto/$',add_adjunto),

    url(r'^userstories&id=(?P<proyecto_id>\d+)/adj&id=(?P<us_id>\d+)/get&id=(?P<arch_id>\d+)/$',retornar_archivo),

   url (r'^userstories&id=(?P<proyecto_id>\d+)/adj&id=(?P<us_id>\d+)/quitar&id=(?P<arch_id>\d+)/$',quitar_archivo),
       url (r'^userstories&id=(?P<proyecto_id>\d+)/cancelar&id=(?P<us_id>\d+)/$',cancelar_us),
           url (r'^configuracion&id=(?P<proyecto_id>\d+)/activar$',activarNotif),
               url (r'^configuracion&id=(?P<proyecto_id>\d+)/desactivar$',desactivarNotif),


      url(r'^configuracion&id=(?P<proyecto_id>\d+)/grafico/sprint&id=(?P<sprint_id>\d+)/$',plot)



)



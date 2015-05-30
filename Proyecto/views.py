"""VIEWS DE FUNCIONALIDADES DEL PROYECTO"""
# -*- coding: utf-8 -*-
import base64
import os
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import logout
from django.template import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib import *
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.forms.formsets import formset_factory
from django.shortcuts import render
from app.forms import *
from app.models import *
from app.helper import *
from django.core.mail.message import EmailMultiAlternatives
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.html import strip_tags
#from matplotlib import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
#from somewhere import handle_uploaded_file
# Create your views here.

@login_required
def admin_proyectos(request):
    """
	Administracion general de proyectos
	:param request:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    lista = Proyecto.objects.all().order_by('id')
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            palabra = form.cleaned_data['filtro']
            lista = Proyecto.objects.filter(Q(nombre__icontains=palabra) | Q(descripcion__icontains=palabra) | Q(
                usuario_scrum__username__icontains=palabra)).order_by('id')
            paginas = form.cleaned_data['paginas']
            request.session['nro_items'] = paginas
            paginator = Paginator(lista, int(paginas))
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                pag = paginator.page(page)
            except (EmptyPage, InvalidPage):
                pag = paginator.page(paginator.num_pages)
            return render_to_response('admin/proyectos/proyectos.html', {'lista': lista, 'pag': pag, 'form': form,
                                                                         'user': user,
                                                                         'ver_proyectos': 'Ver proyectos' in permisos,
                                                                         'crear_proyecto': 'Crear proyecto' in permisos,
                                                                         'mod_proyecto': 'Modificar proyecto' in permisos,
                                                                         'ver_flujos': 'Ver flujos' in permisos,
                                                                         'eliminar_proyecto': 'Eliminar proyecto' in permisos},
                                      context_instance=RequestContext(request))
    else:
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        if not 'nro_items' in request.session:
            request.session['nro_items'] = 5
        paginas = request.session['nro_items']
        paginator = Paginator(lista, int(paginas))
        try:
            pag = paginator.page(page)
        except (EmptyPage, InvalidPage):
            pag = paginator.page(paginator.num_pages)
        form = FilterForm(initial={'paginas': paginas})
        return render_to_response('admin/proyectos/proyectos.html', {'lista': lista, 'pag': pag, 'form': form,
                                                                     'user': user,
                                                                     'ver_proyectos': 'Ver proyectos' in permisos,
                                                                     'crear_proyecto': 'Crear proyecto' in permisos,
                                                                     'mod_proyecto': 'Modificar proyecto' in permisos,
                                                                     'ver_flujos': 'Ver flujos' in permisos,
                                                                     'eliminar_proyecto': 'Eliminar proyecto' in permisos},
                                  context_instance=RequestContext(request))


@login_required
def crear_proyecto(request):
    """
	Crear un nuevo proyecto.
	:param request:
	:return:
    """

    user = User.objects.get(username=request.user.username)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolSistema.objects.filter(usuario=user).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    #-------------------------------------------------------------------
    if request.method == 'POST':
        form = ProyectosForm(request.POST, request.FILES)
        if form.is_valid():
            p = Proyecto()
            p.nombre = form.cleaned_data['nombre']
            p.usuario_scrum = form.cleaned_data['usuario_scrum']
           # p.product_owner = form.cleaned_data['product_owner']
            p.descripcion = form.cleaned_data['descripcion']
            p.fecha_inicio = form.cleaned_data['fecha_inicio']
            p.save()
            relacion = UsuarioRolProyecto()
            relacion.usuario = p.usuario_scrum.usuario
            relacion.rol = Rol.objects.get(id=2)
            #rel = UsuarioRolProyecto()
            #rel.usuario= p.product_owner.usuario
            #rel.rol=Rol.objects.get(id=5)
            #rel.save()

            print relacion.rol
            print "chauuu"
            relacion.proyecto = p
            relacion.save()


        return HttpResponseRedirect('/proyectos')
    else:
        form = ProyectosForm()
        return render_to_response('admin/proyectos/crear_proyecto.html',
                                  {'form': form, 'user': user, 'crear_proyecto': 'Crear proyecto' in permisos},
                                  context_instance=RequestContext(request))


@login_required
def del_proyecto(request, proyecto_id):
    """
	Eliminación de un proyecto del sistema
	:param request:
	:param proyecto_id:
	:return:
    """

    user = User.objects.get(username=request.user.username)
    p = get_object_or_404(Proyecto, id=proyecto_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolSistema.objects.filter(usuario=user).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    #-------------------------------------------------------------------
    if request.method == 'POST':
        p.delete()
        return HttpResponseRedirect("/proyectos")
    else:
        return render_to_response("admin/proyectos/proyecto_confirm_delete.html", {'proyecto': p,
                                                                                   'eliminar_proyecto': 'Eliminar proyecto' in permisos},
                                  context_instance=RequestContext(request))


'''
@login_required
def add_usuario_proyecto(request, object_id):
    user = User.objects.get(username=request.user.username)
    p = get_object_or_404(Proyecto, id = object_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario = user, proyecto = p).only('rol')
    usuario = UsuarioRolProyecto.objects.filter(usuario = user, proyecto = p)
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos

    #-------------------------------------------------------------------
    if request.method == 'POST':
        form = UsuarioProyectoForm(p, request.POST)
        if form.is_valid():
            relacion = UsuarioRolProyecto()
            relacion.usuario = form.cleaned_data['usuario']
            relacion.proyecto = Proyecto.objects.get(pk = object_id)
            relacion.save()

            return HttpResponseRedirect("/proyectos/miembros&id=" + str(object_id))
    else:
        form = UsuarioProyectoForm(p)
    return render_to_response('desarrollo/add_miembro.html', {'form':form,
                                                              'user':user,
                                                              'proyecto': p,
                                                              'abm_miembros': 'ABM miembros' in permisos},context_instance=RequestContext(request))'''


@login_required
def administrar_proyecto(request, proyecto_id):
    """
    Administración de proyecto: flujos, user story, miembros.
    :param request:
    :param proyecto_id:
	:return:
    """

    user = User.objects.get(username=request.user.username)
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    permisos = get_permisos_sistema(user)
    perm = get_permisos_proyecto(user, proyecto)
    print perm
    print "tototo"
    print proyecto
    print user
    print permisos

    """ spt =Sprint.objects.get(proyecto=proyecto.id,fecha_inicio=None)
    sprint =1

    if spt.estado == '0':
          sprint=0"""
    return render_to_response("desarrollo/admin_proyecto.html", {'proyecto': proyecto,
                                                                 'user': user,
                                                                 #  'fin':linea,
                                                                 'ver_flujos': 'Ver flujos' in permisos,
                                                                 'ver_user_story': 'Ver user story' in permisos,
                                                                  'ver_us': 'Ver US' in perm,
                                                                 'Ver_Flujos': 'Ver Flujos' in perm,
                                                                 'Ver_Miembros': 'Ver Miembros' in perm,
                                                                 'ver_miembros': 'Ver miembros' in permisos,
                                                                 'abm_miembros': 'ABM miembros' in permisos,
                                                                 'asignar_roles': 'Asignar roles' in permisos,
                                                                 'generarlb': 'Generar LB',
                                                                 'asignar_tipoItm': 'Asignar tipo-item fase'},
                              context_instance=RequestContext(request))

    return render_to_response("desarrollo/admin_proyecto.html", {'sprint':sprint,'proyecto': proyecto,
                                                                 'user': user,
                                                                 #  'fin':linea,
                                                                 'ver_flujos': 'Ver flujos' in permisos,
                                                                 'ver_user_story': 'Ver user story' in permisos,
                                                                  'ver_us': 'Ver US' in perm,
                                                                 'Ver_Flujos': 'Ver Flujos' in perm,
                                                                 'Ver_Miembros': 'Ver Miembros' in perm,
                                                                 'ver_miembros': 'Ver miembros' in permisos,
                                                                 'abm_miembros': 'ABM miembros' in permisos,
                                                                 'asignar_roles': 'Asignar roles' in permisos,
                                                                 'generarlb': 'Generar LB',
                                                                 'asignar_tipoItm': 'Asignar tipo-item fase'},
                              context_instance=RequestContext(request))


@login_required
def admin_usuarios_proyecto(request, proyecto_id):
    """
    Administración de usuarios del proyecto: ver miembros.
	:param request:
	:param proyecto_id:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    p = Proyecto.objects.get(pk=proyecto_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=p).only('rol')
    permisos_obj = []
    perm = get_permisos_proyecto(user,p)
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    #-------------------------------------------------------------------
    miembros = UsuarioRolProyecto.objects.filter(proyecto=p).order_by('id')
    lista = []
    roles = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=p).only('rol')
    usuario = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=p)
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos

    #-------------------------------------------------------------------
    if request.method == 'POST':
        form = UsuarioProyectoForm(p,request.POST)
        if form.is_valid():
            relacion = UsuarioRolProyecto()
            relacion.usuario = form.cleaned_data['usuario']
            relacion.proyecto = Proyecto.objects.get(pk=proyecto_id)
            relacion.save()
            return HttpResponseRedirect("/proyectos/miembros&id=" + str(proyecto_id))
    for i in miembros:
        if not i.usuario in lista:
            lista.append(i.usuario)
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            palabra = form.cleaned_data['filtro']
            lista = User.objects.filter(Q(username__icontains=palabra) | Q(first_name__icontains=palabra) | Q(
                last_name__icontains=palabra)).order_by('id')
            paginas = form.cleaned_data['paginas']
            request.session['nro_items'] = paginas
            paginator = Paginator(lista, int(paginas))
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                pag = paginator.page(page)
            except (EmptyPage, InvalidPage):
                pag = paginator.page(paginator.num_pages)
            return render_to_response('desarrollo/admin_miembros.html', {'form':form,'lista': lista, 'pag': pag, 'form': form,
                                                                         'user': user,
                                                                         'proyecto': Proyecto.objects.get(
                                                                             id=proyecto_id),
                                                                         'miembros': lista,
                                                                         'Ver_Miembros':'Ver Miembros' in perm,
                                                                         'ver_miembros': 'Ver miembros' in permisos,
                                                                         'abm_miembros': 'ABM miembros' in permisos},
                                      context_instance=RequestContext(request))
    else:
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        if not 'nro_items' in request.session:
            request.session['nro_items'] = 5
        paginas = request.session['nro_items']
        paginator = Paginator(lista, int(paginas))
        try:
            pag = paginator.page(page)
        except (EmptyPage, InvalidPage):
            pag = paginator.page(paginator.num_pages)
        form2 = FilterForm(initial={'paginas': paginas})
        form = UsuarioProyectoForm(p,request.POST)

        return render_to_response('desarrollo/admin_miembros.html', {'form':form,'lista': lista, 'pag': pag, 'form': form,
                                                                     'user': user,
                                                                     'proyecto': Proyecto.objects.get(id=proyecto_id),
                                                                     'miembros': lista,
                                                                     'Ver_Miembros':'Ver Miembros' in perm,
                                                                     'ver_miembros': 'Ver miembros' in permisos,
                                                                     'abm_miembros': 'ABM miembros' in permisos},
                                  context_instance=RequestContext(request))


@login_required
def add_usuario_proyecto(request, proyecto_id):
    """
    Agregar usuarios a un proyecto.
    :param request:
    :param proyecto_id:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    p = get_object_or_404(Proyecto, id=proyecto_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=p).only('rol')
    usuario = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=p)
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos

    #-------------------------------------------------------------------
    if request.method == 'POST':
        form = UsuarioProyectoForm(p,request.POST)
        if form.is_valid():
            relacion = UsuarioRolProyecto()
            relacion.usuario = form.cleaned_data['usuario']
            relacion.proyecto = Proyecto.objects.get(pk=proyecto_id)

            relacion.save()
            return HttpResponseRedirect("/proyectos/miembros&id=" + str(proyecto_id))
    else:
        form = UsuarioProyectoForm(p)
    return render_to_response('desarrollo/add_miembro.html', {'form': form,
                                                              'user': user,
                                                              'proyecto': p,
                                                              'abm_miembros': 'ABM miembros' in permisos,
                                                              'asignar_roles': 'Asignar roles'},
                              context_instance=RequestContext(request))


@login_required
def cambiar_rol_usuario_proyecto(request, proyecto_id, user_id):
    """
    Cambiar rol a un usuario del proyecto.
    :param request:
    :param proyecto_id:
    :param user_id:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    p = Proyecto.objects.get(pk=proyecto_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=p).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    #-------------------------------------------------------------------
    u = User.objects.get(pk=user_id)
    lista = UsuarioRolProyecto.objects.filter(proyecto=p, usuario=u)
    if request.method == 'POST':
        form = AsignarRolesForm(2, request.POST)
        if form.is_valid():
            for i in lista:
                i.delete()
            lista_nueva = form.cleaned_data['roles']
            if lista_nueva:
                for i in lista_nueva:
                    nuevo = UsuarioRolProyecto()
                    nuevo.usuario = u
                    nuevo.proyecto = p
                    nuevo.rol = i
                    nuevo.save()
            else:
                nuevo = UsuarioRolProyecto()
                nuevo.usuario = u
                nuevo.proyecto = p
                nuevo.rol = None
                nuevo.save()
            return HttpResponseRedirect("/proyectos/miembros&id=" + str(proyecto_id))
    else:
        if len(lista) == 1 and not lista[0].rol:
            form = AsignarRolesForm(2)
        else:
            dict = {}
            for i in lista:
                dict[i.rol] = True
            form = AsignarRolesForm(2, initial={'roles': dict})
    return render_to_response("desarrollo/cambiar_usuario_rol.html", {'user': user,
                                                                      'form': form,
                                                                      'usuario': u,
                                                                      'proyecto': p,

                                                                      'asignar_roles': 'Asignar roles' in permisos,
                                                                      'abm_miembros': 'ABM miembros' in permisos},
                              context_instance=RequestContext(request))


@login_required
def eliminar_miembro_proyecto(request, proyecto_id, user_id):
    """
    Eliminar miembro o usuario de un proyecto.
    :param request:
    :param proyecto_id:
	:param user_id:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    usuario = get_object_or_404(User, pk=user_id)
    proy = get_object_or_404(Proyecto, pk=proyecto_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=proy).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    #-------------------------------------------------------------------
    if request.method == 'POST':
        lista = UsuarioRolProyecto.objects.filter(proyecto=proy, usuario=usuario)
        for i in lista:
            i.delete()
        return HttpResponseRedirect("/proyectos/miembros&id=" + str(proyecto_id))
    else:
        return render_to_response("desarrollo/eliminar_miembro.html", {'usuario': usuario,
                                                                       'proyecto': proy,
                                                                       'user': user,
                                                                       'abm_miembros': 'ABM miembros' in permisos},
                                  context_instance=RequestContext(request))


@login_required
def mod_proyecto(request, proyecto_id):
    """
    Modificación de datos de un Proyecto.
    :param request:
    :param proyecto_id:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    p = get_object_or_404(Proyecto, id=proyecto_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolSistema.objects.filter(usuario=user).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    #-------------------------------------------------------------------
    if request.method == 'POST':
        form = ModProyectosForm(p, request.POST, request.FILES)
        if form.is_valid():
            p.nombre = form.cleaned_data['nombre']

            relacion = UsuarioRolProyecto.objects.filter(usuario=User.objects.get(pk=p.usuario_scrum.usuario_id),
                                                         proyecto=p, rol=Rol.objects.get(pk=2))
            relacion.delete()
            relacion = UsuarioRolProyecto()
            relacion.usuario = p.usuario_scrum.usuario
            relacion.rol = Rol.objects.get(id=2)

            relacion.proyecto = p
            relacion.save()

            p.descripcion = form.cleaned_data['descripcion']
            #p.fecha_inicio = form.cleaned_data['fecha_inicio']
            p.save()
            return HttpResponseRedirect('/proyectos')
    else:
        form = ModProyectosForm(p, initial={'nombre': p.nombre,

                                            'descripcion': p.descripcion,
                                            })
    return render_to_response('admin/proyectos/mod_proyecto.html', {'form': form,
                                                                    'user': user,
                                                                    'proyecto': p,
                                                                    'mod_proyecto': 'Modificar proyecto' in permisos},
                              context_instance=RequestContext(request))


@login_required
def admin_flujos(request, proyecto_id):
    """
    Administracion de flujos y actividades de un proyecto
	:param request:
	:param proyecto_id:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    proyectos = Proyecto.objects.get(id=proyecto_id)
    permisos = get_permisos_sistema(user)
    perm = get_permisos_proyecto(user,proyectos)
    print user
    print permisos
    lista = Flujo.objects.filter(proyecto=proyectos)
    actividades = Actividades.objects.filter(proyecto=proyecto_id)
    print actividades
    return render_to_response("flujo/admin_flujo.html", {
        'user': user, 'lista': lista, 'proyecto': proyectos, 'actividades': actividades,
        'mod_acti': 'Modificar actividad' in permisos, 'ver_flujos': 'Ver flujos' in permisos,
        'crear_flujos': 'Crear flujos' in permisos, 'ver_actividades': 'Ver actividades' in permisos,
        'crear_actividades': 'Crear actividades' in permisos,'Ver_Actividades':'Ver Actividades' in perm,
        'Ver_Flujos':'Ver Flujos' in perm,

    }, context_instance=RequestContext(request))


@login_required
def crear_flujos(request,proyecto_id):
    """
    Creación de un nuevo flujo.
    :param request:
    :return:
    """
    proyecto=Proyecto.objects.get(id=proyecto_id)
    user = User.objects.get(username=request.user.username)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolSistema.objects.filter(usuario = user).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    #-------------------------------------------------------------------
    if request.method == 'POST':
        form = FlujosForm(request.POST)
        if form.is_valid():
            p = Flujo()
            p.nombre = form.cleaned_data['nombre']
            p.proyecto=proyecto
            p.save()
            return HttpResponseRedirect("/flujos&id="+str(proyecto_id))
    else:
        form = FlujosForm()
    return render_to_response('flujo/crear_flujo.html',{'form':form,
                                                            'user':user,'proyecto':proyecto,
                                                            'crear_flujos': 'Crear flujos' in permisos},context_instance=RequestContext(request))

@login_required
def crear_actividades(request,proyecto_id):
    """
    Creación de una nueva actividad en el proyecto
	:param request:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolSistema.objects.filter(usuario = user).only('rol')
    proyecto= Proyecto.objects.get(id=proyecto_id)
    perm = get_permisos_proyecto(user,proyecto)
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    print proyecto.id
    #-------------------------------------------------------------------
    if request.method == 'POST':
        form = ActividadesForm(request.POST)
        if form.is_valid():
            p = Actividades()

            p.nombre = form.cleaned_data['nombre']
            p.proyecto = proyecto

            p.save()

            return HttpResponseRedirect("/flujos&id="+str(proyecto_id))
    else:
        form =ActividadesForm()
    return render_to_response('flujo/crear_actividades.html',{'form':form,'proyecto':proyecto,
                                                            'user':user,
                                                            'crear_actividades': 'Crear actividades' in permisos},context_instance=RequestContext(request))
@login_required
def add_actividades(request, proyecto_id, flujo_id):
    """
    Adherir actividades existentes a flujos existentes.
	:param request:
	:param proyecto_id:
	:param flujo_id:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    flujo = Flujo.objects.get(id=flujo_id)
    permisos = get_permisos_sistema(user)

    proyecto = Proyecto.objects.get(id=proyecto_id)
    perm = get_permisos_proyecto(user, proyecto)
    #lista_roles = UsuarioRolSistema.objects.filter(usuario=usuario)
    lista_actividades = ActividadesFlujo.objects.filter(proyecto=proyecto)
    lista_permisos = RolPermiso.objects.filter()
    print request.method
    print lista_permisos
    tam = len(lista_permisos)
    print tam
    ultimo =0
    if request.method == 'POST':
        form = AddActividadesForm(proyecto, request.POST)
        print "ktkkk"
        if form.is_valid():
            lista_nueva = form.cleaned_data['actividades']
            #for i in lista_actividades:
             #  i.delete()
            long= len(lista_nueva)
            print "chau"
            for j in lista_nueva:
                nuevo = ActividadesFlujo()
                nuevo.flujo = flujo
                nuevo.actividades = j
                nuevo.proyecto = proyecto
                print "holaaa"
                if j == lista_nueva[(long-1)]:
                    nuevo.ultimo=1
                nuevo.save()
            return HttpResponseRedirect("/flujos&id=" + str(proyecto_id))
    else:
        print "chauuuuuuuuuuu"
        dict = {}
        for i in lista_actividades:
            dict[i.actividades] = True
        form = AddActividadesForm(proyecto, initial={'actividades': dict})
    return render_to_response("flujo/add_actividades.html",
                              {'form': form, 'user': user, 'flujo': flujo, 'proyecto': proyecto,
                               'add_actividades': 'Agregar Actividades' in perm},
                              context_instance=RequestContext(request))


@login_required
def ver_actividades(request, proyecto_id, flujo_id):
    """
    Visualizar las actividades existentes en un proyecto.
    :param request:
    :param proyecto_id:
    :param flujo_id:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    flujo = get_object_or_404(Flujo, id=flujo_id)
    actividades = ActividadesFlujo.objects.filter(flujo=flujo)
    permisos = get_permisos_sistema(user)
    perm = get_permisos_proyecto(user, proyecto)
    print proyecto
    print user
    print actividades

    return render_to_response("flujo/ver_actividades.html",
                              {'proyecto': proyecto, 'actividades': actividades, 'flujo': flujo,
                               'user': user,
                               #  'fin':linea,
                               'ver_flujos': 'Ver flujos' in permisos,
                               'ver_actividades': 'Ver actividades' in permisos,
                               'ver_Actividades': 'Ver Actividades' in perm,
                               'ver_miembros': 'Ver miembros' in permisos,
                               'abm_miembros': 'ABM miembros' in permisos,
                               'asignar_roles': 'Asignar roles' in permisos,
                               'generarlb': 'Generar LB',
                               'asignar_tipoItm': 'Asignar tipo-item fase'}, context_instance=RequestContext(request))


#*****************************************USER STORY******************************************************************
@login_required
def admin_us(request, proyecto_id):
    """
    Administracion de user stories.
    :param request:
    :param proyecto_id:
    :return:
    """
    print "proyectooooo"
    print proyecto_id
    user = User.objects.get(username=request.user.username)
    proyecto= get_object_or_404(Proyecto, id = proyecto_id)
    print proyecto
    #proyecto = Proyecto.objects.get(pk=proyecto_id)
    #linea = LineaBase.objects.filter(proyectos=proyect, fase=proyect.fase)
    perm = get_permisos_proyecto(user, proyecto)
    permisos = get_permisos_sistema(user)
    lista = UserStory.objects.filter(habilitado=True,proyecto=proyecto.id).order_by('id')
    print permisos
    print "holaaa"
    print perm
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            palabra = form.cleaned_data['filtro']
            lista = UserStory.objects.filter(Q(nombre__icontains=palabra)).order_by('id')
            paginas = form.cleaned_data['paginas']
            request.session['nro_items'] = paginas
            paginator = Paginator(lista, int(paginas))
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                pag = paginator.page(page)
            except (EmptyPage, InvalidPage):
                pag = paginator.page(paginator.num_pages)
            #for i in proyecto:
            variables = RequestContext(request, {'proyecto': proyecto, 'lista': lista, 'pag': pag, 'form': form,
                                                 'lista': lista, 'mod_user_story': 'Modificar us' in permisos,
                                                 'mod_us': 'Modificar US' in perm,
                                                 'abm_user_story': 'ABM user story' in permisos,
                                                 'ver_user_story': 'Ver user story' in permisos,
                                                 'ver_us': 'Ver US' in perm,
                                                 'Crear_US': 'Crear US' in perm,
                                                 'revisar_user_story': 'Revisar user story'})
            return render_to_response('us/user_story.html', variables)

    else:
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        if not 'nro_items' in request.session:
            request.session['nro_items'] = 5
        paginas = request.session['nro_items']
        paginator = Paginator(lista, int(paginas))
        try:
            pag = paginator.page(page)
        except (EmptyPage, InvalidPage):
            pag = paginator.page(paginator.num_pages)
        form = FilterForm(initial={'paginas': paginas})
        #for i in proyecto:
        variables = RequestContext(request, {'proyecto': proyecto, 'lista': lista, 'pag': pag, 'form': form,
                                             'lista': lista, 'mod_user_story': 'Modificar us' in permisos,
                                             'mod_us': 'Modificar US' in perm,
                                             'abm_user_story': 'ABM user story' in permisos,
                                             'ver_user_story': 'Ver user story' in permisos,
                                             'ver_us': 'Ver US' in perm,
                                             'Crear_US': 'Crear US' in perm,
                                             'revisar_user_story': 'Revisar user story'})
        return render_to_response('us/user_story.html', variables)

@login_required
def crear_user_story(request,proyecto_id):
    """
    Creación de un nuevo user story en un proyecto.
	:param request:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolSistema.objects.filter(usuario = user).only('rol')
    proyecto =Proyecto.objects.get(id=proyecto_id)
    permisos_obj = []
    perm = get_permisos_proyecto(user,proyecto)


    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    #-------------------------------------------------------------------
    if request.method == 'POST':
        form = UserStoryForm(request.POST)

        if form.is_valid():
            us = UserStory()
            us.nombre = form.cleaned_data['nombre']
            #us.usuario = form.cleaned_data['usuario']  #solo en el historial?

            us.estado = "En Espera"
            us.version = 1
            us.valor_negocio=form.cleaned_data['valor_negocio']
            us.valor_tecnico=form.cleaned_data['valor_tecnico']
            us.prioridad = form.cleaned_data['prioridad']
            us.descripcion = form.cleaned_data['descripcion']
            us.habilitado = True
            us.proyecto = proyecto
            duracion = form.cleaned_data['duracion']
            us.duracion = duracion*5
            us.estado_actividad='To Do'
            us.hora_acumulada=0
            us.save()
            histus = HistorialUS()
            histus.us = us
            histus.estado= us.estado
            histus.actividad= us.actividad
            histus.estado_actividad =us.estado_actividad
            histus.flujo = us.flujo
            histus.responsable = us.responsable
            histus.fecha = datetime.today()
            histus.save()
            print "pruebaa"
            print us.estado

            #Generacion del historial
            hist = Historial()
            hist.usuario = user
            hist.fecha_creacion = datetime.today()
            hist.user_story = us
            hist.save()
            return HttpResponseRedirect("/userstories&id=" + str(proyecto_id) + "/")
    else:
        form = UserStoryForm()
    return render_to_response('us/crear_user_story.html',{'proyecto': proyecto,
            'form': form,
            'abm_user_story': 'ABM user story' in permisos,
            'crear_us': 'Crear US' in perm},context_instance=RequestContext(request))




def cambiar_hora_estimada(request, proyecto_id,us_id,sprint_id):
    """ Cambia la hora estimada de un user story
    :param request:
    :param proyecto_id:
    :param us_id:
    :param sprint_id:
    :return:
    """
    proyect = get_object_or_404(Proyecto, id=proyecto_id)
    us = UserStory.objects.get(id=us_id)
    sprint = Sprint.objects.get(id= sprint_id)
        # Handle file upload
    if request.method == 'POST':
        form = duracionEstimadaForm(request.POST)
        if form.is_valid():
            us.duracion = form.cleaned_data["duracion"]
            us.save()
            return HttpResponseRedirect("/configuracion&id="+ str(proyect.id)+"/confsprint&id="+str(sprint_id))
    else:
        form =duracionEstimadaForm(
            initial={'duracion': us.duracion})
    # Render list page with the documents and the form
    return render_to_response(
        'us/cambiar_hora_estimada.html',
        {'us': us, 'form': form,'proyecto':proyect,'sprint':sprint},
        context_instance=RequestContext(request)
    )

"""@login_required
def ver_historial(request, proyecto_id, us_id):
    
    print "chaaaaaaaaaaaaaaaaa"
    us = UserStory.objects.get(pk=us_id)
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    perm = get_permisos_proyecto(user, proyecto)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=proyecto).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    #-------------------------------------------------------------------
    historial = Historial.objects.get(user_story=us)
    versiones = RegistroHistorial.objects.filter(us=us).order_by('version')
    print versiones.descripcion
    print "hadfakjfld"
    #linea = LineaBase.objects.filter(proyectos=proyect, fase=3)
    #if (linea):
    fin = 0
    #else:
    #    fin = 1
    variables = RequestContext(request, {'historial': historial,
                                         'lista': versiones,
                                         'user_story': us,
                                         'fin': fin,
                                         'proyecto': proyecto,
                                         'ver_historial_user_story': 'Ver historial' in permisos,
                                         'ver_historial_us': 'Ver Historial'})
    return render_to_response('us/historial.html', variables)

"""

@login_required
def mod_user_story(request, proyecto_id, us_id):
    """
    Permite modificar los datos de un user story existente en un proyecto.
    :param request:
    :param proyecto_id:
    :param us_id:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    perm = get_permisos_proyecto(user, proyecto)
    #Validacion de permisos----------------------------------------------
    roles = UsuarioRolSistema.objects.filter(usuario=user).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    #--------------------------------------------------------------------
    us = get_object_or_404(UserStory, id=us_id)
    print perm
    print "holaaaaaaaaaaaaaa"
    print permisos
    #Datos nuevos del user story
    if request.method == 'POST':
        form = ModUserStoryForm(request.POST)
        if form.is_valid():
            us.nombre = form.cleaned_data['nombre']
            us.descripcion = form.cleaned_data['descripcion']
            us.save()
            return HttpResponseRedirect("/userstories&id=" + str(proyecto_id))
    else:
        form = ModUserStoryForm(
            initial={'nombre': us.nombre, 'descripcion': us.descripcion})
    return render_to_response('us/mod_us.html', {'form': form,
                                                 'proyecto': proyecto,
                                                 'us': us,
                                                 'mod_us': 'Modificar US' in perm,
                                                 'mod_user_story': 'Modificar us' in permisos},
                              context_instance=RequestContext(request))


@login_required
def mod_actividades(request, proyecto_id, acti_id):
    """
    Permite modificar los datos de una actividad y los actualiza en el sistema
    :param request:
    :param proyecto_id:
    :param acti_id:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    #flujo = Flujo.objects.get(pk=flujo_id)
    perm = get_permisos_proyecto(user, proyecto)
    #Validacion de permisos----------------------------------------------
    roles = UsuarioRolSistema.objects.filter(usuario=user).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    #--------------------------------------------------------------------
    acti = get_object_or_404(Actividades, id=acti_id)
    print perm
    print "holaaaaaaaaaaaaaa"
    print permisos
    #Datos nuevos del user story
    if request.method == 'POST':
        form = ModActividadesForm(request.POST)
        if form.is_valid():
            acti.nombre = form.cleaned_data['nombre']
            acti.save()
            return HttpResponseRedirect("/flujos&id=" + str(proyecto_id))
    else:
        form = ModActividadesForm(
            initial={'nombre': acti.nombre})
    return render_to_response('flujo/mod_actividad.html', {'form': form,
                                                           'proyecto': proyecto,
                                                           'act': acti,
                                                           'mod_ACTI': 'Modificar ACTIVIDAD' in perm,
                                                           'mod_acti': 'Modificar actividad' in permisos},
                              context_instance=RequestContext(request))

#----------------------------------CONFIGURACION PREVIA AL INICIO DE CADA SPRINT---------------------------
@login_required
def conf_proyecto(request, proyecto_id,sprint_id):
    """
	Configuración inicial de un proyecto: agregar user stories al sprint, flujos, duración de los sprints.
    :param request:
    :param proyecto_id:
	:param sprint_id:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    flujos= Flujo.objects.filter(proyecto=proyecto_id)
    list = []
    userstories=UserStory.objects.filter(proyecto=proyecto_id, estado='En Espera')
    sprint=Sprint.objects.get(id=sprint_id)
    perm = get_permisos_proyecto(user,proyecto)
    usS=UsSprint.objects.filter(sprint=sprint.id)
    lis= UsSprint.objects.filter(proyecto=proyecto_id,sprint=sprint_id)
    band=1
    for i in lis:
                if i.us.responsable == None or i.us.flujo == None :
                    band=0
                    break
                else:
                    band=1
    equipo=False
    equi=Equipo.objects.filter(proyecto=proyecto.id, sprint=sprint.id)
    for i in equi:
        equipo=True
    if request.method == 'POST':
        for i in userstories:
                list.append(i)
                act =0

        proyecto=Proyecto.objects.get(id=proyecto_id)
        usflujo=flujoUS.objects.filter()
        equi=Equipo.objects.filter(proyecto=proyecto.id, sprint=sprint.id)

        suma=0
        for i in equi:
                suma=int(x=i.horas)+suma

        suma = suma*5*sprint.duracion
        sprint.horastotales=suma
        sprint.disponibilidad=sprint.horastotales
        sprint.save()

   # return render_to_response("conf/sprint.html",{'us':us,'proyecto':proyecto,'usflujo':usflujo

    #return HttpResponseRedirect("/configuracion&id="+str(proyecto_id))
        act=0
        for i in flujos:
                actividad= ActividadesFlujo.objects.filter(flujo=i)
                if actividad:
                    act=1
        if act is not 0:
                equi=Equipo.objects.filter(proyecto=proyecto.id,sprint=sprint.id)
                suma=0
                for i in equi:
                    suma=int(x=i.horas)+suma

                return render_to_response('conf/config_inicial.html', {'equipo':equipo,'us':usS,'lista': proyecto,'usflujo':usflujo,
                                                                   'proyecto':proyecto, 'sprint':sprint,'band':band,
                                                                   'user': user,
                                                                   'listaUS':userstories,
                                                                   'ver_proyectos': 'Ver proyectos' in permisos,
                                                                   'crear_proyecto': 'Crear proyecto' in permisos,
                                                                   'mod_proyecto': 'Modificar proyecto' in permisos,
                                                                   'ver_flujos': 'Ver flujos' in permisos,
                                                                   'Asignar_Flujo': 'Asignar Flujo' in permisos,
                                                                   'Asignar_Responsable':'Asignar Responsable' in permisos,
                                                                   'Agregar_US': 'Agregar us' in permisos,

                                                                   'Iniciar_Proyecto':'Iniciar Proyecto' in permisos,
                                                                   'eliminar_proyecto': 'Eliminar proyecto' in permisos},
                                                                     context_instance=RequestContext(request))

        else:
                return HttpResponse("Debe agregar por lo menos un flujo con una actividad para  iniciar el proyecto")
    else:
         usflujo=flujoUS.objects.filter()
         print "holiiii"

         return render_to_response('conf/config_inicial.html', {'equipo':equipo,'band':band,'lista': proyecto,'us':usS,'usflujo':usflujo,
                                                                   'proyecto':proyecto, 'sprint':sprint,
                                                                   'user': user,
                                                                   'listaUS':userstories,
                                                                   'ver_proyectos': 'Ver proyectos' in permisos,
                                                                   'crear_proyecto': 'Crear proyecto' in permisos,
                                                                   'mod_proyecto': 'Modificar proyecto' in permisos,
                                                                   'ver_flujos': 'Ver flujos' in permisos,
                                                                   'Asignar_Flujo': 'Asignar Flujo' in permisos,
                                                                   'Asignar_Responsable':'Asignar Responsable' in permisos,
                                                                   'Agregar_US': 'Agregar us' in permisos,

                                                                   'Iniciar_Proyecto':'Iniciar Proyecto' in permisos,
                                                                   'eliminar_proyecto': 'Eliminar proyecto' in permisos},
                                                                     context_instance=RequestContext(request))


#----------->Generar Equipo
@login_required
def admin_equipo(request,proyecto_id,sprint_id):
    """
	Administración de equipos: creación de equipos de trabajo  para un sprint dado.
	:param request:
	:param proyecto_id:
	:param sprint_id:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    p = Proyecto.objects.get(pk=proyecto_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=p).only('rol')
    permisos_obj = []
    for i in roles:
        print "mundooo"
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos

    sprint=Sprint.objects.get(proyecto=proyecto_id,id=sprint_id)
    miembros = Equipo.objects.filter(proyecto=proyecto_id,sprint=sprint.id).order_by('id')

    suma=0
    for i in miembros:
                suma=int(x=i.horas)+suma

    suma = suma*5*sprint.duracion
    sprint.horastotales=suma
    sprint.disponibilidad=sprint.horastotales
    sprint.save()
    #-------------------------------------------------------------------
    lista = []
    listah=[]

    for i in miembros:
        if not i.usuario.usuario in lista:
             lista.append(i.usuario)

    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            palabra = form.cleaned_data['filtro']
            lista = Equipo.objects.filter(Q(username__icontains=palabra) | Q(first_name__icontains=palabra) | Q(
                last_name__icontains=palabra)).order_by('id')
            paginas = form.cleaned_data['paginas']
            request.session['nro_items'] = paginas
            paginator = Paginator(lista, int(paginas))
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                pag = paginator.page(page)
            except (EmptyPage, InvalidPage):
                pag = paginator.page(paginator.num_pages)
            return render_to_response('conf/admin_equipo.html', {'sprint':sprint,'lista': lista, 'pag': pag, 'form': form,
                                                                         'user': user,
                                                                         'proyecto': Proyecto.objects.get(
                                                                             id=proyecto_id),
                                                                         'miembros': miembros,

                                                                         'ver_miembros': 'Ver miembros' in permisos,
                                                                         'abm_miembros': 'ABM miembros' in permisos},
                                      context_instance=RequestContext(request))
    else:
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        if not 'nro_items' in request.session:
            request.session['nro_items'] = 5
        paginas = request.session['nro_items']
        paginator = Paginator(lista, int(paginas))
        try:
            pag = paginator.page(page)
        except (EmptyPage, InvalidPage):
            pag = paginator.page(paginator.num_pages)
        form = FilterForm(initial={'paginas': paginas})
        return render_to_response('conf/admin_equipo.html', {'sprint':sprint,'lista': lista, 'pag': pag, 'form': form,
                                                                     'user': user,
                                                                     'proyecto': Proyecto.objects.get(id=proyecto_id),
                                                                     'miembros': miembros, #este fue cambiado de lista a miembros
                                                                     'ver_miembros': 'Ver miembros' in permisos,
                                                                     'abm_miembros': 'ABM miembros' in permisos},
                                  context_instance=RequestContext(request))

@login_required
def add_miembro_equipo(request, proyecto_id,sprint_id):
    """
    Agregar miembros a un equipo creado para un sprint.
    :param request:
    :param proyecto_id:
	:param sprint_id:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    p = get_object_or_404(Proyecto, id=proyecto_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=p).only('rol')



    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    proyecto=Proyecto.objects.get(id=proyecto_id)
    sprint=Sprint.objects.get(proyecto=proyecto_id,id=sprint_id)
    #-------------------------------------------------------------------
    if request.method == 'POST':
        form = MiembroEquipoForm(p, request.POST)
        if form.is_valid():
            relacion = Equipo()

            relacion.usuario = form.cleaned_data['usuario']
            relacion.proyecto = proyecto
            relacion.sprint= sprint.id
            relacion.horas=form.cleaned_data['horas']
            relacion.save()





            return HttpResponseRedirect("/configuracion/equipo&id=" + str(proyecto_id)+"/sprint&id="+str(sprint_id))
    else:
        form = MiembroEquipoForm(p)
    return render_to_response('conf/add_miembroE.html', {'sprint':sprint,'form': form,
                                                              'user': user,
                                                              'proyecto': p,
                                                              'abm_miembros': 'ABM miembros' in permisos,
                                                              'asignar_roles': 'Asignar roles'},
                              context_instance=RequestContext(request))
@login_required
def responsable_us(request, proyecto_id, us_id,sprint_id):
    """
    Asignar un usuario responsable para un user story dado, de acuerdo al equipo creado para el sprint.
    :param request:
    :param proyecto_id:
	:param us_id:
	:param sprint_id:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    print proyecto
    perm = get_permisos_proyecto(user,proyecto)
    lista_miembros = UsuarioRolProyecto.objects.filter(proyecto=proyecto)

    sprint=Sprint.objects.get(id=sprint_id)
    us= UserStory.objects.get(id=us_id)
    usprint=UsSprint.objects.get(us=us_id,sprint=sprint.id)
    print usprint
    lista_equipo= Equipo.objects.filter(sprint=sprint.id, proyecto=proyecto.id)

    print "holaaaaa"
    print us.proyecto

    if request.method == 'POST':
        print "ttttt"
        form = RespUserStoryForm(proyecto,sprint,request.POST)
        if form.is_valid():

            nuevo = ResponsableUS()
            nue=form.cleaned_data['usuario']
            nuevo.usuario = form.cleaned_data['usuario']

            nuevo.us= us
            nuevo.save()
            histus=HistorialUS()
            histus.us=us
            histus.estado= us.estado
            histus.actividad= us.actividad
            histus.estado_actividad =us.estado_actividad
            histus.flujo = us.flujo
            histus.responsable = us.responsable
            histus.fecha=datetime.today()
            histus.save()
            print "st es"
            print nuevo.usuario.usuario.id
            usrol=UsuarioRolProyecto.objects.get(id=nuevo.usuario.usuario.id,proyecto=proyecto_id)
            print usrol.id

            print "nuevo"
            equipo=Equipo.objects.get(usuario=usrol.id,sprint=sprint.id)
            us.responsable=equipo.usuario.usuario
            us.horas=equipo.horas
            us.save()
            sprint.save()

            return HttpResponseRedirect("/configuracion&id=" + str(proyecto_id)+"/confsprint&id="+str(sprint_id))
        else:
            return render_to_response("conf/asignar_us.html", {'sprint':sprint_id,'form':form,'proyecto':us.proyecto}, context_instance=RequestContext(request))
    else:
        dict = {}
        for i in lista_equipo:
            dict[i.usuario.usuario] = True
        form = RespUserStoryForm(proyecto,sprint,initial = {'usuario': dict})
        return render_to_response("conf/asignar_us.html", {'sprint':sprint_id,'form':form,'proyecto':us.proyecto}, context_instance=RequestContext(request))


@login_required
def asignar_flujoUS(request, proyecto_id, us_id,sprint_id):
    """
	Asignar flujos a user story existentes en un proyecto.
    :param request:
    :param proyecto_id:
	:param us_id:
	:param sprint_id:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    p = get_object_or_404(Proyecto, id=proyecto_id)
    permisos = get_permisos_sistema(user)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    perm = get_permisos_proyecto(user,proyecto)
    lista_flujos = Flujo.objects.filter(proyecto=proyecto_id)
    us= UserStory.objects.get(id=us_id)

    if request.method == 'POST':

        form = UserStoryFlujoForm(proyecto,request.POST)
        if form.is_valid():

            nuevo = flujoUS()
            nuevo.flujo = form.cleaned_data['flujo']
            nuevo.us= us
            nuevo.save()
            us.flujo=nuevo.flujo
            act_flujos= ActividadesFlujo.objects.filter(flujo=us.flujo)
            histus=HistorialUS()
            histus.us=nuevo.us
            histus.estado= us.estado
            histus.actividad= us.actividad
            histus.estado_actividad =us.estado_actividad
            histus.flujo = us.flujo
            histus.responsable = us.responsable
            histus.fecha=datetime.today()
            histus.save()
            list=[]
            for i in act_flujos:
                list.append(i)
            us.actividad=list[0]
            us.save()
            print list[0]

            return HttpResponseRedirect("/configuracion&id=" + str(proyecto_id)+"/confsprint&id="+str(sprint_id))


        else:

            return render_to_response("conf/asignar_flujoaUS.html", {'proyecto':proyecto, 'sprint':sprint_id,'form':form}, context_instance=RequestContext(request))
    dict = {}
    for i in lista_flujos:
            print i.nombre
            dict[i.proyecto] = True
    form = UserStoryFlujoForm(proyecto,initial = {'flujo': dict})
    return render_to_response("conf/asignar_flujoaUS.html", {'proyecto':proyecto, 'sprint':sprint_id,'form':form}, context_instance=RequestContext(request))

def iniciarsprint(request, proyecto_id,sprint_id):
    """
    Iniciar un sprint si cumple con los requerimientos: todos los user stories agregados al sprint, deben tener un flujo y responsable asignados.
    :param request:
    :param proyecto_id:
	:param sprint_id:
    :return:
    """
    sprint=Sprint.objects.get(id=sprint_id)
    usS=UsSprint.objects.filter(sprint=sprint_id,proyecto=proyecto_id)
    bandera=0
    for i in usS:
        if i.us.responsable == None or i.us.flujo == None:

            bandera=1
            break

    flujo=Flujo.objects.filter(proyecto=proyecto_id)
    user=User.objects.get(id=request.user.id)
    proyecto=Proyecto.objects.get(id=proyecto_id)
    actividades=ActividadesFlujo.objects.filter(proyecto=proyecto_id)
    usflujo= UserStory.objects.filter(proyecto=proyecto_id)
    sprint.fecha_inicio= datetime.today()
    sprint.estado='Iniciado'


    funcion_sprint(sprint)
    equi=Equipo.objects.filter(proyecto=proyecto.id,sprint=sprint.id)
    suma=0
    for i in equi:
                suma=int(x=i.horas)+suma

    suma = suma*5*sprint.duracion
    sprint.horastotales=suma
    sprint.save()
    if bandera == 1:
        return HttpResponse("Asigne Flujo o Responsable")
    return HttpResponseRedirect("/configuracion&id="+str(proyecto_id)+"/sprint_bk")
    #return render_to_response("conf/sprint_bk.html",{'bandera':bandera,'suma':suma,'user':user,'flujo':flujo,'proyecto':proyecto,'actividades':actividades,'usflujo':usflujo}, context_instance=RequestContext(request))

def cambiar_estado(request, proyecto_id, act_id, us_id,flujo_id):
    """
    Cambiar el estado de una actividad de un user story (Todo a Doing o de Doing a Done).
    :param request:
    :param proyecto_id:
    :param act_id:
    :param us_id:
    :param flujo_id:
    :return:
    """
    flujo=Flujo.objects.filter(proyecto=proyecto_id)
    proyecto=Proyecto.objects.get(id=proyecto_id)
    actividades=ActividadesFlujo.objects.filter(proyecto=proyecto_id)
    act=Actividades.objects.get(id=act_id)
    print "alñdkfjañdlfkjakdfñlakfajñflkaf"
    print act_id
    fluj=Flujo.objects.get(id=flujo_id)
    usflujo= UserStory.objects.filter(proyecto=proyecto_id)
    us= UserStory.objects.get(id=us_id)
    lista_flujos=ActividadesFlujo.objects.filter(flujo=flujo)
    termino=0
    sp= Sprint.objects.get(proyecto=proyecto_id,estado='Iniciado')
    ussp= UsSprint.objects.filter(proyecto=proyecto_id,sprint=sp.id)


    long=len(ActividadesFlujo.objects.filter(flujo=flujo_id))
    total = []
    for i in ActividadesFlujo.objects.filter(flujo=flujo_id):
        total.append(i)
    if us.actividad == total[long-1]:

        termino=1
    if request.method == 'POST':
        form = CambiarEstadoActividadForm(request.POST)

        if form.is_valid() :
            us.estado_actividad = form.cleaned_data["Estado"]
            us.save()
            histus= HistorialUS()
            histus.us=us
            histus.estado= us.estado
            histus.actividad= us.actividad
            histus.estado_actividad =us.estado_actividad
            histus.flujo = us.flujo
            histus.responsable = us.responsable
            histus.fecha=datetime.today()
            histus.save()

            for i in ussp:
                    if i.us.actividad.ultimo == 1 and i.us.estado_actividad == 'Done':
                        print "prooooo"
                        mensaje= 'Scrum Master:' + str(proyecto.usuario_scrum.usuario.get_full_name()) + str("\n")+ 'Responsable:' + str(i.us.responsable.get_full_name())+'  El user story debe ser verificado para enviar a release: '+ str(us)+ " pertenece al proyecto " + "'" +str(proyecto.nombre)+"'"+ " en el Sprint " + "'"+str(sp.nro_sprint)+"'"
                        enviar_correo(request,request.user,mensaje,proyecto.usuario_scrum.usuario.email,us.responsable.email)

            return HttpResponseRedirect("/configuracion&id=" + str(proyecto_id)+"/tablero")
        else:

            return render_to_response("conf/cambiar_estado.html", {'termino':termino,'form':form,'act':act,'us':us,'flujo':fluj}, context_instance=RequestContext(request))
    else:

        form= CambiarEstadoActividadForm(initial = {'Estados': us.estado_actividad})
    return render_to_response("conf/cambiar_estado.html",{'termino':termino,'form':form,'act':act,'us':us,'flujo':fluj,'proyecto':proyecto,'actividades':actividades,'usflujo':usflujo}, context_instance=RequestContext(request))

def flujo_user_sprint(request, proyecto_id):
    """
    Relacionar un user story a un sprint.
    :param request:
    :param proyecto_id:
    :return:
    """
    us=UsSprint.objects.filter(sprint=1)
    proyecto=Proyecto.objects.get(id=proyecto_id)
    usflujo=flujoUS.objects.filter()

    return render_to_response("conf/sprint.html",{'us':us,'proyecto':proyecto,'usflujo':usflujo},context_instance=RequestContext(request))


#------------------------VIEW PARA ENVIAR CORREO
#enviar_correo(request,user,'Fueron Agregados los siguientes cambios al User Story : ',us.nombre,us.descripcion)

def enviar_correo(request,User_nombre,mensaje,emailtoscrum,emailtorespo):

    """
	Se envía un correo al scrum y al responsable, ante modificaciones en el Historial de tareas del User Story.
    :param request:
    :param User_nombre: nombre del usuario que realizó el cambio.
	:param mensaje:    
	:param emailtoscrum:
    :param emailtorespo:
    :return:
    """

    email_context = {
        'titulo': "Actualizaciones:",
        'usuario':request.user.get_full_name(),#cambiar
        'mensaje': mensaje,
    }
    email_html =  render_to_string('email.html',email_context)
    email_text = strip_tags(email_html)
    #destinatario = request.user.email
    correo = EmailMultiAlternatives(
        'GDT Project - Notificacion',
        email_text,#contenido del correo
        'gdtprojectinfo@gmail.com',#quien lo envia
        #[destinatario],
       [emailtoscrum,emailtorespo],#a quien se le envia
    )
    # se especifica que el contenido es html
    correo.attach_alternative(email_html, 'text/html')
    correo.send()
    return HttpResponseRedirect('/')

@login_required
def add_tarea(request, proyecto_id, us_id):
    """
    Agregar una tarea con la descripcion, nombre y tiempo que le tomo hacer el user story.
    :param request:
    :param proyecto_id:
    :param us_id:
    :return:
    """
    #####
    user = User.objects.get(username=request.user.username)
    proyect = get_object_or_404(Proyecto, id=proyecto_id)
    permisos = get_permisos_proyecto(user, proyect)
    us = get_object_or_404(UserStory, id=us_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolSistema.objects.filter(usuario = user).only('rol')
    proyecto =Proyecto.objects.get(id=proyecto_id)
    permisos_obj = []
    perm = get_permisos_proyecto(user,proyecto)
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    #-------------------------------------------------------------------
    if request.method == 'POST':
        form = TareaForm(request.POST)

        if form.is_valid():
            #docu=get_object_or_404(Documento,us=us)

            nuevo = Tarea()
            nuevo.tiempo=form.cleaned_data['tiempo']
            nuevo.descripcion = form.cleaned_data['descripcion']
            nuevo.nombre = form.cleaned_data['nombre']
            nuevo.us = us
            nuevo.fluactpro=us.actividad
            nuevo.save()
            us.hora_acumulada= us.hora_acumulada+nuevo.tiempo
            us.save()
            if us.estado_actividad == 'To Do':
                us.estado_actividad = 'Doing'
                us.save()
            #envio de email ante tarea sobre el us
            mensaje= 'Scrum Master:' + str(proyecto.usuario_scrum.usuario.get_full_name()) + str("\n")+ 'Responsable:' + str(us.responsable.get_full_name())+ str("\n")+'  AVISO:'+ str("\n")+'  Se Agrego la tarea: '+ " ' " + nuevo.nombre+" ' "+str("\n")+ ' con la siguiente descripcion : '+" ' " + nuevo.descripcion + " ' " + str("\n")+' en la actividad: '+ " ' "+ nuevo.fluactpro.actividades.nombre+" ' "+  str("\n")+' en el flujo: '+" ' " + nuevo.fluactpro.flujo.nombre+" ' "

            enviar_correo(request,user,mensaje,proyecto.usuario_scrum.usuario.email,us.responsable.email)
            #Generacion del historial
            hist = Historial()
            hist.usuario = user
            hist.fecha_creacion = datetime.today()
            hist.user_story = us
           # hist.documento=docu
            hist.descripcion=nuevo.descripcion
            hist.save()
            adjunto= Adjunto()
            adjunto.nombre= "Ninguno"
            adjunto.save()

	    registrar_historial(us,hist,nuevo,adjunto)
            return HttpResponseRedirect("/configuracion&id=" + str(proyecto_id) + "/tablero")
    else:
        form = TareaForm()
    return render_to_response('us/crear_tarea.html',{'proyecto': proyecto,'us':us,
            'form': form,
            'abm_user_story': 'ABM user story' in permisos,
            'crear_us': 'Crear US' in perm},context_instance=RequestContext(request))


@login_required
def ver_historial(request, proyecto_id, us_id):
    """
    Despliega el historial de un user story mostrando la descripción de las tareas agregadas y el nombre de adjuntos cargados.
    :param request:
    :param proyecto_id:
    :param us_id:
    :return:
    """
    us = UserStory.objects.get(pk=us_id)
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    perm = get_permisos_proyecto(user, proyecto)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=proyecto).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    #-------------------------------------------------------------------
    versiones = RegistroHistorial.objects.filter(us=us)
    #linea = LineaBase.objects.filter(proyectos=proyect, fase=3)
    #if (linea):
    fin = 0
    #else:
    #    fin = 1
    hist=Historial.objects.filter(user_story=us)
    variables = RequestContext(request, {
                                         'lista': versiones,
                                         'user_story': us,'hist':hist,
                                         'fin': fin,
                                         'proyecto': proyecto,
                                         'ver_historial_user_story': 'Ver historial' in permisos,
                                         'ver_historial_us': 'Ver Historial'})
    return render_to_response('us/historial.html', variables)


def list(request, proyecto_id, us_id):
    """
    Subir archivo adjunto al proyecto.
    :param request:
    :param proyecto_id:
    :param us_id:
    :return:
    """
    proyect = get_object_or_404(Proyecto, id=proyecto_id)
    # Handle file upload
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Documento(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect("/userstories&id="+ str(proyect.id) +  "/")
    else:
        form = DocumentoForm() # A empty, unbound form

    # Load documents for the list page
    documents = Documento.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'us/crear_tarea.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


@login_required
def actividad_flujo(request, proyecto_id, flujo_id,us_id):
    """
    Relacionar una actividad con un flujo dado en un proyecto.
    :param request:
    :param proyecto_id:
    :param flujo_id:
    :param us_id:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    p = get_object_or_404(Proyecto, id=proyecto_id)
    permisos = get_permisos_sistema(user)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    perm = get_permisos_proyecto(user,proyecto)
    flujo = Flujo.objects.get(id=flujo_id)
    us= UserStory.objects.get(id=us_id)
    lista_flujos=ActividadesFlujo.objects.filter(flujo=flujo)
    if request.method == 'POST':
        form = ActividadesFlujoForm(flujo,request.POST)

        if form.is_valid():


            us.actividad = form.cleaned_data['act_flujo']
            print us.actividad
            us.estado_actividad= "To Do"
            us.save()
            return HttpResponseRedirect("/configuracion&id=" + str(proyecto_id))
        else:

            return render_to_response("conf/act_flujo.html", {'form':form}, context_instance=RequestContext(request))
    dict = {}
    for i in lista_flujos:
            print i.actividades
            dict[i.actividades] = False
    form =ActividadesFlujoForm(flujo,initial = {'act_flujo': dict})
    return render_to_response("conf/act_flujo.html", {'form':form}, context_instance=RequestContext(request))

def cambiar_actividad(request, proyecto_id, act_id, us_id,flujo_id):
    """
    Cambiar actividad de un user stories (lo puede hacer un scrum master o un desarrollador).
    :param request:
    :param proyecto_id:
    :param act_id:
    :param us_id:
    :param flujo_id:
    :return:
    """
    act=Actividades.objects.get(id=act_id)
    flujo=Flujo.objects.filter(proyecto=proyecto_id)
    proyecto=Proyecto.objects.get(id=proyecto_id)
    actividades=ActividadesFlujo.objects.filter(proyecto=proyecto_id)
    usflujo= UserStory.objects.filter(proyecto=proyecto_id)
    us= UserStory.objects.get(id=us_id)
    lista_flujos=ActividadesFlujo.objects.filter(flujo=flujo_id)
    user=User.objects.get(id=request.user.id)
    sp= Sprint.objects.get(proyecto=proyecto_id,estado='Iniciado')
    ussp= UsSprint.objects.filter(proyecto=proyecto_id,sprint=sp.id)
    for i in lista_flujos:
        if i.actividades.id == act.id :
            nueva= int(x=i.id)+1
            print nueva
            print "nueva"
            if ActividadesFlujo.objects.get(id=nueva,flujo=flujo_id) != None:

                us.actividad= ActividadesFlujo.objects.get(id=nueva,flujo=flujo_id)
                us.estado_actividad='To Do'
                us.save()
                histus=HistorialUS()
                histus.us=us
                histus.estado= us.estado
                histus.actividad= us.actividad
                histus.estado_actividad =us.estado_actividad
                histus.flujo = us.flujo
                histus.responsable = us.responsable
                histus.fecha = datetime.today()
                histus.save()
                return HttpResponseRedirect("/configuracion&id="+str(proyecto_id)+"/tablero/")



    return render_to_response("conf/sprint_iniciado.html",{'user':user,'flujo':flujo,'proyecto':proyecto,'actividades':actividades,'usflujo':usflujo}, context_instance=RequestContext(request))

def ver_tablero(request, proyecto_id):
    """
    Visualización del tablero Kanban con todos los user stories existentes.
    :param request:
    :param proyecto_id:
    :return:
    """
    flujo=Flujo.objects.filter(proyecto=proyecto_id)
    user=User.objects.get(id=request.user.id)
    proyecto=Proyecto.objects.get(id=proyecto_id)
    actividades=ActividadesFlujo.objects.filter(proyecto=proyecto_id)
    sprint=Sprint.objects.get(proyecto=proyecto_id,estado='Iniciado')
    nro= sprint.nro_sprint
    usflujo= UsSprint.objects.filter(proyecto=proyecto_id,sprint=sprint.id)
    roles = UsuarioRolProyecto.objects.filter(usuario = user, proyecto=proyecto_id).only('rol')
    rol=0
    for i in roles:
        if i.rol.id == 2:
            rol = 1



    return render_to_response("conf/sprint_iniciado.html",{'rol':rol,'nro':nro,'user':user,'flujo':flujo,'proyecto':proyecto,'actividades':actividades,'usflujo':usflujo}, context_instance=RequestContext(request))

def sprint_admin(request,proyecto_id):
    """
    Muestra los sprint del proyecto dado. Aquellos en ejecucion y los terminados.
    :param request: peticion
    :param proyecto_id: identificador del proyecto
    :return:la vista de los sprint en ejecucion y los terminados.
    """
    proyecto=Proyecto.objects.get(id=proyecto_id)
    return HttpResponse("El proyecto  --"+str(proyecto) +"-- no cuenta con sprints finalizados")

def us_backlog(request,proyecto_id):
    """
    Busca los user stories que tienen estado en espera de un proyecto
    Para poder trabajar con ellos en el siguiente sprint
    :param request: peticion
    :param proyecto_id:
    :return:
    """
    proyecto=Proyecto.objects.get(id=proyecto_id)
    userstories=UserStory.objects.filter(proyecto=proyecto_id,estado='En Espera')
    print userstories
    return render_to_response("conf/us_backlog.html",{'proyecto':proyecto,'userstories':userstories}, context_instance=RequestContext(request))

@login_required
def sprint_bk(request,proyecto_id):
    """
	Visualiza los user stories que pertenezcan a un sprint en un momento dado.
    :param request:
    :param proyecto_id:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    proyecto=Proyecto.objects.get(id=proyecto_id)
    perm = get_permisos_proyecto(user,proyecto)
    lista= Sprint.objects.filter(proyecto=proyecto.id)
    """for i in equi:
                suma=int(x=i.horas)+suma

    suma = suma*5*sprint.duracion
    sprint.horastotales=suma
    sprint.save()"""

    for i in lista:
        print datetime.today()
        if i.fecha_fin != None:
            fecha=datetime(i.fecha_fin.year,i.fecha_fin.month,i.fecha_fin.day)
            print fecha
            fecha_actual= datetime.today()
            year= fecha_actual.year
            month=fecha_actual.month
            day=fecha_actual.day
            fecha_actual=datetime(year,month,day)
            if fecha == fecha_actual:


                print "kkkk"
                i.estado='Finalizado'
                i.save()
                uslista=UsSprint.objects.filter(sprint=i.id)
                for j in uslista:
                    user=UserStory.objects.get(id=j.us.id)
                    if user.estado=='En Proceso':
                        user.estado='En Proceso'
                        user.save()

    estado=0
    for j in lista:
        if j.estado == 'Iniciado':
            estado=1
            break


    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            palabra = form.cleaned_data['filtro']
           # lista = Sprint.objects.filter(Q(nombre__icontains=palabra) | Q(descripcion__icontains=palabra) | Q(
              #  usuario_scrum__username__icontains=palabra)).order_by('id')
            lista= Sprint.objects.filter(proyecto=proyecto.id)
            paginas = form.cleaned_data['paginas']
            request.session['nro_items'] = paginas
            paginator = Paginator(lista, int(paginas))
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                pag = paginator.page(page)
            except (EmptyPage, InvalidPage):
                pag = paginator.page(paginator.num_pages)
            return render_to_response('conf/sprint_bk.html', {'estado':estado,'proyecto':proyecto,'lista': lista, 'pag': pag, 'form': form,
                                                                         'user': user,
                                                                         'ver_sprint': 'Ver Sprint' in perm,
                                                                         'Ver_Sprint': 'Ver sprint' in permisos,
                                                                         'crear_sprint': 'Crear Sprint' in permisos,
                                                                         'crear_proyecto': 'Crear proyecto' in permisos,
                                                                         'mod_proyecto': 'Modificar proyecto' in permisos,
                                                                         'ver_flujos': 'Ver flujos' in permisos,
                                                                         'eliminar_proyecto': 'Eliminar proyecto' in permisos},
                                      context_instance=RequestContext(request))
    else:
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        if not 'nro_items' in request.session:
            request.session['nro_items'] = 5
        paginas = request.session['nro_items']
        paginator = Paginator(lista, int(paginas))
        try:
            pag = paginator.page(page)
        except (EmptyPage, InvalidPage):
            pag = paginator.page(paginator.num_pages)
        form = FilterForm(initial={'paginas': paginas})
        return render_to_response('conf/sprint_bk.html', {'estado':estado,'proyecto':proyecto,'lista': lista, 'pag': pag, 'form': form,
                                                                         'user': user,
                                                                          'crear_sprint': 'Crear Sprint' in permisos,
                                                                         'ver_sprint': 'Ver Sprint' in perm,
                                                                         'Ver_Sprint': 'Ver sprint' in permisos,
                                                                         'crear_proyecto': 'Crear proyecto' in permisos,
                                                                         'mod_proyecto': 'Modificar proyecto' in permisos,
                                                                         'ver_flujos': 'Ver flujos' in permisos,
                                                                         'eliminar_proyecto': 'Eliminar proyecto' in permisos},
                                      context_instance=RequestContext(request))

def add_us_sprint(request, proyecto_id,us_id,sprint_id):
    """
	Permite agregar user stories a un sprint.
    :param request:
    :param proyecto_id:
	:param us_id:
	:param sprint_id;
    :return:
    """
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    us = UserStory.objects.get(id=us_id)
    sprint=Sprint.objects.get(id=sprint_id)
    nuevo=UsSprint()
    nuevo.us= us
    us.estado='En Proceso'
    us.save()
    nuevo.sprint=sprint.id
    nuevo.proyecto=proyecto
    nuevo.save()
    sprint.disponibilidad=sprint.disponibilidad-us.duracion
    print sprint.disponibilidad
    sprint.save()
    us= UserStory.objects.get(id=us_id)
    us.estado= 'En Proceso'
    us.save()

    return HttpResponseRedirect("/configuracion&id="+str(proyecto_id)+"/confsprint&id="+str(sprint_id))

@login_required
def conf_inicio_sprint(request, proyecto_id):
    """
	Permite la configuracion para el inicio de un proyecto: agregar user stories al sprint, flujos, duracion de los sprints
    :param request:
    :param proyecto_id:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    proyecto = Proyecto.objects.get(id=proyecto_id)

    sp=Sprint.objects.filter(proyecto=proyecto_id)
    perm = get_permisos_proyecto(user,proyecto)
    userstories=UserStory.objects.filter(proyecto=proyecto_id,estado='En Espera')
    usflujo=flujoUS.objects.filter()

    if request.method == 'POST':
        print "tanteo"
        form=SprintForm(request.POST)
        if form.is_valid():
            sprint=Sprint()
            sprint.estado='Preconfig'
            sprint.duracion= form.cleaned_data['duracion']
            sprint.proyecto=proyecto
            sprint.nro_sprint=len(sp)+1
            sprint.save()
            return HttpResponseRedirect("/configuracion&id="+str(proyecto_id)+"/confsprint&id="+str(sprint.id))
    else:
        form=SprintForm(request.POST)
        return render_to_response('conf/equipo.html', {'duracion':form,'sprint':sp,'lista': proyecto,
                                                                   'proyecto':proyecto,
                                                                   'user': user,

                                                                   'ver_proyectos': 'Ver proyectos' in permisos,
                                                                   'crear_proyecto': 'Crear proyecto' in permisos,
                                                                   'mod_proyecto': 'Modificar proyecto' in permisos,
                                                                   'ver_flujos': 'Ver flujos' in permisos,
                                                                   'Asignar_Flujo': 'Asignar Flujo' in permisos,
                                                                   'Asignar_Responsable':'Asignar Responsable' in permisos,
                                                                   'Agregar_US': 'Agregar us' in permisos,

                                                                   'Iniciar_Proyecto':'Iniciar Proyecto' in permisos,
                                                                   'eliminar_proyecto': 'Eliminar proyecto' in permisos},
                                                                     context_instance=RequestContext(request))



@login_required
def sprint_us(request, proyecto_id,sprint_id):
    """
	Permite la configuracion para el inicio de un proyecto,
    agrega user stories al sprint, flujos, duracion de los sprints
    :param request:
    :param proyecto_id:
	:param sprint_id:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    flujos= Flujo.objects.filter(proyecto=proyecto_id)
    list = []
    userstories=UserStory.objects.filter(proyecto=proyecto_id,estado='En Espera')
    sprint=Sprint.objects.get(id=sprint_id)
    perm = get_permisos_proyecto(user,proyecto)
    usS=UsSprint.objects.filter(sprint=sprint.id)
    if request.method == 'POST':
        for i in userstories:
                list.append(i)
                act =0

        proyecto=Proyecto.objects.get(id=proyecto_id)
        usflujo=flujoUS.objects.filter()
        equi=Equipo.objects.filter(proyecto=proyecto.id, sprint=sprint.id)
        suma=0
        for i in equi:
                suma=int(x=i.horas)+suma

        suma = suma*5*sprint.duracion
        sprint.horastotales=suma
        sprint.disponibilidad=sprint.horastotales
        sprint.save()

   # return render_to_response("conf/sprint.html",{'us':us,'proyecto':proyecto,'usflujo':usflujo

    #return HttpResponseRedirect("/configuracion&id="+str(proyecto_id))
        act=0
        for i in flujos:
                actividad= ActividadesFlujo.objects.filter(flujo=i)
                if actividad:
                    act=1
        if act is not 0:
                equi=Equipo.objects.filter(proyecto=proyecto.id,sprint=sprint.id)
                suma=0
                for i in equi:
                    suma=int(x=i.horas)+suma

                return render_to_response('conf/sprint_us.html', {'us':usS,'lista': proyecto,'usflujo':usflujo,
                                                                   'proyecto':proyecto, 'sprint':sprint,
                                                                   'user': user,
                                                                   'listaUS':userstories,
                                                                   'ver_proyectos': 'Ver proyectos' in permisos,
                                                                   'crear_proyecto': 'Crear proyecto' in permisos,
                                                                   'mod_proyecto': 'Modificar proyecto' in permisos,
                                                                   'ver_flujos': 'Ver flujos' in permisos,
                                                                   'Asignar_Flujo': 'Asignar Flujo' in permisos,
                                                                   'Asignar_Responsable':'Asignar Responsable' in permisos,
                                                                   'Agregar_US': 'Agregar us' in permisos,

                                                                   'Iniciar_Proyecto':'Iniciar Proyecto' in permisos,
                                                                   'eliminar_proyecto': 'Eliminar proyecto' in permisos},
                                                                     context_instance=RequestContext(request))

        else:
                return HttpResponse("Debe agregar por lo menos un flujo con una actividad para  iniciar el proyecto")
    else:
         usflujo=flujoUS.objects.filter()
         print "holiiii"

         return render_to_response('conf/sprint_us.html', {'lista': proyecto,'us':usS,'usflujo':usflujo,
                                                                   'proyecto':proyecto, 'sprint':sprint,
                                                                   'user': user,
                                                                   'listaUS':userstories,
                                                                   'ver_proyectos': 'Ver proyectos' in permisos,
                                                                   'crear_proyecto': 'Crear proyecto' in permisos,
                                                                   'mod_proyecto': 'Modificar proyecto' in permisos,
                                                                   'ver_flujos': 'Ver flujos' in permisos,
                                                                   'Asignar_Flujo': 'Asignar Flujo' in permisos,
                                                                   'Asignar_Responsable':'Asignar Responsable' in permisos,
                                                                   'Agregar_US': 'Agregar us' in permisos,

                                                                   'Iniciar_Proyecto':'Iniciar Proyecto' in permisos,
                                                                   'eliminar_proyecto': 'Eliminar proyecto' in permisos},
                                                                     context_instance=RequestContext(request))


@login_required
def enviar_a_release(request, proyecto_id, us_id):
    """
	Enviar los user stories con estado Done, al release.
	:param request:
	:param proyecto_id:
	:param us_id:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    proyect = Proyecto.objects.get(id=proyecto_id)
    us= UserStory.objects.get(pk=us_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario = user, proyecto = proyect).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos

    #-------------------------------------------------------------------

    release = Release()
    release.us = us
    release.save()
    us.estado= 'Pendiente'
    us.save()
    return HttpResponseRedirect("/configuracion&id="+str(proyecto_id)+"/tablero/")


    #return HttpResponseRedirect("/configuracion&id="+str(proyecto_id)+"/tablero/")


@login_required
def release(request, proyecto_id):
    """
	Lista de user stories con estado Done, que se encuentran en el release.
	:param request:
	:param proyecto_id:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    proyect = Proyecto.objects.get(id=proyecto_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario = user, proyecto = proyect).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    userstories= UserStory.objects.filter(estado='Pendiente')
    #-------------------------------------------------------------------

    return render_to_response("conf/release.html", {'proyecto':proyect,
                                                                   'user':user,
                                                                   'us':userstories,

                                                                   'revisar_item': 'Revisar items' in permisos},context_instance=RequestContext(request))

@login_required
def revisar_us(request, proyecto_id, us_id):
    """
	Permite al scrum, verificar los user stories con estado Done y confirmar o rechazar los mismos.
	:param request:
	:param proyecto_id:
	:param us_id:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    proyect = Proyecto.objects.get(id=proyecto_id)
    us= UserStory.objects.get(pk=us_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario = user, proyecto = proyect).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    #-------------------------------------------------------------------
    if request.method == 'POST':
            us.estado = 'Aprobado'
            us.save()
            histus=HistorialUS()
            histus.us=us
            histus.estado= us.estado
            histus.actividad= us.actividad
            histus.estado_actividad =us.estado_actividad
            histus.flujo = us.flujo
            histus.responsable = us.responsable
            histus.fecha=datetime.today()
            histus.save()
            return render_to_response("conf/confirmacion.html",{'proyecto':us.proyecto})


    return render_to_response("conf/revisar_detalles.html", {'proyecto':proyect,
                                                                   'user':user,
                                                                   'us':us,

                                                                   'revisar_item': 'Revisar items' in permisos},context_instance=RequestContext(request))


def recambiar_actividad(request, proyecto_id, act_id, us_id,flujo_id):
    """
	Permite cambiar un user story de actividad.
    :param request:
    :param proyecto_id:
    :param act_id:
    :param us_id:
    :param flujo_id:
    :return:
    """
    flujo=Flujo.objects.filter(proyecto=proyecto_id)
    proyecto=Proyecto.objects.get(id=proyecto_id)
    actividades=ActividadesFlujo.objects.filter(proyecto=proyecto_id)
    act=ActividadesFlujo.objects.get(id=act_id)
    print act_id
    fluj=Flujo.objects.get(id=flujo_id)
    usflujo= UserStory.objects.filter(proyecto=proyecto_id)
    us= UserStory.objects.get(id=us_id)
    lista_flujos=ActividadesFlujo.objects.filter(flujo=flujo)
    termino=0


    if request.method == 'POST':
        form = RecambiarActividadForm(act,fluj,request.POST)
        if form.is_valid() :
            us.actividad = form.cleaned_data["actividad"]
            us.estado_actividad = "To Do"
            us.estado= 'En Espera'

            us.save()
            histus=HistorialUS()
            histus.us=us
            histus.estado= us.estado
            histus.actividad= us.actividad
            histus.estado_actividad =us.estado_actividad
            histus.flujo = us.flujo
            histus.responsable = us.responsable
            histus.fecha=datetime.today()
            histus.save()
            return HttpResponseRedirect("/configuracion&id=" + str(proyecto_id)+"/tablero")
        else:

            return render_to_response("conf/recambiar_actividad.html", {'termino':termino,'form':form,'act':act,'us':us,'flujo':fluj}, context_instance=RequestContext(request))
    else:

        form = RecambiarActividadForm(act,fluj,request.POST)
        return render_to_response("conf/recambiar_actividad.html",{'termino':termino,'form':form,'act':act,'us':us,'flujo':fluj,'proyecto':proyecto,'actividades':actividades,'usflujo':usflujo}, context_instance=RequestContext(request))

@login_required
def ver_historial_us(request, proyecto_id, us_id):
    """
    Despliega el historial de un user story mostrando la descripcion de las tareas
    agregadas y el nombre de adjuntos cargados
    :param request:
    :param proyecto_id:
    :param us_id:
    :return:
    """
    us = UserStory.objects.get(pk=us_id)
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    perm = get_permisos_proyecto(user, proyecto)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=proyecto).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    #-------------------------------------------------------------------

    #linea = LineaBase.objects.filter(proyectos=proyect, fase=3)
    #if (linea):
    fin = 0
    #else:
    #    fin = 1
    hist=HistorialUS.objects.filter(us=us)
    for i in hist:
        print i.id
    variables = RequestContext(request, {'us':us,
                                         'lista': hist,
                                         'fin': fin,
                                         'proyecto': proyecto,
                                         'ver_historial_user_story': 'Ver historial' in permisos,
                                         'ver_historial_us': 'Ver Historial'})
    return render_to_response('conf/historial_us.html', variables)



@login_required
def admin_adjuntos(request, proyecto_id, us_id):
    """
	Administracion de archivos de un item dado.
	:param request:
	:param proyecto_id:
	:param us_id:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    us = get_object_or_404(UserStory, id =us_id)
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    permisos = get_permisos_proyecto(user, proyecto)
    archivos = Adjunto.objects.filter(us = us, habilitado = True)
    return render_to_response('us/adjuntos.html', {'us':us, 'lista': archivos,'user':user,
    'proyecto':proyecto,                                                                        # 'abm_items': 'ABM items' in permisos
				})


@login_required
def add_adjunto(request, proyecto_id, us_id):
    """
	Adherir un archivo adjunto al proyecto.
	:param request:
	:param proyecto_id:
	:param us_id:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    proyect = get_object_or_404(Proyecto, id=proyecto_id)
    permisos = get_permisos_proyecto(user, proyect)
    us = get_object_or_404(UserStory, id=us_id)
    AdjuntoFormSet = formset_factory(AdjuntoForm)
    if request.method == 'POST':
        formset = AdjuntoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            archivos = Adjunto.objects.filter(us= us, habilitado=True)
            archivos_nuevos = request.FILES.values()
            for f in archivos_nuevos:
                nuevo = Adjunto()
                nuevo.nombre =f
                nuevo.tamano = f.size
                if f.size > 1048576:
                    mensaje = 'Tama&ntilde;o m&aacute;ximo excedido'
                    return render_to_response('error.html', {'mensaje':mensaje})
                nuevo.mimetype = f.content_type
                nuevo.contenido = base64.b64encode(f.read())
                nuevo.us = us
                nuevo.save()

                mensaje= 'Scrum Master:' + str(proyect.usuario_scrum.usuario.get_full_name()) + str("\n")+ 'Responsable:' + str(us.responsable.get_full_name())+ str("\n")+'  AVISO:'+ str("\n")+'  Se Agrego el adjunto: '+ " ' " + str(nuevo.nombre)+" '"
                enviar_correo(request,user,mensaje,proyect.usuario_scrum.usuario.email,us.responsable.email)
                tarea = Tarea()
                tarea.descripcion= "Adjunto"
                tarea.nombre= 'Adjunto'+str(nuevo.id)
                tarea.fluactpro= us.actividad
                tarea.us = us
                tarea.tiempo= 1
                tarea.save()
            #Generacion del historial
                hist = Historial()
                hist.usuario = user
                hist.fecha_creacion = datetime.today()
                hist.user_story = us
           # hist.documento=docu
                hist.descripcion="Se ha agregado un adjunto " + str(nuevo.nombre)
                hist.save()
                registrar_historial(us,hist,tarea,nuevo)
    	        return HttpResponseRedirect("/userstories&id="+ str(proyect.id) + "/adj&id=" + str(us_id) + "/")
        #return render_to_response('error.html', {'form': form})
    else:
        formset = AdjuntoFormSet()
        return render_to_response('us/add_adjunto.html', {'formset':formset,'us':us, 
                                                                                      'user':user, 'proyecto':proyect,
                                                                                      'abm_items': 'ABM items' in permisos})


@login_required
def quitar_archivo(request, proyecto_id, us_id, arch_id):
    """
	Eliminar un archivo adjunto del proyecto.
	:param request:
	:param proyecto_id:
	:param us_id:
	:param arch_id:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    proyect = get_object_or_404(Proyecto, id=proyecto_id)
    permisos = get_permisos_proyecto(user, proyect)
    us= get_object_or_404(UserStory, id=us_id)
    adjunto = get_object_or_404(Adjunto, id=arch_id)
    if request.method == 'POST':
        archivos = Adjunto.objects.filter(us= us, habilitado=True)      
        adjunto.habilitado = False
        adjunto.save()
        return HttpResponseRedirect('/userstories&id=' + str(proyecto_id) + '/adj&id=' + str(us_id) + '/')
    else:
        return render_to_response('us/quitar_adjunto.html', {'us':us, 'user':user, 'proyecto':proyect,
                                                                                       'abm_items': 'ABM items' in permisos})
@login_required
def retornar_archivo(request, proyecto_id, us_id, arch_id):
    """
	Retorna el archivo adjunto cargado.
	:param request:
	:param proyecto_id:
	:param us_id:
	:param arch_id:
	:return:
    """
    user = User.objects.get(username=request.user.username)
    proyect = get_object_or_404(Proyecto, id=proyecto_id)
    us = get_object_or_404(UserStory, id=us_id)
    permisos = get_permisos_proyecto(user, proyect)
    adjunto = get_object_or_404(Adjunto, id=arch_id)
    if request.method == 'GET':
            respuesta = HttpResponse(base64.b64decode(adjunto.contenido), content_type= adjunto.mimetype)
            respuesta['Content-Disposition'] = 'attachment; filename=' + adjunto.nombre
            respuesta['Content-Length'] = adjunto.tamano
            return respuesta
    mensaje = 'No se pudo traer el archivo'
    return render_to_response('error.html', {'mensaje': mensaje})

@login_required
def cancelar_us(request, proyecto_id, us_id):
    """
	Permite cancelar un user story.	
	:param request:
	:param proyecto_id:
	:param us_id:
	:return:
    """
    user= User.objects.get(username=request.user.username)
    proyecto=Proyecto.objects.get(id=proyecto_id)
    us = UserStory.objects.get(id=us_id)
    us.estado= 'Cancelado'
    us.save()
    histus=HistorialUS()
    histus.us=us
    histus.estado= us.estado
    histus.actividad= us.actividad
    histus.estado_actividad =us.estado_actividad
    histus.flujo = us.flujo
    histus.responsable = us.responsable
    histus.fecha = datetime.today()
    histus.save()
    mensaje= 'Scrum Master:' + str(proyecto.usuario_scrum.usuario.get_full_name()) + str("\n")+ 'Responsable:' + str(us.responsable.get_full_name())+'  El user story: '+ str(us)+ " que pertenece al proyecto " + "'" +str(proyecto.nombre)+"'"+ " ha sido cancelado"
    enviar_correo(request,request.user,mensaje,proyecto.usuario_scrum.usuario.email,us.responsable.email)

    return HttpResponseRedirect("/configuracion&id="+str(proyecto_id)+"/tablero/")


@login_required
def ver_historial_release(request, proyecto_id, us_id):
    """
    Despliega el historial de un user story mostrando la descripcion de las tareas
    agregadas y el nombre de adjuntos cargados
    :param request:
    :param proyecto_id:
    :param us_id:
    :return:
    """
    us = UserStory.objects.get(pk=us_id)
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    perm = get_permisos_proyecto(user, proyecto)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=proyecto).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    #-------------------------------------------------------------------
    versiones = RegistroHistorial.objects.filter(us=us)
    #linea = LineaBase.objects.filter(proyectos=proyect, fase=3)
    #if (linea):
    fin = 0
    #else:
    #    fin = 1
    hist=Historial.objects.filter(user_story=us)
    variables = RequestContext(request, {
                                         'lista': versiones,
                                         'user_story': us,'hist':hist,
                                         'fin': fin,
                                         'proyecto': proyecto,
                                         'ver_historial_user_story': 'Ver historial' in permisos,
                                         'ver_historial_us': 'Ver Historial'})
    return render_to_response('conf/historial_release.html', variables)


def grafico(request,proyecto_id):
    """
	Creación de gráfico para el burndowchart.
	:param request:
	:param proyecto_id:
	:return:
    """
    matplotlib.pyplot.style.use('ggplot')

    x = [5,8,10]
    y = [12,16,6]

    x2 = [6,9,11]
    y2 = [6,15,7]

# can plot specifically, after just showing the defaults:
    plt.plot(x,y,linewidth=5)
    plt.plot(x2,y2,linewidth=5)

    plt.title('Epic Info')
    plt.ylabel('Y axis')
    plt.xlabel('X axis')
    plt.show()

    return HttpResponseRedirect("/configuracion&id="+str(proyecto_id)+"/sprint_bk/")

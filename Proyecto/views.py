#-*- coding: utf-8 -*-
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
from django.contrib import*
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
# Create your views here.
@login_required
def admin_proyectos(request):
    """Administracion general de proyectos"""
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    lista = Proyecto.objects.all().order_by('id')
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            palabra = form.cleaned_data['filtro']
            lista = Proyecto.objects.filter(Q(nombre__icontains = palabra) | Q(descripcion__icontains = palabra) | Q(usuario_scrum__username__icontains = palabra)).order_by('id')
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
            return render_to_response('admin/proyectos/proyectos.html',{'lista':lista, 'pag': pag, 'form':form,
                                                                'user':user,
                                                                'ver_proyectos':'Ver proyectos' in permisos,
                                                                'crear_proyecto': 'Crear proyecto' in permisos,
                                                                'mod_proyecto': 'Modificar proyecto' in permisos,
                                                                'eliminar_proyecto': 'Eliminar proyecto' in permisos},context_instance=RequestContext(request))
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
        return render_to_response('admin/proyectos/proyectos.html',{'lista':lista, 'pag': pag, 'form':form,
                                                                'user':user,
                                                                'ver_proyectos':'Ver proyectos' in permisos,
                                                                'crear_proyecto': 'Crear proyecto' in permisos,
                                                                'mod_proyecto': 'Modificar proyecto' in permisos,

                                                               'eliminar_proyecto': 'Eliminar proyecto' in permisos}, context_instance=RequestContext(request))

@login_required
def crear_proyecto(request):
    """Crea un nuevo proyecto."""
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
        form = ProyectosForm(request.POST, request.FILES)
        if form.is_valid():
            p = Proyecto()
            p.nombre = form.cleaned_data['nombre']
            p.usuario_scrum = form.cleaned_data['usuario_scrum']
            p.descripcion = form.cleaned_data['descripcion']
            p.fecha_inicio = form.cleaned_data['fecha_inicio']
            #p.fecha_fin = form.cleaned_data['fecha_fin']
            #p.cronograma = form.cleaned_data['cronograma']
           # p.fase = Fase.objects.get(pk=1)
           # p.cantidad = form.cleaned_data['cantidad']
	    #p.cant_actual = 0
	    p.save()
            relacion = UsuarioRolProyecto()
            relacion.usuario = p.usuario_scrum.usuario
            relacion.rol = Rol.objects.get(id=2)
            print relacion.rol
            print "chauuu"
            relacion.proyecto = p
            relacion.save()

            # Asociacion inicial de TipoItem a fase por proyecto
            #lista = TipoItem.objects.all()
            #for i in lista:
             #   rel = TipoItemFase()
              #  rel.proyecto = p
              #  rel.fase = i.fase
               # rel.tipo_item = i
               # rel.cant = 1
                #rel.save()

            return HttpResponseRedirect('/proyectos')
    else:
        form = ProyectosForm()
    return render_to_response('admin/proyectos/crear_proyecto.html',{'form':form,
                                                                   'user':user,
                                                                   'crear_proyecto':'Crear proyecto' in permisos}, context_instance=RequestContext(request))


@login_required
def del_proyecto(request, proyecto_id):
    """Eliminar proyecto del sistema"""
    user = User.objects.get(username=request.user.username)
    p = get_object_or_404(Proyecto, id = proyecto_id)
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
        p.delete()
        return HttpResponseRedirect("/proyectos")
    else:
        return render_to_response("admin/proyectos/proyecto_confirm_delete.html", {'proyecto':p,
                                                                                   'eliminar_proyecto': 'Eliminar proyecto' in permisos}, context_instance=RequestContext(request))
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
    """Administracion de proyecto para el modulo de desarrollo."""
    user = User.objects.get(username=request.user.username)
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    permisos = get_permisos_sistema(user)
    print proyecto
    print user
    print permisos
   # permisos_ant = []
   # if proyecto.fase.id == 2:
   #     permisos_ant = get_permisos_proyecto_ant(user, proyecto, Fase.objects.get(pk=1))
    #elif proyecto.fase.id == 3:
     #   permisos_ant = get_permisos_proyecto_ant(user, proyecto, Fase.objects.get(pk=1)) + get_permisos_proyecto_ant(user, proyecto, Fase.objects.get(pk=2))
   # print permisos_ant
   # linea = LineaBase.objects.filter(proyectos=proyecto, fase=3)
    return render_to_response("desarrollo/admin_proyecto.html", {'proyecto':proyecto,
                                                                 'user':user,
                                                               #  'fin':linea,
                                                                 'ver_items': 'Ver items',
                                                                 'abm_items': 'ABM items',
                                                                 'ver_miembros': 'Ver miembros' in permisos,
                                                                 'abm_miembros': 'ABM miembros' in permisos,
                                                                 'asignar_roles': 'Asignar roles' in permisos,
                                                                 'generarlb':'Generar LB',
                                                                 'asignar_tipoItm': 'Asignar tipo-item fase'},context_instance=RequestContext(request) )

@login_required
def admin_usuarios_proyecto(request, proyecto_id):
    """Administración de usuarios del proyecto"""
    user = User.objects.get(username=request.user.username)
    p = Proyecto.objects.get(pk = proyecto_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario = user, proyecto = p).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    #-------------------------------------------------------------------
    miembros = UsuarioRolProyecto.objects.filter(proyecto = p).order_by('id')
    lista = []
    for i in miembros:
        if not i.usuario in lista:
            lista.append(i.usuario)
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            palabra = form.cleaned_data['filtro']
            lista = User.objects.filter(Q(username__icontains = palabra) | Q(first_name__icontains = palabra) | Q(last_name__icontains = palabra)).order_by('id')
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
            return render_to_response('desarrollo/admin_miembros.html',{'lista':lista, 'pag': pag, 'form':form,
                                                                'user':user,
                                                                'proyecto':Proyecto.objects.get(id=proyecto_id),
                                                                'miembros': lista,
                                                                'ver_miembros': 'Ver miembros' in permisos,
                                                                'abm_miembros': 'ABM miembros' in permisos}, context_instance=RequestContext(request))
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
        return render_to_response('desarrollo/admin_miembros.html',{'lista':lista, 'pag': pag, 'form':form,
                                                                'user':user,
                                                                'proyecto':Proyecto.objects.get(id=proyecto_id),
                                                                'miembros': lista,
                                                                'ver_miembros': 'Ver miembros' in permisos,
                                                                'abm_miembros': 'ABM miembros' in permisos}, context_instance=RequestContext(request))

@login_required
def add_usuario_proyecto(request, proyecto_id):
    """Agregar usuarios al proyecto"""
    user = User.objects.get(username=request.user.username)
    p = get_object_or_404(Proyecto, id = proyecto_id)
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
            relacion.proyecto = Proyecto.objects.get(pk = proyecto_id)
            relacion.save()

            return HttpResponseRedirect("/proyectos/miembros&id=" + str(proyecto_id))
    else:
        form = UsuarioProyectoForm(p)
    return render_to_response('desarrollo/add_miembro.html', {'form':form,
                                                              'user':user,
                                                              'proyecto': p,
                                                              'abm_miembros': 'ABM miembros' in permisos}, context_instance=RequestContext(request))

@login_required
def cambiar_rol_usuario_proyecto(request, proyecto_id, user_id):
    """Cambiar rol a un usuario de proyecto"""
    user = User.objects.get(username=request.user.username)
    p = Proyecto.objects.get(pk = proyecto_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario = user, proyecto = p).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    #-------------------------------------------------------------------
    u = User.objects.get(pk = user_id)
    lista = UsuarioRolProyecto.objects.filter(proyecto = p, usuario = u)
    if request.method == 'POST':
        form = AsignarRolesForm(2, request.POST)
        if form.is_valid():
            for i in lista :
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
                dict[i.rol.id] = True
            form = AsignarRolesForm(2,initial = {'roles':dict})
    return render_to_response("desarrollo/cambiar_usuario_rol.html", {'user': user,
                                                                      'form':form,
                                                                      'usuario':u,
                                                                      'proyecto': p,

                                                                      'asignar_roles': 'Asignar roles' in permisos,
                                                                      'abm_miembros':'ABM miembros' in permisos},context_instance=RequestContext(request))

@login_required
def eliminar_miembro_proyecto(request, proyecto_id, user_id):
    """Eliminar miembros del proyecto"""
    user = User.objects.get(username=request.user.username)
    usuario = get_object_or_404(User, pk=user_id)
    proy = get_object_or_404(Proyecto, pk=proyecto_id)
    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario = user, proyecto = proy).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    #-------------------------------------------------------------------
    if request.method == 'POST':
        lista = UsuarioRolProyecto.objects.filter(proyecto = proy, usuario = usuario)
        for i in lista:
            i.delete()
        return HttpResponseRedirect("/proyectos/miembros&id=" + str(proyecto_id))
    else:
        return render_to_response("desarrollo/eliminar_miembro.html", {'usuario':usuario,
                                                                       'proyecto':proy,
                                                                       'user':user,
                                                                       'abm_miembros': 'ABM miembros' in permisos},context_instance=RequestContext(request))


@login_required
def admin_flujos(request):
    """Administracion de flujos para el modulo de desarrollo."""
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    print user
    print permisos
   # permisos_ant = []
   # if proyecto.fase.id == 2:
   #     permisos_ant = get_permisos_proyecto_ant(user, proyecto, Fase.objects.get(pk=1))
    #elif proyecto.fase.id == 3:
     #   permisos_ant = get_permisos_proyecto_ant(user, proyecto, Fase.objects.get(pk=1)) + get_permisos_proyecto_ant(user, proyecto, Fase.objects.get(pk=2))
   # print permisos_ant
   # linea = LineaBase.objects.filter(proyectos=proyecto, fase=3)
    return render_to_response("flujo/admin_flujo.html", {
                                                                 'user':user,
                                                               #  'fin':linea,
                                                                 'ver_items': 'Ver items',
                                                                 'abm_items': 'ABM items',
                                                                 'ver_miembros': 'Ver miembros' in permisos,
                                                                 'abm_miembros': 'ABM miembros' in permisos,
                                                                 'asignar_roles': 'Asignar roles' in permisos,
                                                                 'generarlb':'Generar LB',
                                                                 'asignar_tipoItm': 'Asignar tipo-item fase'},context_instance=RequestContext(request) )

@login_required
def mod_proyecto(request, proyecto_id):
    """Modificar Proyecto"""
    user = User.objects.get(username=request.user.username)
    p = get_object_or_404(Proyecto, id = proyecto_id)
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
        form = ModProyectosForm(p, request.POST, request.FILES)
        if form.is_valid():
                p.nombre = form.cleaned_data['nombre']

                relacion = UsuarioRolProyecto.objects.filter(usuario = User.objects.get(pk = p.usuario_scrum.usuario_id), proyecto = p, rol = Rol.objects.get(pk=2))
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
        form = ModProyectosForm(p, initial = {'nombre': p.nombre,

                                        'descripcion': p.descripcion,
                                      })
    return render_to_response('admin/proyectos/mod_proyecto.html',{'form':form,
                                                                   'user':user,
                                                                   'proyecto': p,
                                                                   'mod_proyecto':'Modificar proyecto' in permisos}, context_instance=RequestContext(request))

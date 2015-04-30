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
Crea un nuevo proyecto.
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
            p.product_owner = form.cleaned_data['product_owner']
            p.descripcion = form.cleaned_data['descripcion']
            p.fecha_inicio = form.cleaned_data['fecha_inicio']
            p.sprint = form.cleaned_data['sprint']
            p.save()
            relacion = UsuarioRolProyecto()
            relacion.usuario = p.usuario_scrum.usuario
            relacion.rol = Rol.objects.get(id=2)
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
Eliminar proyecto del sistema
:param request:
:param proyecto_id:
:return:
"""
    """"""
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
Administracion de proyecto
:param request:
:param proyecto_id:
:return:
"""

    user = User.objects.get(username=request.user.username)
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    permisos = get_permisos_sistema(user)
    #perm = get_permisos_proyecto(user, proyecto_id)
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
    return render_to_response("desarrollo/admin_proyecto.html", {'proyecto': proyecto,
                                                                 'user': user,
                                                                 #  'fin':linea,
                                                                 'ver_flujos': 'Ver flujos' in permisos,
                                                                 'ver_user_story': 'Ver user story' in permisos,
                                                                 # 'ver_us': 'Ver US' in perm,
                                                                 #'ver_Flujos': 'Ver Flujos' in perm,
                                                                 'ver_miembros': 'Ver miembros' in permisos,
                                                                 'abm_miembros': 'ABM miembros' in permisos,
                                                                 'asignar_roles': 'Asignar roles' in permisos,
                                                                 'generarlb': 'Generar LB',
                                                                 'asignar_tipoItm': 'Asignar tipo-item fase'},
                              context_instance=RequestContext(request))


@login_required
def admin_usuarios_proyecto(request, proyecto_id):
    """
Administración de usuarios del proyecto
:param request:
:param proyecto_id:
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
    miembros = UsuarioRolProyecto.objects.filter(proyecto=p).order_by('id')
    lista = []
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
            return render_to_response('desarrollo/admin_miembros.html', {'lista': lista, 'pag': pag, 'form': form,
                                                                         'user': user,
                                                                         'proyecto': Proyecto.objects.get(
                                                                             id=proyecto_id),
                                                                         'miembros': lista,
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
        return render_to_response('desarrollo/admin_miembros.html', {'lista': lista, 'pag': pag, 'form': form,
                                                                     'user': user,
                                                                     'proyecto': Proyecto.objects.get(id=proyecto_id),
                                                                     'miembros': lista,
                                                                     'ver_miembros': 'Ver miembros' in permisos,
                                                                     'abm_miembros': 'ABM miembros' in permisos},
                                  context_instance=RequestContext(request))


@login_required
def add_usuario_proyecto(request, proyecto_id):
    """
Agregar usuarios al proyecto
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
Cambiar rol a un usuario de proyecto
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
                dict[i.rol.id] = True
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
Eliminar miembros del proyecto
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
    Modificacion de Proyectos
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
Administracion de flujos
:param request:
:param proyecto_id:
:return:
"""
    user = User.objects.get(username=request.user.username)
    proyectos = Proyecto.objects.get(id=proyecto_id)
    permisos = get_permisos_sistema(user)
    print user
    print permisos
    lista = Flujo.objects.filter(proyecto=proyectos)
    actividades = Actividades.objects.filter(proyecto=proyecto_id)
    print actividades
    return render_to_response("flujo/admin_flujo.html", {
        'user': user, 'lista': lista, 'proyecto': proyectos, 'actividades': actividades,
        'mod_acti': 'Modificar actividad' in permisos, 'ver_flujos': 'Ver flujos' in permisos,
        'crear_flujos': 'Crear flujos' in permisos, 'ver_actividades': 'Ver actividades' in permisos,
        'crear_actividades': 'Crear actividades' in permisos,

    }, context_instance=RequestContext(request))


@login_required
def crear_flujos(request,proyecto_id):
    """
    Agrega un nuevo flujo
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
Agrega una nueva actividad een el proyecto
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
Adhiere actividades a un flujo dado
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
    if request.method == 'POST':
        form = AddActividadesForm(proyecto, request.POST)
        print "ktkkk"
        if form.is_valid():
            lista_nueva = form.cleaned_data['actividades']
            for i in lista_actividades:
               i.delete()

            print "chau"
            for j in lista_nueva:
                nuevo = ActividadesFlujo()
                nuevo.flujo = flujo
                nuevo.actividades = j
                nuevo.proyecto = proyecto
                nuevo.save()
                print "holaaa"
                print nuevo
            return HttpResponseRedirect("/flujos&id=" + str(proyecto_id))
    else:
        print "chauuuuuuuuuuu"
        dict = {}
        for i in lista_actividades:
            dict[i.actividades.id] = True
        form = AddActividadesForm(proyecto, initial={'actividades': dict})
    return render_to_response("flujo/add_actividades.html",
                              {'form': form, 'user': user, 'flujo': flujo, 'proyecto': proyecto,
                               'add_actividades': 'Agregar Actividades' in perm},
                              context_instance=RequestContext(request))


@login_required
def ver_actividades(request, proyecto_id, flujo_id):
    """
Visualizar las actividades
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
    Muestra la pagina de administracion de user stories.
    :param request:
    :param proyecto_id:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    #proyecto= get_object_or_404(Proyecto, id = proyecto_id)
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    #linea = LineaBase.objects.filter(proyectos=proyect, fase=proyect.fase)
    perm = get_permisos_proyecto(user, proyecto)
    permisos = get_permisos_sistema(user)
    lista = UserStory.objects.filter(habilitado=True).order_by('id')
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
                                             'revisar_user_story': 'Revisar user story'})
        return render_to_response('us/user_story.html', variables)

@login_required
def crear_user_story(request,proyecto_id):
    """
Agrega un nuevo us
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

            us.estado = 1
            us.version = 1
            us.valor_negocio=form.cleaned_data['valor_negocio']
            us.valor_tecnico=form.cleaned_data['valor_tecnico']
            us.prioridad = form.cleaned_data['prioridad']
            us.descripcion = form.cleaned_data['descripcion']
            us.habilitado = True
            us.proyecto = proyecto
            us.duracion = form.cleaned_data['duracion']
            us.save()

            #Generacion del historial
            hist = Historial()
            hist.usuario = user
            hist.fecha_creacion = datetime.date.today()
            hist.user_story = us
            hist.save()
            return HttpResponseRedirect("/userstories&id=" + str(proyecto_id) + "/")
    else:
        form = UserStoryForm()
    return render_to_response('us/crear_user_story.html',{'proyecto': proyecto,
            'form': form,
            'abm_user_story': 'ABM user story' in permisos,
            'crear_us': 'Crear US' in perm},context_instance=RequestContext(request))



@login_required
def eecrear_user_story(request, proyecto_id):
    """
    Crear un User Story"
    :param request:
    :param proyecto_id:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    proyecto = Proyecto.objects.get(pk=proyecto_id)

    #Validacion de permisos---------------------------------------------
    roles = UsuarioRolProyecto.objects.filter(usuario=user, proyecto=proyecto).only('rol')
    perm = get_permisos_proyecto(user, proyecto)
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    #-------------------------------------------------------------------
    if request.method == 'POST':
        form = UserStoryForm(proyecto_id, request.POST, request.FILES)
        if form.is_valid():
            us = UserStory()
            us.nombre = form.cleaned_data['nombre']
            #us.usuario = form.cleaned_data['usuario']  #solo en el historial?

            us.estado = 1
            us.version = 1
            us.valor_negocio=form.cleaned_data['valor_negocio']
            us.valor_tecnico=form.cleaned_data['valor_tecnico']
            us.prioridad = form.cleaned_data['prioridad']
            us.descripcion = form.cleaned_data['descripcion']
            us.habilitado = True
            us.proyecto = proyecto
            us.duracion = form.cleaned_data['duracion']
            us.save()

            #Generacion del historial
            hist = Historial()
            hist.usuario = user
            hist.fecha_creacion = datetime.date.today()
            hist.user_story = us
            hist.save()
            return HttpResponseRedirect("/userstories&id=" + str(proyecto_id) + "/")
    else:
        form = UserStoryForm(proyecto)

        variables = RequestContext(request, {
            'proyecto': proyecto,
            'form': form,
            'abm_user_story': 'ABM user story' in permisos,
            'crear_us': 'Crear US' in perm})
        return render_to_response('us/crear_user_story.html', variables)



@login_required
def ver_historial(request, proyecto_id, us_id):
    """
Ver historial
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
    historial = Historial.objects.get(user_story=us)
    versiones = RegistroHistorial.objects.filter(historial=historial).order_by('version')
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


@login_required
def mod_user_story(request, proyecto_id, us_id):
    """Modifica los datos de un usuario y los actualiza en el sistema"""
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
            return HttpResponseRedirect("/userstories&id=" + str(us_id))
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
    """Modifica los datos de una actividad y los actualiza en el sistema"""
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
def conf_proyecto(request, proyecto_id):
    """
 :param request:
 :param proyecto_id:
 :return:
 """
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    flujos= Flujo.objects.filter(proyecto=proyecto_id)
    act =0
    for i in flujos:
        actividad= ActividadesFlujo.objects.filter(flujo=i)
        if actividad:
            print actividad
            act=1
    if act is not 0:
        return render_to_response('conf/config_inicial.html', {'lista': proyecto,
                                                                   'proyecto':proyecto,
                                                                   'user': user,
                                                                   'ver_proyectos': 'Ver proyectos' in permisos,
                                                                   'crear_proyecto': 'Crear proyecto' in permisos,
                                                                   'mod_proyecto': 'Modificar proyecto' in permisos,
                                                                   'ver_flujos': 'Ver flujos' in permisos,
                                                                   'eliminar_proyecto': 'Eliminar proyecto' in permisos},
                                                                     context_instance=RequestContext(request))

    else:
        return HttpResponse("Debe agregar por lo menos un flujo con una actividad para  iniciar el proyecto")


#----------->Generar Equipo
@login_required
def admin_equipo(request,proyecto_id):
    """
Dirigue a la interfaz, para la creacion de equipos de trabajo  para el sprint dado
:param request:
:param proyecto_id:
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
    miembros = Equipo.objects.filter(sprint=1).order_by('id')
    lista = []
    listah=[]

    for i in miembros:
        if not i.usuario in lista:
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
            return render_to_response('conf/admin_equipo.html', {'lista': lista, 'pag': pag, 'form': form,
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
        return render_to_response('conf/admin_equipo.html', {'lista': lista, 'pag': pag, 'form': form,
                                                                     'user': user,
                                                                     'proyecto': Proyecto.objects.get(id=proyecto_id),
                                                                     'miembros': miembros, #este fue cambiado de lista a miembros
                                                                     'ver_miembros': 'Ver miembros' in permisos,
                                                                     'abm_miembros': 'ABM miembros' in permisos},
                                  context_instance=RequestContext(request))

@login_required
def add_miembro_equipo(request, proyecto_id):
    """
Agregar usuarios al equipo
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
        form = MiembroEquipoForm(p, request.POST)
        if form.is_valid():
            relacion = Equipo()
            relacion.usuario = form.cleaned_data['usuario']
            relacion.proyecto = Proyecto.objects.get(pk=proyecto_id)
            relacion.sprint=1
            relacion.horas=form.cleaned_data['horas']
            relacion.save()

            return HttpResponseRedirect("/configuracion/equipo&id=" + str(proyecto_id))
    else:
        form = MiembroEquipoForm(p)
    return render_to_response('conf/add_miembroE.html', {'form': form,
                                                              'user': user,
                                                              'proyecto': p,
                                                              'abm_miembros': 'ABM miembros' in permisos,
                                                              'asignar_roles': 'Asignar roles'},
                              context_instance=RequestContext(request))


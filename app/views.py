"""VIEWS DE LA ADMINISTRACION GENERAL """
#-*- coding: utf-8 -*-
import base64
from django.views.decorators.csrf import csrf_protect
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
from app.forms import *
from app.models import *
from app.helper import *
from django.contrib.auth.forms import UserCreationForm

@login_required
@csrf_protect
def principal(request):
    """Muestra la pagina principal del sistema"""
    user = User.objects.get(username=request.user.username)
     #Validacion de permisos---------------------------------------------
    roles = UsuarioRolSistema.objects.filter(usuario = user).only('rol')
    print roles
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos_sistema = []
    for i in permisos_obj:
        permisos_sistema.append(i.nombre)
    variables ={}
    for i in permisos_sistema:
        if i == 'Ver roles' or i == 'Crear rol' or i == 'Modificar rol' or i == 'Eliminar rol' or i == 'Asignar rol':
            variables['roles'] = True

        if i == 'Ver usuarios' or i == 'Crear usuario' or i == 'Modificar usuario' or i == 'Eliminar usuario':
            variables['usuarios'] = True
	if i == 'Ver proyectos' or i == 'Crear proyecto' or i == 'Modificar proyecto' or i == 'Eliminar proyecto':
    	    variables['proyectos'] = True
    variables['user'] = user
    print variables
    rolesp = UsuarioRolProyecto.objects.filter(usuario = user).only('rol')
    lista_proyectos = []
    for i in rolesp:
        if not i.proyecto.id in lista_proyectos:
            lista_proyectos.append(i.proyecto.id)
    #variables['acciones']=True
    print lista_proyectos
    variables['permisos_proyecto'] = lista_proyectos
    #-------------------------------------------------------------------
    lista = Proyecto.objects.all()
    variables['lista'] = lista
    return render_to_response('main_page.html', variables, context_instance=RequestContext(request))



@login_required
def add_user(request):
    """Agrega un nuevo usuario en el sistema."""
    user = User.objects.get(username=request.user.username)
    #Validacion de permisos----------------------------------------------
    roles = UsuarioRolSistema.objects.filter(usuario = user).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    #--------------------------------------------------------------------
    #Agrega los datos del nuevo usuario
    if request.method == 'POST':
        form = UsuariosForm(request.POST)
        if form.is_valid():
            nuevo=User()

            nuevo.username = form.cleaned_data['username']
            nuevo.first_name = form.cleaned_data['first_name']
            nuevo.last_name = form.cleaned_data['last_name']
            nuevo.email = form.cleaned_data['email']
            nuevo.set_password(form.cleaned_data['password'])
            nuevo.is_staff = True
            nuevo.is_active = True

            nuevo.is_superuser = True
            nuevo.last_login = datetime.datetime.now()
            nuevo.date_joined = datetime.datetime.now()
            nuevo.save()
            return HttpResponseRedirect("/usuarios")
    else:
        form = UsuariosForm()
    return render_to_response('admin/usuarios/crear_usuario.html',{'form':form,
                                                                  'user':user,
                                                                 'crear_usuario': 'Crear usuario' in permisos}, context_instance=RequestContext(request))

@login_required
def mod_user(request, usuario_id):
    """Modifica los datos de un usuario y los actualiza en el sistema"""
    user = User.objects.get(username=request.user.username)
    #Validacion de permisos----------------------------------------------
    roles = UsuarioRolSistema.objects.filter(usuario = user).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    #--------------------------------------------------------------------
    usuario = get_object_or_404(User, id=usuario_id)
    #Datos nuevos del usuario
    if request.method == 'POST':
        form = ModUsuariosForm(request.POST)
        if form.is_valid():
            usuario.first_name = form.cleaned_data['first_name']
            usuario.last_name = form.cleaned_data['last_name']
            usuario.email = form.cleaned_data['email']
            usuario.save()
            return HttpResponseRedirect("/usuarios")
    else:
        form = ModUsuariosForm(initial={'first_name':usuario.first_name, 'last_name': usuario.last_name,'email':usuario.email})
    return render_to_response('admin/usuarios/mod_usuario.html',{'form':form,
                                                                 'user':user,
                                                                 'usuario':usuario,
                                                                 'mod_usuario': 'Modificar usuario' in permisos},context_instance=RequestContext(request))

@login_required
def cambiar_password(request):
    """Cambia la contrasena del usuario logueado y lo direge a la pagina principal"""
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = CambiarPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return HttpResponseRedirect("/")
    else:
        form = CambiarPasswordForm()
    return render_to_response('admin/usuarios/cambiar_password.html', {'form': form, 'user': user},context_instance=RequestContext(request))

@login_required
def asignar_roles_sistema(request, usuario_id):
    """Asigna roles de sistema a un usuario"""
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    usuario = get_object_or_404(User, id=usuario_id)
    lista_roles = UsuarioRolSistema.objects.filter(usuario = usuario)
    lista_permisos = RolPermiso.objects.filter()

    print lista_permisos
    tam=len(lista_permisos)
    print tam
    if request.method == 'POST':
        form = AsignarRolesForm(1, request.POST)
        if form.is_valid():
            lista_nueva = form.cleaned_data['roles']
            for i in lista_roles:
                i.delete()
            for i in lista_nueva:
                nuevo = UsuarioRolSistema()
		rel = RolUsuario()
                nuevo.usuario = usuario
                nuevo.rol = i
		nuevo.save()
		if i.id == 2:
			rel.usuario = usuario

			rel.save()

            return HttpResponseRedirect("/usuarios")
    else:
        if usuario.id == 1:
            error = "No se puede editar roles sobre el superusuario."
            return render_to_response("admin/usuarios/asignar_roles.html", {'mensaje': error,
                                                                            'usuario':usuario,
                                                                            'user': user,
                                                                            'asignar_roles': 'Asignar rol' in permisos},context_instance=RequestContext(request))
        dict = {}
        for i in lista_roles:
            print i.rol
            dict[i.rol.id] = True
        form = AsignarRolesForm(1,initial = {'roles': dict})
    return render_to_response("admin/usuarios/asignar_roles.html", {'form':form, 'usuario':usuario, 'user':user, 'asignar_roles': 'Asignar rol' in permisos},context_instance=RequestContext(request))

@login_required
def borrar_usuario(request, usuario_id):
    """Borra un usuario, comprobando las dependencias primero"""
    user = User.objects.get(username=request.user.username)
    #Validacion de permisos----------------------------------------------
    roles = UsuarioRolSistema.objects.filter(usuario = user).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    print permisos
    #--------------------------------------------------------------------
    usuario = get_object_or_404(User, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return HttpResponseRedirect("/usuarios")
    else:
        if usuario.id == 1:
            error = "No se puede borrar al superusuario."
            return render_to_response("admin/usuarios/user_confirm_delete.html", {'mensaje': error,'usuario':usuario, 'user': user, 'eliminar_usuario': 'Eliminar usuario' in permisos},context_instance=RequestContext(request))

    return render_to_response("admin/usuarios/user_confirm_delete.html", {'usuario':usuario,
                                                                          'user':user,
                                                                          'eliminar_usuario': 'Eliminar usuario' in permisos},context_instance=RequestContext(request))



@login_required
def admin_usuarios(request):
    """Administracion general de usuarios"""
    '''Ya esta la validacion de permisos en este'''
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    lista = User.objects.all().order_by("id")
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
            return render_to_response('admin/usuarios/usuarios.html',{'pag': pag,
                                                               'form': form,
                                                               'lista':lista,
                                                               'user':user,
                                                               'ver_usuarios': 'Ver usuarios' in permisos,
                                                               'crear_usuario': 'Crear usuario' in permisos,
                                                               'mod_usuario': 'Modificar usuario' in permisos,
                                                               'eliminar_usuario': 'Eliminar usuario' in permisos,
                                                               'asignar_roles': 'Asignar rol' in permisos},context_instance=RequestContext(request))
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
    return render_to_response('admin/usuarios/usuarios.html',{ 'pag':pag,
                                                               'form': form,
                                                               'lista':lista,
                                                               'user':user,
                                                               'ver_usuarios': 'Ver usuarios' in permisos,
                                                               'crear_usuario': 'Crear usuario' in permisos,
                                                               'mod_usuario': 'Modificar usuario' in permisos,
                                                               'eliminar_usuario': 'Eliminar usuario' in permisos,
                                                               'asignar_roles': 'Asignar rol' in permisos},context_instance=RequestContext(request))


@login_required
def admin_roles(request):
    """Administracion general de roles"""
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    return render_to_response('admin/roles/roles.html',{'user':user,
                                                        'ver_roles':'Ver roles' in permisos,
                                                        'crear_rol': 'Crear rol' in permisos,
                                                        'mod_rol': 'Modificar rol' in permisos,
                                                        'eliminar_rol': 'Eliminar rol' in permisos},context_instance=RequestContext(request))
@login_required
def admin_roles_sist(request):
    """Administracion general de roles"""
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    lista = Rol.objects.filter(categoria=1).order_by('id')
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            palabra = form.cleaned_data['filtro']
            lista = Rol.objects.filter(Q(categoria = 1), Q(nombre__icontains = palabra) | Q(descripcion__icontains = palabra) | Q(usuario_creador__username__icontains = palabra)).order_by('id')
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
            return render_to_response('admin/roles/roles_sistema.html',{'lista':lista, 'form': form,
                                                        'user':user, 'pag': pag,
                                                        'ver_roles':'Ver roles' in permisos,
                                                        'crear_rol': 'Crear rol' in permisos,
                                                        'mod_rol': 'Modificar rol' in permisos,
                                                        'eliminar_rol': 'Eliminar rol' in permisos},context_instance=RequestContext(request))
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
    return render_to_response('admin/roles/roles_sistema.html',{'lista':lista, 'form':form,
                                                            'user':user, 'pag': pag,
                                                            'ver_roles':'Ver roles' in permisos,
                                                            'crear_rol': 'Crear rol' in permisos,
                                                            'mod_rol': 'Modificar rol' in permisos,
                                                            'eliminar_rol': 'Eliminar rol' in permisos},context_instance=RequestContext(request))

@login_required
def admin_roles_proy(request):
    """Administracion general de roles"""
    user = User.objects.get(username=request.user.username)
    permisos = get_permisos_sistema(user)
    lista = Rol.objects.filter(categoria=2).order_by('id')
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            palabra = form.cleaned_data['filtro']
            lista = Rol.objects.filter(Q(categoria = 2), Q(nombre__icontains = palabra) | Q(descripcion__icontains = palabra) | Q(usuario_creador__username__icontains = palabra)).order_by('id')
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
            return render_to_response('admin/roles/roles_sistema.html',{'lista':lista,'form':form,
                                                        'user':user, 'pag': pag,
                                                        'ver_roles':'Ver roles' in permisos,
                                                        'crear_rol': 'Crear rol' in permisos,
                                                        'mod_rol': 'Modificar rol' in permisos,
                                                        'eliminar_rol': 'Eliminar rol' in permisos},context_instance=RequestContext(request))
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
    return render_to_response('admin/roles/roles_proyecto.html',{'lista':lista,'form':form,
                                                        'user':user,'pag': pag,
                                                        'ver_roles':'Ver roles' in permisos,
                                                        'crear_rol': 'Crear rol' in permisos,
                                                        'mod_rol': 'Modificar rol' in permisos},context_instance=RequestContext(request))



@login_required
def crear_rol(request):
    """Agrega un nuevo rol"""
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
        form = RolesForm(request.POST)
        if form.is_valid():
            r = Rol()
            r.nombre = form.cleaned_data['nombre']
            r.descripcion = form.cleaned_data['descripcion']
            r.fecHor_creacion = datetime.datetime.now()
            r.usuario_creador = user
            r.categoria = form.cleaned_data['categoria']
            r.save()
            if r.categoria == "1":
               return HttpResponseRedirect("/roles/sist")
            return HttpResponseRedirect("/roles/proy")
    else:
        form = RolesForm()
    return render_to_response('admin/roles/crear_rol.html',{'form':form,
                                                            'user':user,
                                                            'crear_rol': 'Crear rol' in permisos},context_instance=RequestContext(request))

@login_required
def admin_permisos(request, rol_id):
    """Administracion general de permisos que pueden ser asignados"""
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
    actual = get_object_or_404(Rol, id=rol_id)
    if request.method == 'POST':
        if actual.categoria == 1:
            form = PermisosForm(request.POST)
        else:
            form = PermisosProyectoForm(request.POST)
        if form.is_valid():
               actual.permisos.clear()
               if actual.categoria == 1:
                  lista = form.cleaned_data['permisos']
                  for i in lista:
                    nuevo = RolPermiso()
                    nuevo.rol = actual
                    nuevo.permiso = i
                    nuevo.save()
               else:
                    lista_req = form.cleaned_data['permisos1']
                    lista_dis = form.cleaned_data['permisos2']
                    lista_impl = form.cleaned_data['permisos3']
                    for i in lista_req:
                      nuevo = RolPermiso()
                      nuevo.rol = actual
                      nuevo.permiso = i
                    #nuevo.fase = Fase.objects.get(pk=1)
                      nuevo.save()
                    for i in lista_dis:
                      nuevo = RolPermiso()
                      nuevo.rol = actual
                      nuevo.permiso = i
                    #nuevo.fase = Fase.objects.get(pk=2)
                      nuevo.save()
                    for i in lista_impl:
                      nuevo = RolPermiso()
                      nuevo.rol = actual
                      nuevo.permiso = i

                      nuevo.save()
        return HttpResponseRedirect("/roles/sist")
    else:

        if actual.categoria == 1:
            dict = {}

            for i in actual.permisos.all():
                dict[i.id] = True
            form = PermisosForm(initial={'permisos': dict})

    return render_to_response("admin/roles/admin_permisos.html", {'form': form,
                                                                  'rol': actual,
                                                                  'user':user,
                                                                  'mod_rol':'Modificar rol' in permisos},context_instance=RequestContext(request))


def mod_rol(request, rol_id):
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
    actual = get_object_or_404(Rol, id=rol_id)
    if request.method == 'POST':
        form = ModRolesForm(request.POST)
        if form.is_valid():
            actual.descripcion = form.cleaned_data['descripcion']
            actual.save()
            if actual.categoria == 1:
               return HttpResponseRedirect("/roles/sist")
            return HttpResponseRedirect("/roles/proy")
    else:
        if actual.id == 1:
            error = "No se puede modificar el rol de superusuario"
            return render_to_response("admin/roles/abm_rol.html", {'mensaje': error, 'rol':actual, 'user':user},context_instance=RequestContext(request))
        form = ModRolesForm()
        form.fields['descripcion'].initial = actual.descripcion
    return render_to_response("admin/roles/mod_rol.html", {'user':user,
                                                           'form':form,
							   'rol': actual,
                                                           'mod_rol':'Modificar rol' in permisos},context_instance=RequestContext(request))


@login_required
def borrar_rol(request, rol_id):
    """Borra un rol con las comprobaciones de consistencia"""
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
    #-------------------------------------------------------
    actual = get_object_or_404(Rol, id=rol_id)
    #Obtener todas las posibles dependencias
    if actual.categoria == 1:
        relacionados = UsuarioRolSistema.objects.filter(rol = actual).count()
    elif actual.categoria == 2:
        relacionados = UsuarioRolProyecto.objects.filter(rol = actual).count()
    if request.method == 'POST':
        actual.delete()
        if actual.categoria == 1:
           return HttpResponseRedirect("/roles/sist")
        return HttpResponseRedirect("/roles/proy")
    else:
        if actual.id == 1:
            error = "No se puede borrar el rol de superusuario"
            return render_to_response("admin/roles/rol_confirm_delete.html", {'mensaje': error,
                                                                              'rol':actual,
                                                                              'user':user,
                                                                              'eliminar_rol':'Eliminar rol' in permisos},context_instance=RequestContext(request))
        if relacionados > 0:
            error = "El rol se esta utilizando."
            return render_to_response("admin/roles/rol_confirm_delete.html", {'mensaje': error,
                                                                              'rol':actual,
                                                                              'user':user,
                                                                              'eliminar_rol':'Eliminar rol' in permisos},context_instance=RequestContext(request))
    return render_to_response("admin/roles/rol_confirm_delete.html", {'rol':actual,
                                                                      'user':user,
                                                                      'eliminar_rol':'Eliminar rol' in permisos},context_instance=RequestContext(request))


@login_required
def terminar(peticion):
    """Muestra una pagina de confirmacion de exito"""
    return render_to_response('operacion_exitosa.html');

def login_redirect(request):
    """Redirige de /accounts/login a /login."""
    return HttpResponseRedirect('/login')

def logout_pagina(request):
    """Pagina de logout"""
    try:
        del request.session['nro_items']
    except KeyError:
        pass

    logout(request)
    return HttpResponseRedirect('/')



def index_view(request):
	return render_to_response('index.html', context_instance=RequestContext(request))
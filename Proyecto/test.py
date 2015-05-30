from django.test import TestCase,RequestFactory
from django.core.urlresolvers import reverse
from django.utils import timezone
from app.forms import *
import unittest
from django.contrib.auth.models import User
from django.test import Client
from app.models import *
from app.views import *
import datetime
# tere
#*******************************************PRUEBAS DE VISTAS*************************************************
class TestLlamadas(TestCase):
    def setUp(self):
    	self.c = Client()
    	self.user = User.objects.create_user(username="test", email="test@test.com", password="test")
#-->LOGIN
    def test_llama_carga_vistas(self):
	self.client.login(username='user', password='test')
	response = self.client.get('/login/')
	self.assertEqual(response.status_code, 200)
	self.assertTemplateUsed(response, 'registration/login.html')
	print('login-OK')
#-->PRINCIPAL
    def test_llama_vista_principal(self):
	response = self.client.get('/')
	self.assertEqual(response.status_code, 200)
	self.assertTemplateUsed(response, 'index.html')
	t=response.content
#-->ADMIN_USUARIOS
    def test_agregar_user(self):
	response = self.client.get('/usuarios/')
	self.assertEqual(response.status_code, 302)
    	self.client.login(username='test', password='test')
    	data = {'text': 'Test text', 'title': 'Test title'}
    	data['user'] = self.user.id
    	self.assertEqual(User.objects.count(), 1)
    	self.assertEqual(response.status_code, 302)
#--->ADMIN_PROYECTOS
    def test_llama_vista_principal(self):
	# {'ver_usuarios': 'Ver usuarios','crear_usuario': 'Crear usuario',}
	response =self.client.post('admin/proyectos/proyectos.html')
	self.assertEqual(response.status_code, 404)
	print('admin_proyectos-OK')
#--->USERSTORIES
    def test_ver_productbk(self):
        response=self.client.post('us/user_story.html')
        self.assertEqual(response.status_code, 404)
    def test_ver_sprintbk(self):
        response=self.client.post('conf/admin_sprint.html')
        self.assertEqual(response.status_code, 404)
    def test_ver_flujos(self):
        response=self.client.post('flujo/admin_flujo.html')
        self.assertEqual(response.status_code, 404)
    def test_ver_miembros(self):
        response=self.client.post('desarrollo/admin_miembros.html')
        self.assertEqual(response.status_code, 404)

class TestVistas(unittest.TestCase):
    def setUp(self):
        self.client = Client()
    def test_responseCrearProyecto(self):
        response = self.client.get('admin/proyectos/crear_proyecto.html')
        self.assertEqual(response.status_code, 404)
        user = User.objects.create(username='AnonymousUser')
class TestAaLogueo(TestCase):
    def test_ap_page(self):
	c = Client()
	response = c.post('/login/',{'username':'admin','password':'12345'})
	response.status_code
	self.assertEqual(response.status_code, 200)
	response = c.get('/principal')
	response.content
	print('El usuario, admin se logueo correctamente')


#********************************************PRUEBAS DE MODELOS*************************************************
#------------------------------------PROYECTO-------------------------------------------#
class TestAdminProyecto(TestCase):
    def add_proyecto(self, nombre='test',descripcion='test'):
        scrum = RolUsuario(1)
        fecha = datetime.date(day=01,month=03,year=2015)
        P = Proyecto.objects.create(nombre=nombre,usuario_scrum=scrum,descripcion=descripcion,fecha_inicio=fecha)
        return P
    def test_valido_form(self):
    	w = self.add_proyecto(nombre='Foo',descripcion='hola')
    	data = {'nombre': w.nombre, 'descripcion': w.descripcion,'fecha_inicio':w.fecha_inicio,'sprint':1}
	form = 	ProyectosForm(data=data)
    	self.assertFalse(form.is_valid())#formulario
    def test_cantidad_proyectos(self):
	p1=self.add_proyecto(nombre='p1')
    	p2=self.add_proyecto(nombre='p2')
    	self.assertEqual(Proyecto.objects.count(), 2)
    def test_add_proyecto(self):
        u = self.add_proyecto(nombre='test')
        self.assertTrue(isinstance(u,Proyecto))
        self.assertEqual(u.__unicode__(), u.nombre)
        print('Test de crear Proyecto, exitoso')
#-------------------------------FLUJOS & ACTIVIDADES-----------------------------------------#
#--Flujos
class TestAdminFlujos(TestCase):
    def add_proyecto(self, nombre='test',descripcion='test'):
        scrum = RolUsuario(1)
        fecha = datetime.date(day=01,month=03,year=2015)
        P = Proyecto.objects.create(nombre=nombre,usuario_scrum=scrum,descripcion=descripcion,fecha_inicio=fecha)
        return P
    def add_Flujo(self,nombre='test'):
	proyecto = self.add_proyecto(nombre='test')
	flujo = Flujo.objects.create(nombre = nombre,proyecto=proyecto)
        return flujo
    def test_add_Flujo(self):
        f = self.add_Flujo(nombre='test')
        self.assertTrue(isinstance(f,Flujo))
        self.assertEquals(f.__unicode__(),f.nombre)
        print('Test de crear Flujo, exitoso')
    def test_valido_form(self):
    	w = self.add_Flujo(nombre='Flujo1')
    	data = {'nombre': w.nombre}
	form = 	FlujosForm(data=data)
    def test_flujoUS(self):
        flujo=Flujo()
        us = UserStory()
        fu=flujoUS(flujo=flujo,us=us)
        isinstance(fu,flujoUS)

#--Actividades
class TestAdminActividades(TestCase):
    def add_proyecto(self, nombre='test',descripcion='test'):
        scrum = RolUsuario(1)
        fecha = datetime.date(day=01,month=03,year=2015)
        P = Proyecto.objects.create(nombre=nombre,usuario_scrum=scrum,descripcion=descripcion,fecha_inicio=fecha)
        return P
    def add_Actividad(self,nombre='test'):
        actividad = Actividades.objects.create(nombre = nombre)
        return actividad
    def test_valido_form(self):
    	w = self.add_Actividad(nombre='Act1')
    	data = {'nombre': w.nombre}
	form = 	ActividadesForm(data=data)
    	#elf.assertFalse(form.is_valid())
	print('formulario valido')
    def test_add_Actividad(self):
        f = self.add_Actividad(nombre='test')
        self.assertTrue(isinstance(f,Actividades))
        self.assertEquals(f.__unicode__(),f.nombre)
	print('Test de crear Actividades, exitoso')
    def add_Actividad(self,nombre='test'):
	p = self.add_proyecto(nombre='test')
        actividad = Actividades.objects.create(nombre = nombre,estado='To Do',proyecto=p)
        return actividad
    def test_add_flujoAc(self,nombre='flujo'):
        proyecto = self.add_proyecto(nombre='test')
	flujo = Flujo.objects.create(nombre = nombre,proyecto=proyecto)
	print('Test asignar actividad a flujo, exitoso')
	return flujo
#-----------------------------------USER STORY--------------------------------------------------#
    def add_us(self,nombre='test',version='1',descripcion='descripcion',estado='1',prioridad='1',habilitado=True,duracion='1',valor_tecnico='1',valor_negocio='1'):
        estado=estado
        proyecto = self.add_proyecto(nombre='test')
        US = UserStory.objects.create(nombre=nombre,version=version,descripcion=descripcion,estado=estado,prioridad=prioridad,habilitado=habilitado,duracion=duracion,proyecto=proyecto,valor_tecnico=valor_tecnico,valor_negocio=valor_negocio)
        return US
    def test_add_us(self):
        f = self.add_us(nombre='test')
        self.assertTrue(isinstance(f,UserStory))
        self.assertEquals(f.__unicode__(),f.nombre)
	print('Test agregar us, exitoso')
    def test_generarHistorialUS(self):
        us= UserStory()
        flujo= Flujo()
        actividad= ActividadesFlujo()
        responsable=User()
        fecha = datetime.date(day=01,month=03,year=2015)
        HistoUS=HistorialUS(us=us,estado=True,flujo=flujo,actividad=actividad,responsable=responsable,estado_actividad=True,fecha=fecha)
        isinstance(HistoUS,HistorialUS)
        print('Test que genera un Historial de un UserStory')
    #tarea
    def test_generarTarea(self):
        us = UserStory()
        fluactpro = ActividadesFlujo()
        tarea=Tarea(descripcion='descripcion',nombre='tarea',tiempo=1,us=us,fluactpro=fluactpro,habilitado=True)
        isinstance(tarea,Tarea)
        print('Test que genera una tarea para un UserStory dado')
    def test_HistorialTarea(self):
        """Clase que representa el historial de los user stories"""
        fecha_creacion =datetime.date(day=01,month=03,year=2015)
        user_story = UserStory()
        documento=Documento()
        hista=Historial(fecha_creacion=fecha_creacion,user_story=user_story,documento=documento)
        isinstance(hista,Historial)
        print('Test que genera un historial de una tarea')
    def test_generarRelease(self):
        us=UserStory()
        re=Release(us=us)
        isinstance(re,Release)

#----------------------------CONFIGURACION
#GenerarEquipo
class TestConfiguracion(TestCase):
    def add_equipo(self, nombre='test',descripcion='test'):
        usuario = UsuarioRolProyecto(1)
        scrum=RolUsuario(1)
        fecha = datetime.date(day=01,month=03,year=2015)
        P = Proyecto.objects.create(nombre=nombre,usuario_scrum=scrum,descripcion=descripcion,fecha_inicio=fecha)
        E = Equipo.objects.create(usuario=usuario,horas=1,sprint=1,proyecto=P)
        return E
    def test_add_equipo(self):
        e = self.add_equipo(nombre='test')
        self.assertTrue(isinstance(e,Equipo))
        print('Test para generar un Equipo, exitoso')
     # tabla para asignar responsable del Us
    def test_asignarResponsable(self):
    # ResponsableUS
       usuario = Equipo()
       us = UserStory()
       res=ResponsableUS(usuario=usuario,us=us)
       isinstance(res,ResponsableUS)
       print('Test para reasignar responsable a un userstory')
#-------------------------SPRINT----------------#
    def Generar_Sprint(self, nombre='test'):
        scrum=RolUsuario(1)
        fecha = datetime.date(day=01,month=03,year=2015)
        proyecto = Proyecto.objects.create(nombre=nombre,usuario_scrum=scrum,descripcion='descripcion',fecha_inicio=fecha)
        fecha_inicio= datetime.date(day=01,month=03,year=2015)
        fecha_fin=datetime.date(day=02,month=04,year=2015)
        S = Sprint.objects.create(estado='Iniciado',proyecto=proyecto,nro_sprint=1,fecha_inicio=fecha_inicio,fecha_fin=fecha_fin,duracion=2,disponibilidad=3,horastotales=8)
        return S
    def test_generar_sprint(self):
        s = self.Generar_Sprint(nombre='test')
        self.assertTrue(isinstance(s,Sprint))
        print('Test para generar un Sprint, exitoso')
    def test_generarUsSprint(self):
        us=UserStory()
        sprint=self.Generar_Sprint(nombre='sprint')
        estado = 'Iniciado'
        proyecto=sprint.proyecto
        UsS=UsSprint(us=us,sprint=sprint,estado=estado,proyecto=proyecto)
        isinstance(UsS,UsSprint)
        print('Test para generar la relacion de  User Story-Sprint')


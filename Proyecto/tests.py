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
	#print(t)
    '''def test_llama_vista_base(self):
	response = self.client.get('/principal')
	self.assertEqual(response.status_code, 302)
	self.assertTemplateUsed(render_to_response, 'main_page.html')
	t=response.content
	#print(t)'''

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
class TestVistas(unittest.TestCase):
    def setUp(self):
        self.client = Client()
    def test_responseCrearProyecto(self):
        response = self.client.get('admin/proyectos/crear_proyecto.html')
        self.assertEqual(response.status_code, 404)
        user = User.objects.create(username='AnonymousUser')
	print response.context['user']

class TestAaLogueo(TestCase):
    def test_ap_page(self):
	c = Client()
	#http://127.0.0.1:8000/login/
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
        product_owner = ProductOwner(1)
        fecha = datetime.date(day=01,month=03,year=2015)
        P = Proyecto.objects.create(nombre=nombre,usuario_scrum=scrum,product_owner=product_owner,descripcion=descripcion,fecha_inicio=fecha,sprint=1)
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
        product_owner = ProductOwner(1)
        fecha = datetime.date(day=01,month=03,year=2015)
        P = Proyecto.objects.create(nombre=nombre,usuario_scrum=scrum,product_owner=product_owner,descripcion=descripcion,fecha_inicio=fecha,sprint=1)
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
    	self.assertFalse(form.is_valid())
#--Actividades
class TestAdminActividades(TestCase):
    def add_proyecto(self, nombre='test',descripcion='test'):
        scrum = RolUsuario(1)
        product_owner = ProductOwner(1)
        fecha = datetime.date(day=01,month=03,year=2015)
        P = Proyecto.objects.create(nombre=nombre,usuario_scrum=scrum,product_owner=product_owner,descripcion=descripcion,fecha_inicio=fecha,sprint=1)
        return P
    def add_Actividad(self,nombre='test'):
        actividad = Actividades.objects.create(nombre = nombre)
        return actividad
    def test_valido_form(self):
    	w = self.add_Actividad(nombre='Act1')
    	data = {'nombre': w.nombre}
	form = 	ActividadesForm(data=data)
    	self.assertFalse(form.is_valid())
	print('formulario valido')
    def test_add_Actividad(self):
        f = self.add_Actividad(nombre='test')
        self.assertTrue(isinstance(f,Actividades))
        self.assertEquals(f.__unicode__(),f.nombre)
	print('Test de crear Actividades, exitoso')
    def add_Actividad(self,nombre='test'):
	p = self.add_proyecto(nombre='test')
        actividad = Actividades.objects.create(nombre = nombre,estado=1,proyecto=p)
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


from django.test import TestCase
from django.contrib.auth.models import User
from app.models import *
import datetime
# tere
class TestAdminProyecto(TestCase):

    def add_proyecto(self, nombre='test',descripcion='test'):
        scrum = RolUsuario(1)
        product_owner = ProductOwner(1)
        fecha = datetime.date(day=01,month=03,year=2015)
        P = Proyecto.objects.create(nombre=nombre,usuario_scrum=scrum,product_owner=product_owner,descripcion=descripcion,fecha_inicio=fecha)
        return P

    def test_add_proyecto(self):
        u = self.add_proyecto(nombre='test')
        self.assertTrue(isinstance(u,Proyecto))
        self.assertEqual(u.__unicode__(), u.nombre)
        print('Test de crear Proyecto, exitoso')

#-------------------------------FLUJOS & ACTIVIDADES-----------------------------------------#

class TestAdminFlujos(TestCase):
    def add_Flujo(self,nombre='test'):
        flujo = Flujo.objects.create(nombre = nombre)
        return flujo
    def test_add_Flujo(self):
        f = self.add_Flujo(nombre='test')
        self.assertTrue(isinstance(f,Flujo))
        self.assertEquals(f.__unicode__(),f.nombre)
        print('Test de crear Flujo, exitoso')

class TestAdminActividades(TestCase):
    def add_Actividad(self,nombre='test'):
        actividad = Actividades.objects.create(nombre = nombre)
        return actividad
    def test_add_Actividad(self):
        f = self.add_Actividad(nombre='test')
        self.assertTrue(isinstance(f,Actividades))
        self.assertEquals(f.__unicode__(),f.nombre)
        print('Test de crear Actividades, exitoso')

class TestProyectoFlujo(TestCase):
    def in_proyecto(self,nombre='test'):
        p = Proyecto.objects.create(nombre = nombre)
        return p
    def in_flujo(self):
        f = Flujo.objects.create(nombre='test')

        self.assertTrue(isinstance(f,Flujo))

        print('Test de flujo por proyecto, exitoso')

class TestFlujoActividades(TestCase):
    def add_Actividad(self,nombre='test'):
        actividad = Actividades.objects.create(nombre = nombre)
        return actividad
    def add_flujo(self,nombre='flujo'):
        f=Flujo.objects.create(nombre=nombre)
    def test_add_ActividadFlujo(self):
        f = self.add_Actividad(nombre='test')
        self.assertTrue(isinstance(f,Actividades))
        self.assertEquals(f.__unicode__(),f.nombre)
        print('Test de asignar FLujo-Actividades, exitoso')
"""
class TestAdminUserStory(TestCase):
    def add_us(self,nombre='test',version='1',descripcion='descripcion',estado='1',prioridad='1',habilitado=True,duracion='1',proyecto='proyecto'):
        usuario = User(1)
        estado=estado
        US = UserStory.objects.create(nombre=nombre,usuario=usuario,descripcion=descripcion)
        return US
    def test_add_us(self):
        f = self.add_us(nombre='test')
        self.assertTrue(isinstance(f,UserStory))

        self.assertEquals(f.__unicode__(),f.nombre)"""


